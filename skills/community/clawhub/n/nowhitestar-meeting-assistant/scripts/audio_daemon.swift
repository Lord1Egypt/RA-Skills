// audio_daemon.swift — ScreenCaptureKit 系统音频 + 麦克风 + 半双工混音
// 替代 BlackHole + SoX 的方案。
//
// 编译:
//   swiftc -o audio_daemon audio_daemon.swift \
//     -framework Cocoa -framework ScreenCaptureKit \
//     -framework AVFoundation -framework CoreMedia -framework CoreAudio

import Cocoa
import ScreenCaptureKit
import AVFoundation
import CoreMedia

let HOME = FileManager.default.homeDirectoryForCurrentUser
let CONFIG_DIR = HOME.appendingPathComponent(".config/meeting-assistant")
let SOCKET_PATH = CONFIG_DIR.appendingPathComponent("audio_daemon.sock")
let STATE_PATH = CONFIG_DIR.appendingPathComponent(".state.json")
let PID_PATH = CONFIG_DIR.appendingPathComponent(".audio_daemon.pid")
let LOG_PATH = CONFIG_DIR.appendingPathComponent("audio_daemon.log")
let SILENCE_THRESHOLD: Float = 0.01
let SYS_ACTIVE_THRESHOLD: Float = 0.001  // 系统音频常偏低，半双工判断不能用自动静音阈值
let DEFAULT_SILENCE_SEC: TimeInterval = 300
let FADE_FRAMES = Int(0.5 * 48000)
let SAMPLE_RATE: UInt32 = 48000

var SYS_READY = false
var SYS_ERROR = ""
var MIC_READY = false
var MIC_ERROR = ""
var SYS_FORMAT_LOGGED = false

func defaultRecordingDir() -> URL {
    // AudioDaemon.app lives at <repo>/meeting-assistant/scripts/AudioDaemon.app.
    // Store recordings at <repo>/meeting-recordings by default.
    let app = Bundle.main.bundleURL
    let repo = app
        .deletingLastPathComponent() // scripts
        .deletingLastPathComponent() // nested meeting-assistant
        .deletingLastPathComponent() // repo root
    return repo.appendingPathComponent("meeting-recordings")
}

func loadRecordingDir() -> URL {
    let configPath = CONFIG_DIR.appendingPathComponent("config.json")
    guard let data = try? Data(contentsOf: configPath),
          let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
          let audio = json["audio"] as? [String: Any],
          let raw = audio["output_dir"] as? String,
          !raw.isEmpty else {
        return defaultRecordingDir()
    }
    let path = raw.hasPrefix("~/") ? HOME.appendingPathComponent(String(raw.dropFirst(2))).path : raw
    return URL(fileURLWithPath: path)
}

let RECORDING_DIR = loadRecordingDir()

var logFile: FileHandle?
func log(_ msg: String) {
    let df = DateFormatter(); df.dateFormat = "yyyy-MM-dd HH:mm:ss"
    let line = "[\(df.string(from: Date()))] \(msg)"
    print(line); fflush(stdout)
    logFile?.write(Data((line + "\n").utf8))
}

// ─── WAV 写入器 ───────────────────────────────────────

class WavWriter {
    let url: URL
    var audioData = Data()

    init?(url: URL) {
        self.url = url
    }

    func append(_ data: Data) { audioData.append(data) }

