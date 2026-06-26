import Foundation
import IOKit

struct TemperatureSensor: Codable {
    let key: String
    let label: String
    let group: String
    let celsius: Double
}

struct TemperatureSummary: Codable {
    let cpu_celsius: Double?
    let battery_celsius: Double?
    let ambient_celsius: Double?
    let hottest_celsius: Double?
    let hottest_label: String?
    let hottest_key: String?
}

struct TemperaturePayload: Codable {
    let kind: String
    let implemented: Bool
    let supported: Bool
    let sensors: [TemperatureSensor]
    let summary: TemperatureSummary
    let notes: [String]

    init(supported: Bool, sensors: [TemperatureSensor], summary: TemperatureSummary, notes: [String]) {
        self.kind = "tempstat"
        self.implemented = true
        self.supported = supported
        self.sensors = sensors
        self.summary = summary
        self.notes = notes
    }
}

enum SMCDataType: String {
    case ui8 = "ui8 "
    case ui16 = "ui16"
    case ui32 = "ui32"
    case sp1e = "sp1e"
    case sp3c = "sp3c"
    case sp4b = "sp4b"
    case sp5a = "sp5a"
    case spa5 = "spa5"
    case sp69 = "sp69"
    case sp78 = "sp78"
    case sp87 = "sp87"
    case sp96 = "sp96"
    case spb4 = "spb4"
    case spf0 = "spf0"
    case flt = "flt "
    case fpe2 = "fpe2"
}

enum SMCKeys: UInt8 {
    case kernelIndex = 2
    case readBytes = 5
    case readKeyInfo = 9
}

struct SMCKeyData {
    typealias Bytes = (UInt8, UInt8, UInt8, UInt8, UInt8, UInt8, UInt8, UInt8,
                       UInt8, UInt8, UInt8, UInt8, UInt8, UInt8, UInt8, UInt8,
                       UInt8, UInt8, UInt8, UInt8, UInt8, UInt8, UInt8, UInt8,
                       UInt8, UInt8, UInt8, UInt8, UInt8, UInt8, UInt8, UInt8)

    struct Version { var major: UInt8 = 0; var minor: UInt8 = 0; var build: UInt8 = 0; var reserved: UInt8 = 0; var release: UInt16 = 0 }
    struct LimitData { var version: UInt16 = 0; var length: UInt16 = 0; var cpuPLimit: UInt32 = 0; var gpuPLimit: UInt32 = 0; var memPLimit: UInt32 = 0 }
    struct KeyInfo { var dataSize: IOByteCount32 = 0; var dataType: UInt32 = 0; var dataAttributes: UInt8 = 0 }

    var key: UInt32 = 0
    var vers = Version()
    var pLimitData = LimitData()
    var keyInfo = KeyInfo()
    var padding: UInt16 = 0
    var result: UInt8 = 0
    var status: UInt8 = 0
    var data8: UInt8 = 0
    var data32: UInt32 = 0
    var bytes: Bytes = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
}

struct SMCValue {
    var key: String
    var dataSize: UInt32 = 0
    var dataType: String = ""
    var bytes: [UInt8] = Array(repeating: 0, count: 32)
}

struct SensorProbe {
    let key: String
    let label: String
    let group: String
}

extension FourCharCode {
    init(fromString string: String) {
        self = string.utf8.reduce(0) { ($0 << 8) | UInt32($1) }
    }

    func asString() -> String {
        String(UnicodeScalar(self >> 24 & 0xff)!) +
        String(UnicodeScalar(self >> 16 & 0xff)!) +
        String(UnicodeScalar(self >> 8 & 0xff)!) +
        String(UnicodeScalar(self & 0xff)!)
    }
}

extension UInt16 {
    init(bytes: (UInt8, UInt8)) {
        self = UInt16(bytes.0) << 8 | UInt16(bytes.1)
    }
}

extension UInt32 {
    init(bytes: (UInt8, UInt8, UInt8, UInt8)) {
        self = UInt32(bytes.0) << 24 | UInt32(bytes.1) << 16 | UInt32(bytes.2) << 8 | UInt32(bytes.3)
    }
}

extension Int {
    init(fromFPE2 bytes: (UInt8, UInt8)) {
        self = (Int(bytes.0) << 6) + (Int(bytes.1) >> 2)
    }
}

extension Float {
    init?(_ bytes: [UInt8]) {
        self = bytes.withUnsafeBytes { $0.load(fromByteOffset: 0, as: Self.self) }
    }
}

final class SMC {
    private var conn: io_connect_t = 0

    init?() {
        var iterator: io_iterator_t = 0
        let matching = IOServiceMatching("AppleSMC")
        let result = IOServiceGetMatchingServices(kIOMainPortDefault, matching, &iterator)
        guard result == kIOReturnSuccess else { return nil }
        let device = IOIteratorNext(iterator)
        IOObjectRelease(iterator)
        guard device != 0 else { return nil }
        let openResult = IOServiceOpen(device, mach_task_self_, 0, &conn)
        IOObjectRelease(device)
        guard openResult == kIOReturnSuccess else { return nil }
    }

    deinit { IOServiceClose(conn) }

