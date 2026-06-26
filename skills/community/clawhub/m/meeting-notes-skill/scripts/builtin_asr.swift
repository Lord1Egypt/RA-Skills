import Foundation
import Speech

func authStatusText(_ status: SFSpeechRecognizerAuthorizationStatus) -> String {
    switch status {
    case .notDetermined:
        return "notDetermined"
    case .denied:
        return "denied"
    case .restricted:
        return "restricted"
    case .authorized:
        return "authorized"
    @unknown default:
        return "unknown"
    }
}

let args = CommandLine.arguments
if args.count < 2 {
    fputs("Usage: swift builtin_asr.swift <audio-file> [locale]\n", stderr)
    exit(1)
}

let audioPath = args[1]
let localeId = args.count >= 3 ? args[2] : "zh-CN"
let audioURL = URL(fileURLWithPath: audioPath)

guard FileManager.default.fileExists(atPath: audioPath) else {
    fputs("Audio file not found: \(audioPath)\n", stderr)
    exit(1)
}

guard let recognizer = SFSpeechRecognizer(locale: Locale(identifier: localeId)) else {
    fputs("Speech recognizer unavailable for locale: \(localeId)\n", stderr)
    exit(2)
}

if !recognizer.isAvailable {
    fputs("Speech recognizer is currently unavailable.\n", stderr)
    exit(2)
}

let sem = DispatchSemaphore(value: 0)
var finalText = ""
var done = false
var task: SFSpeechRecognitionTask?

SFSpeechRecognizer.requestAuthorization { status in
    guard status == .authorized else {
        fputs("Speech authorization status: \(authStatusText(status)) (\(status.rawValue)). Enable Speech Recognition for your terminal/app in macOS Privacy settings.\n", stderr)
        sem.signal()
        return
    }

    let req = SFSpeechURLRecognitionRequest(url: audioURL)
    // Do not force on-device/cloud; let system pick the best available path.
    req.shouldReportPartialResults = true

    task = recognizer.recognitionTask(with: req) { result, error in
        if let r = result {
            finalText = r.bestTranscription.formattedString
            if r.isFinal && !done {
                done = true
                print(finalText)
                sem.signal()
            }
        }
        if let e = error, !done {
            done = true
            fputs("Recognition error: \(e.localizedDescription)\n", stderr)
            sem.signal()
        }
    }
}

let timeout = DispatchTime.now() + .seconds(180)
_ = sem.wait(timeout: timeout)

let out = finalText.trimmingCharacters(in: .whitespacesAndNewlines)
if out.isEmpty {
    fputs("No transcription produced.\n", stderr)
    exit(1)
}
if !done {
    // Timeout or early completion without final callback: return best partial text.
    print(out)
}