    func finalize() {
        let audioSize = UInt32(audioData.count)
        let fileSize = audioSize + 44 - 8
        var h = Data()
        h.append(contentsOf: [0x52,0x49,0x46,0x46] as [UInt8])
        var v32 = fileSize.littleEndian
        withUnsafeBytes(of: &v32) { h.append(Data($0)) }
        h.append(contentsOf: [0x57,0x41,0x56,0x45] as [UInt8])
        h.append(contentsOf: [0x66,0x6D,0x74,0x20] as [UInt8])
        v32 = UInt32(16).littleEndian
        withUnsafeBytes(of: &v32) { h.append(Data($0)) }
        var v16 = UInt16(1).littleEndian
        withUnsafeBytes(of: &v16) { h.append(Data($0)) }
        v16 = UInt16(2).littleEndian
        withUnsafeBytes(of: &v16) { h.append(Data($0)) }
        v32 = UInt32(48000).littleEndian
        withUnsafeBytes(of: &v32) { h.append(Data($0)) }
        v32 = UInt32(48000*2*2).littleEndian
        withUnsafeBytes(of: &v32) { h.append(Data($0)) }
        v16 = UInt16(4).littleEndian
        withUnsafeBytes(of: &v16) { h.append(Data($0)) }
        v16 = UInt16(16).littleEndian
        withUnsafeBytes(of: &v16) { h.append(Data($0)) }
        h.append(contentsOf: [0x64,0x61,0x74,0x61] as [UInt8])
        v32 = audioSize.littleEndian
        withUnsafeBytes(of: &v32) { h.append(Data($0)) }
        h.append(audioData)
        try? h.write(to: url)
    }
}

func normalizeToDBFS(_ samples: [Int16], targetDB: Float = -20) -> [Int16] {
    guard !samples.isEmpty else { return samples }
    var sum: Float = 0; let m = Float(Int(Int16.max) * Int(Int16.max))
    for s in samples { sum += Float(s) * Float(s) / m }
    let rms = sqrt(sum / Float(samples.count))
    guard rms > 0.0001 else { return samples }
    let gain = pow(10.0, targetDB / 20.0) / rms
    let clamped = min(max(gain, 0.1), 10.0)
    return samples.map { Int16(max(-1.0, min(1.0, Float($0) / Float(Int16.max) * clamped)) * Float(Int16.max)) }
}

// ─── 状态管理 ──────────────────────────────────────────

func writeState(recording: Bool, title: String = "", path: String = "") {
    let df = ISO8601DateFormatter()
    let d: [String: Any] = ["recording": recording, "title": title, "file_path": path,
                             "updated_at": df.string(from: Date())]
    if let data = try? JSONSerialization.data(withJSONObject: d, options: .prettyPrinted) {
        try? data.write(to: STATE_PATH)
    }
}

// ─── 音频数据管理器 + 半双工混音 ───────────────────────

class AudioRecorder {
    var writer: WavWriter?
    var isRecording = false
    var startTime: Date?
    var lastAudioTime: Date?
    var silenceTask: DispatchWorkItem?
    var silenceSeconds = DEFAULT_SILENCE_SEC
    var onStopRequest: (() -> Void)?

    // Streaming buffers
    var sysBuf: [Int16] = []
    var micBuf: [Int16] = []
    let bufLock = NSLock()
    var fadePos: Float = 0  // 半双工混音进度（跨 chunk 持久）

    func start(title: String) -> String? {
        let df = DateFormatter(); df.dateFormat = "yyyyMMdd_HHmmss"
        let fn = "\(title.components(separatedBy: .alphanumerics.inverted).joined())_\(df.string(from: Date())).wav"
        let url = RECORDING_DIR.appendingPathComponent(fn)
        try? FileManager.default.createDirectory(at: RECORDING_DIR, withIntermediateDirectories: true)
        guard let w = WavWriter(url: url) else { return nil }
        writer = w; isRecording = true; startTime = Date(); lastAudioTime = Date()
        sysBuf = []; micBuf = []; fadePos = 0
        writeState(recording: true, title: title, path: url.path)
        log("🎙 \(fn)")
        startSilenceMonitor()
        return url.path
    }

    @discardableResult
    func stop() -> (path: String?, duration: Int) {
        isRecording = false
        silenceTask?.cancel()
        let dur = startTime.map { Int(Date().timeIntervalSince($0)) } ?? 0
        // Write remaining audio
        flushBuffers()
        let p = writer?.url.path
        writer?.finalize(); writer = nil
        writeState(recording: false)
        log("⏹ \(dur)s")
        return (p, dur)
    }

    func onSysAudio(_ samples: [Int16]) {
        guard isRecording else { return }
        bufLock.lock()
        sysBuf.append(contentsOf: samples)
        bufLock.unlock()
        let rms = calcRMS(samples)
        if rms > SILENCE_THRESHOLD { lastAudioTime = Date() }
        mixAndWrite()
    }