    func getValue(_ key: String) -> Double? {
        var value = SMCValue(key: key)
        guard read(&value) == kIOReturnSuccess else { return nil }
        if value.dataSize == 0 || value.bytes.first(where: { $0 != 0 }) == nil { return nil }

        switch value.dataType {
        case SMCDataType.ui8.rawValue: return Double(value.bytes[0])
        case SMCDataType.ui16.rawValue: return Double(UInt16(bytes: (value.bytes[0], value.bytes[1])))
        case SMCDataType.ui32.rawValue: return Double(UInt32(bytes: (value.bytes[0], value.bytes[1], value.bytes[2], value.bytes[3])))
        case SMCDataType.sp1e.rawValue: return Double(UInt16(value.bytes[0]) * 256 + UInt16(value.bytes[1])) / 16384
        case SMCDataType.sp3c.rawValue: return Double(UInt16(value.bytes[0]) * 256 + UInt16(value.bytes[1])) / 4096
        case SMCDataType.sp4b.rawValue: return Double(UInt16(value.bytes[0]) * 256 + UInt16(value.bytes[1])) / 2048
        case SMCDataType.sp5a.rawValue: return Double(UInt16(value.bytes[0]) * 256 + UInt16(value.bytes[1])) / 1024
        case SMCDataType.sp69.rawValue: return Double(UInt16(value.bytes[0]) * 256 + UInt16(value.bytes[1])) / 512
        case SMCDataType.sp78.rawValue: return Double(Int(value.bytes[0]) * 256 + Int(value.bytes[1])) / 256
        case SMCDataType.sp87.rawValue: return Double(Int(value.bytes[0]) * 256 + Int(value.bytes[1])) / 128
        case SMCDataType.sp96.rawValue: return Double(Int(value.bytes[0]) * 256 + Int(value.bytes[1])) / 64
        case SMCDataType.spa5.rawValue: return Double(UInt16(value.bytes[0]) * 256 + UInt16(value.bytes[1])) / 32
        case SMCDataType.spb4.rawValue: return Double(Int(value.bytes[0]) * 256 + Int(value.bytes[1])) / 16
        case SMCDataType.spf0.rawValue: return Double(Int(value.bytes[0]) * 256 + Int(value.bytes[1]))
        case SMCDataType.flt.rawValue:
            if let f = Float(value.bytes) { return Double(f) }
            return nil
        case SMCDataType.fpe2.rawValue: return Double(Int(fromFPE2: (value.bytes[0], value.bytes[1])))
        default: return nil
        }
    }

    private func read(_ value: inout SMCValue) -> kern_return_t {
        var input = SMCKeyData()
        var output = SMCKeyData()
        input.key = FourCharCode(fromString: value.key)
        input.data8 = SMCKeys.readKeyInfo.rawValue

        var result = call(SMCKeys.kernelIndex.rawValue, input: &input, output: &output)
        guard result == kIOReturnSuccess else { return result }

        value.dataSize = UInt32(output.keyInfo.dataSize)
        value.dataType = output.keyInfo.dataType.asString()
        input.keyInfo.dataSize = output.keyInfo.dataSize
        input.data8 = SMCKeys.readBytes.rawValue

        result = call(SMCKeys.kernelIndex.rawValue, input: &input, output: &output)
        guard result == kIOReturnSuccess else { return result }

        memcpy(&value.bytes, &output.bytes, Int(value.dataSize))
        return kIOReturnSuccess
    }

    private func call(_ index: UInt8, input: inout SMCKeyData, output: inout SMCKeyData) -> kern_return_t {
        let inputSize = MemoryLayout<SMCKeyData>.stride
        var outputSize = MemoryLayout<SMCKeyData>.stride
        return IOConnectCallStructMethod(conn, UInt32(index), &input, inputSize, &output, &outputSize)
    }
}

let probes: [SensorProbe] = [
    SensorProbe(key: "Tp0P", label: "CPU proximity", group: "cpu"),
    SensorProbe(key: "Tp0T", label: "CPU die average", group: "cpu"),
    SensorProbe(key: "Te0T", label: "Efficiency cluster", group: "cpu"),
    SensorProbe(key: "Ts0P", label: "SoC proximity", group: "soc"),
    SensorProbe(key: "TB0T", label: "Battery", group: "battery"),
    SensorProbe(key: "TW0P", label: "Wireless", group: "board"),
]

let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]

func emit(_ payload: TemperaturePayload) -> Never {
    let data = try! encoder.encode(payload)
    FileHandle.standardOutput.write(data)
    FileHandle.standardOutput.write("\n".data(using: .utf8)!)
    exit(0)
}

guard let smc = SMC() else {
    emit(TemperaturePayload(
        supported: false,
        sensors: [],
        summary: TemperatureSummary(cpu_celsius: nil, battery_celsius: nil, ambient_celsius: nil, hottest_celsius: nil, hottest_label: nil, hottest_key: nil),
        notes: ["AppleSMC service could not be opened."]
    ))
}

var sensors: [TemperatureSensor] = []
for probe in probes {
    if let value = smc.getValue(probe.key), value > -40, value < 140 {
        sensors.append(TemperatureSensor(key: probe.key, label: probe.label, group: probe.group, celsius: value))
    }
}

let hottest = sensors.max(by: { $0.celsius < $1.celsius })
let cpuSensors = sensors.filter { $0.group == "cpu" }
let batterySensor = sensors.first { $0.group == "battery" }
let ambientSensor = sensors.first { $0.group == "ambient" }

let summary = TemperatureSummary(
    cpu_celsius: cpuSensors.isEmpty ? nil : cpuSensors.map(\ .celsius).reduce(0, +) / Double(cpuSensors.count),
    battery_celsius: batterySensor?.celsius,
    ambient_celsius: ambientSensor?.celsius,
    hottest_celsius: hottest?.celsius,
    hottest_label: hottest?.label,
    hottest_key: hottest?.key
)

var notes = ["Non-privileged AppleSMC temperature readout."]
if sensors.isEmpty {
    notes.append("No known temperature keys returned values on this host.")
} else {
    notes.append("Reported values come from a conservative curated key list; absent components are omitted instead of guessed.")
}

emit(TemperaturePayload(supported: !sensors.isEmpty, sensors: sensors, summary: summary, notes: notes))