    func onMicAudio(_ samples: [Float]) {
        guard isRecording else { return }
        let ints = samples.map { Int16(max(-1.0, min(1.0, $0)) * Float(Int16.max)) }
        bufLock.lock()
        micBuf.append(contentsOf: ints)
        bufLock.unlock()
        let rms = calcRMS(ints)
        if rms > SILENCE_THRESHOLD { lastAudioTime = Date() }
        mixAndWrite()
    }

    private func calcRMS(_ s: [Int16]) -> Float {
        guard !s.isEmpty else { return 0 }
        var sum: Float = 0; let m = Float(Int(Int16.max) * Int(Int16.max))
        for v in s { sum += Float(v) * Float(v) / m }
        return sqrt(sum / Float(s.count))
    }

    /// 流式混音：从 sysBuf/micBuf 取等量的样本，半双工混合后写出
    private func mixAndWrite() {
        guard let w = writer else { return }
        bufLock.lock()
        // 取能混的最多样本数（sys 是 stereo, mic 是 mono）
        let outLen = sysBuf.count  // sys 驱动输出速率
        guard outLen >= 1024 else { bufLock.unlock(); return }  // 至少等 10ms 的数据再写
        let sysChunk = Array(sysBuf.prefix(outLen))
        sysBuf.removeFirst(outLen)

        // 从 micBuf 取对应 mono 样本数（sys/2 因为 stereo vs mono）
        let micNeeded = outLen / 2
        let micChunk: [Int16]
        if micBuf.count >= micNeeded {
            micChunk = Array(micBuf.prefix(micNeeded))
            micBuf.removeFirst(micNeeded)
        } else {
            micChunk = micBuf + [Int16](repeating: 0, count: micNeeded - micBuf.count)
            micBuf.removeAll()
        }
        bufLock.unlock()

        let mixed = halfDuplexMix(sys: sysChunk, mic: micChunk)
        w.append(Data(bytes: mixed, count: mixed.count * 2))
    }

    private func halfDuplexMix(sys: [Int16], mic: [Int16]) -> [Int16] {
        let n = sys.count  // stereo samples
        let m = min(mic.count, n / 2)  // mono samples

        // No normalization - use raw levels to avoid distortion
        let sysNorm = sys
        let micMono = mic
        var micStereo = [Int16](repeating: 0, count: n)
        for i in 0..<n { micStereo[i] = micMono[min(i/2, m-1)] }

        // Per-frame RMS analysis (30ms frames)
        let frameSamples = Int(SAMPLE_RATE * 30 / 1000) * 2  // stereo frame
        let numFrames = max(1, n / frameSamples)
        let fadeStep: Float = 1.0 / Float(Int(SAMPLE_RATE) * 2)

        var out = [Int16](repeating: 0, count: n)

        for fi in 0..<numFrames {
            let start = fi * frameSamples
            let end = min(start + frameSamples, n)
            let sysFrame = sysNorm[start..<end]
            var sysSum: Float = 0; let mVal = Float(Int(Int16.max) * Int(Int16.max))
            for v in sysFrame { sysSum += Float(v) * Float(v) / mVal }
            let sysActive = sqrt(sysSum / Float(end - start)) > SYS_ACTIVE_THRESHOLD

            if sysActive { fadePos = 0 }
            else { fadePos = min(1.0, fadePos + fadeStep * Float(end - start)) }

            let mixRatio = 1.0 - fadePos
            for i in start..<end {
                let sv = Float(sysNorm[i]) / Float(Int16.max)
                let mv = Float(micStereo[i]) / Float(Int16.max)
                out[i] = Int16(max(-1.0, min(1.0, mixRatio * sv + fadePos * mv)) * Float(Int16.max))
            }
        }
        return out
    }

    private func flushBuffers() {
        guard let w = writer else { return }
        bufLock.lock()
        if !sysBuf.isEmpty || !micBuf.isEmpty {
            let outLen = sysBuf.isEmpty ? micBuf.count * 2 : sysBuf.count
            let sys: [Int16] = sysBuf.isEmpty ? [Int16](repeating: 0, count: outLen) : sysBuf
            let mic: [Int16] = micBuf.isEmpty ? [Int16](repeating: 0, count: outLen/2) : micBuf
            sysBuf.removeAll(); micBuf.removeAll()
            bufLock.unlock()
            w.append(Data(bytes: halfDuplexMix(sys: sys, mic: Array(mic.prefix(outLen/2))), count: outLen * 2))
        } else { bufLock.unlock() }
    }

    private func startSilenceMonitor() {
        silenceTask?.cancel()
        let task = DispatchWorkItem { [weak self] in
            guard let self = self, self.isRecording else { return }
            if let last = self.lastAudioTime, Date().timeIntervalSince(last) >= self.silenceSeconds {
                log("🔇 silence \(Int(self.silenceSeconds))s — auto stop")
                self.onStopRequest?()
            }
        }
        silenceTask = task
        DispatchQueue.main.asyncAfter(deadline: .now() + silenceSeconds, execute: task)
    }
}

class MicCapture {
    let recorder: AudioRecorder
    var engine: AVAudioEngine?

    init(recorder: AudioRecorder) { self.recorder = recorder }

    func start() {
        let engine = AVAudioEngine()
        let input = engine.inputNode
        let fmt = input.outputFormat(forBus: 0)

        input.installTap(onBus: 0, bufferSize: 4096, format: fmt) { [weak self] buf, _ in
            guard let self = self, self.recorder.isRecording else { return }
            guard let chData = buf.floatChannelData else { return }
            let len = Int(buf.frameLength)
            let samples = Array(UnsafeBufferPointer(start: chData[0], count: len))
            self.recorder.onMicAudio(samples)
        }

        do { try engine.start(); self.engine = engine; MIC_READY = true; MIC_ERROR = ""; log("🎤 Mic capture started") }
        catch { MIC_READY = false; MIC_ERROR = "\(error)"; log("Mic start failed: \(error)") }
    }

    func stop() { engine?.stop(); engine = nil }
}

// ─── SCStream 输出处理器 ──────────────────────────────

@available(macOS 12.3, *)
class SysAudioOutput: NSObject, SCStreamOutput {
    unowned let recorder: AudioRecorder
    init(_ r: AudioRecorder) { recorder = r }

    func stream(_ s: SCStream, didOutputSampleBuffer buf: CMSampleBuffer, of type: SCStreamOutputType) {
        guard type == .audio, recorder.isRecording else { return }
        let asbd = buf.formatDescription.flatMap { CMAudioFormatDescriptionGetStreamBasicDescription($0)?.pointee }
        let flags = asbd?.mFormatFlags ?? 0
        let channels = Int(asbd?.mChannelsPerFrame ?? 2)
        let isFloat = (flags & kAudioFormatFlagIsFloat) != 0
        let isInt = (flags & kAudioFormatFlagIsSignedInteger) != 0
        let nonInterleaved = (flags & kAudioFormatFlagIsNonInterleaved) != 0
        if !SYS_FORMAT_LOGGED, let a = asbd {
            SYS_FORMAT_LOGGED = true
            log("SC audio ASBD: sr=\(a.mSampleRate) ch=\(a.mChannelsPerFrame) bits=\(a.mBitsPerChannel) bytesFrame=\(a.mBytesPerFrame) bytesPacket=\(a.mBytesPerPacket) framesPacket=\(a.mFramesPerPacket) float=\(isFloat) int=\(isInt) nonInterleaved=\(nonInterleaved) flags=0x\(String(flags, radix:16))")
        }
        guard let db = buf.dataBuffer else { return }
        var ptr: UnsafeMutablePointer<Int8>?; var len: Int = 0
        guard CMBlockBufferGetDataPointer(db, atOffset: 0, lengthAtOffsetOut: &len, totalLengthOut: nil, dataPointerOut: &ptr) == noErr,
              let p = ptr, len > 0 else { return }
        let cnt = len / MemoryLayout<Float>.size
        guard cnt > 0 else { return }

        let raw = UnsafeMutableRawPointer(p)
        let floats = [Float](UnsafeBufferPointer(start: raw.assumingMemoryBound(to: Float.self), count: cnt))
        let stereoFloats: [Float]
        if isFloat && nonInterleaved && channels >= 2 {
            // ScreenCaptureKit reports planar Float32. In CMBlockBuffer this is
            // laid out as all left samples followed by all right samples.
            let frames = cnt / channels
            var interleaved = [Float](); interleaved.reserveCapacity(frames * 2)
            for i in 0..<frames {
                interleaved.append(floats[i])
                interleaved.append(floats[frames + i])
            }
            stereoFloats = interleaved
        } else if isFloat && channels == 1 {
            var stereo = [Float](); stereo.reserveCapacity(cnt * 2)
            for v in floats { stereo.append(v); stereo.append(v) }
            stereoFloats = stereo
        } else {
            stereoFloats = floats
        }
        guard !stereoFloats.isEmpty else { return }
        let int16s = stereoFloats.map { Int16(max(-1.0, min(1.0, $0)) * Float(Int16.max)) }
        recorder.onSysAudio(int16s)
    }
}

// ─── 屏幕捕获管理器 ───────────────────────────────────

@available(macOS 12.3, *)
class AudioCapture {
    let recorder: AudioRecorder
    let output: SysAudioOutput
    var stream: SCStream?

    init(recorder: AudioRecorder) {
        self.recorder = recorder
        self.output = SysAudioOutput(recorder)
    }

    func startCapture() {
        Task {
            do {
                let content = try await SCShareableContent.current
                guard let d = content.displays.first else { log("No display"); return }
                let filter = SCContentFilter(display: d, excludingWindows: [])
                let config = SCStreamConfiguration()
                config.capturesAudio = true
                let s = SCStream(filter: filter, configuration: config, delegate: nil)
                try await s.startCapture()
                try s.addStreamOutput(output, type: .audio, sampleHandlerQueue: .global())
                self.stream = s
                SYS_READY = true; SYS_ERROR = ""
                log("🔊 Sys capture started (display \(d.displayID))")
            } catch {
                SYS_READY = false; SYS_ERROR = (error as NSError).localizedDescription
                log("Sys capture failed: \(SYS_ERROR)")
            }
        }
    }

    func stopCapture() { Task { try? await stream?.stopCapture() }; stream = nil }
}

// ─── Socket 服务器 ────────────────────────────────────

class SocketServer {
    let recorder: AudioRecorder
    var sock: Int32 = -1

    init(_ r: AudioRecorder) { recorder = r }

    func stop() {
        if sock >= 0 { close(sock); sock = -1 }
    }

    func start() {
        try? FileManager.default.removeItem(at: SOCKET_PATH)
        sock = Darwin.socket(AF_UNIX, SOCK_STREAM, 0)
        guard sock >= 0 else { log("Socket: create failed"); return }
        var addr = sockaddr_un()
        addr.sun_family = sa_family_t(AF_UNIX)
        _ = SOCKET_PATH.path.withCString { strncpy(&addr.sun_path.0, $0, min(SOCKET_PATH.path.utf8.count, 103)) }
        let ok = withUnsafePointer(to: &addr) {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) { Darwin.bind(sock, $0, socklen_t(MemoryLayout<sockaddr_un>.size)) }
        }
        guard ok == 0 else { log("Socket: bind \(ok)"); close(sock); sock = -1; return }
        Darwin.listen(sock, 5); chmod(SOCKET_PATH.path, 0o666)
        log("Socket ready")
        DispatchQueue.global(qos: .background).async { [weak self] in
            while true {
                let c = Darwin.accept(self?.sock ?? -1, nil, nil)
                if c >= 0 { self?.handle(c); close(c) }
            }
        }
    }

    private func handle(_ c: Int32) {
        var data = Data()
        var buf = [UInt8](repeating: 0, count: 4096)
        while true { let n = read(c, &buf, 4096); if n <= 0 { break }; data.append(buf, count: n) }
        guard let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let action = json["action"] as? String else { send(c, ["error":"invalid"]); return }
        var resp: [String: Any]
        switch action {
        case "windows":
            resp = self.scanWindows()
        case "start":
            if !SYS_READY {
                resp = ["error":"sys_capture_not_ready", "sysReady": SYS_READY, "sysError": SYS_ERROR, "micReady": MIC_READY, "micError": MIC_ERROR]
            } else if !MIC_READY {
                resp = ["error":"mic_capture_not_ready", "sysReady": SYS_READY, "sysError": SYS_ERROR, "micReady": MIC_READY, "micError": MIC_ERROR]
            } else if let p = recorder.start(title: json["title"] as? String ?? "meeting") { resp = ["status":"recording", "file":p] }
            else { resp = ["error":"start_failed"] }
        case "stop":
            let (p, d) = recorder.stop(); resp = ["status":"stopped", "file": p ?? "", "duration": d]
        case "status":
            resp = ["recording": recorder.isRecording, "file": recorder.writer?.url.path ?? "", "sysReady": SYS_READY, "sysError": SYS_ERROR, "micReady": MIC_READY, "micError": MIC_ERROR]
        case "quit": resp = ["status":"bye"]; send(c, resp)
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) { NSApp.terminate(nil) }; return
        default: resp = ["error":"unknown: \(action)"]
        }
        send(c, resp)
    }

    private func send(_ c: Int32, _ d: [String: Any]) {
        guard let data = try? JSONSerialization.data(withJSONObject: d) else { return }
        data.withUnsafeBytes { if let b = $0.baseAddress { _ = write(c, b, data.count) } }
    }

    func scanWindows() -> [String: Any] {
        let workspace = NSWorkspace.shared
        var results: [[String: String]] = []
        let apps = workspace.runningApplications
        for app in apps where app.activationPolicy == .regular {
            let appElem = AXUIElementCreateApplication(app.processIdentifier)
            var winList: CFTypeRef?
            guard AXUIElementCopyAttributeValue(appElem, kAXWindowsAttribute as CFString, &winList) == .success,
                  let wins = winList as? [AXUIElement] else { continue }
            for w in wins {
                var title: CFTypeRef?
                AXUIElementCopyAttributeValue(w, kAXTitleAttribute as CFString, &title)
                if let t = title as? String, !t.isEmpty {
                    results.append(["app": app.localizedName ?? "", "title": t])
                }
            }
        }
        return ["windows": results]
    }
}

// ─── App Delegate ──────────────────────────────────────

class AppDelegate: NSObject, NSApplicationDelegate {
    var recorder: AudioRecorder?
    var micCapture: MicCapture?
    var audioCapture: AudioCapture?
    var socketServer: SocketServer?

    func applicationDidFinishLaunching(_ n: Notification) {
        try? FileManager.default.createDirectory(at: CONFIG_DIR, withIntermediateDirectories: true)
        FileManager.default.createFile(atPath: LOG_PATH.path, contents: nil)
        logFile = try? FileHandle(forWritingTo: LOG_PATH)
        try? "\(ProcessInfo.processInfo.processIdentifier)".write(to: PID_PATH, atomically: true, encoding: .utf8)
        log("🎧 Audio Daemon (pid=\(ProcessInfo.processInfo.processIdentifier))")

        let rec = AudioRecorder(); recorder = rec
        rec.onStopRequest = { [weak self] in self?.recorder?.stop() }

        if #available(macOS 12.3, *) {
            let ac = AudioCapture(recorder: rec); audioCapture = ac
            DispatchQueue.main.asyncAfter(deadline: .now() + 1) { ac.startCapture() }
        }
        let mic = MicCapture(recorder: rec); micCapture = mic
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) { mic.start() }

        let ss = SocketServer(rec); socketServer = ss; ss.start()
        log("Ready")
    }

    func applicationWillTerminate(_ n: Notification) {
        recorder?.stop(); socketServer?.stop(); audioCapture?.stopCapture(); micCapture?.stop()
        try? FileManager.default.removeItem(at: PID_PATH)
        try? FileManager.default.removeItem(at: SOCKET_PATH)
        try? logFile?.close()
    }
}

// ─── 入口 ──────────────────────────────────────────────

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.accessory)
app.run()
