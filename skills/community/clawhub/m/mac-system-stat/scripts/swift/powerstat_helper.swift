import Foundation
import IOKit

struct ChannelSample: Codable {
    let name: String
    let unit: String
    let joules: Double
    let watts: Double
}

struct PowerPayload: Codable {
    let kind: String
    let implemented: Bool
    let supported: Bool
    let sample_interval_ms: Int
    let subsystem_power_watts: [String: Double]
    let channels: [ChannelSample]
    let notes: [String]

    init(supported: Bool, sample_interval_ms: Int, subsystem_power_watts: [String: Double], channels: [ChannelSample], notes: [String]) {
        self.kind = "powerstat"
        self.implemented = true
        self.supported = supported
        self.sample_interval_ms = sample_interval_ms
        self.subsystem_power_watts = subsystem_power_watts
        self.channels = channels
        self.notes = notes
    }
}

private func energyToJoules(_ value: Double, unit: String) -> Double? {
    switch unit {
    case "mJ": return value / 1e3
    case "uJ": return value / 1e6
    case "nJ": return value / 1e9
    case "J": return value
    default: return nil
    }
}

private func category(for name: String) -> String? {
    if name == "CPU Energy" || name.hasSuffix("CPU Energy") { return "cpu" }
    if name == "GPU Energy" || name.hasSuffix("GPU Energy") { return "gpu" }
    if name == "ANE" || name.hasPrefix("ANE") { return "ane" }
    if name == "DRAM" || name.hasPrefix("DRAM") { return "dram" }
    if name.hasPrefix("PCI") && name.hasSuffix("Energy") { return "pci" }
    return nil
}

private func getChannels() -> CFMutableDictionary? {
    guard let energyModel = IOReportCopyChannelsInGroup("Energy Model" as CFString, nil, 0, 0, 0)?.takeRetainedValue() else {
        return nil
    }
    let size = CFDictionaryGetCount(energyModel)
    return CFDictionaryCreateMutableCopy(kCFAllocatorDefault, size, energyModel)
}

private func takeSnapshot(subscription: IOReportSubscriptionRef, channels: CFMutableDictionary) -> [String: (unit: String, joules: Double)]? {
    guard let sample = IOReportCreateSamples(subscription, channels, nil)?.takeRetainedValue(),
          let dict = sample as? [String: Any],
          let items = dict["IOReportChannels"] as? [Any] else {
        return nil
    }

    var result: [String: (unit: String, joules: Double)] = [:]
    for itemAny in items {
        let item = itemAny as! CFDictionary
        guard let group = IOReportChannelGetGroup(item)?.takeUnretainedValue() as String?, group == "Energy Model",
              let name = IOReportChannelGetChannelName(item)?.takeUnretainedValue() as String?,
              let unit = IOReportChannelGetUnitLabel(item)?.takeUnretainedValue() as String? else {
            continue
        }
        guard let cat = category(for: name) else { continue }
        let raw = Double(IOReportSimpleGetIntegerValue(item, 0))
        guard let joules = energyToJoules(raw, unit: unit) else { continue }
        if let existing = result[cat] {
            result[cat] = (unit: unit, joules: existing.joules + joules)
        } else {
            result[cat] = (unit: unit, joules: joules)
        }
    }
    return result
}

let intervalMs: Int = {
    if CommandLine.arguments.count > 1, let value = Int(CommandLine.arguments[1]), value >= 100 {
        return value
    }
    return 1000
}()

let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]

func emit(_ payload: PowerPayload) -> Never {
    let data = try! encoder.encode(payload)
    FileHandle.standardOutput.write(data)
    FileHandle.standardOutput.write("\n".data(using: .utf8)!)
    exit(0)
}

guard let channels = getChannels() else {
    emit(PowerPayload(supported: false, sample_interval_ms: intervalMs, subsystem_power_watts: [:], channels: [], notes: ["IOReport Energy Model channels were not available on this host."]))
}

var scratch: Unmanaged<CFMutableDictionary>?
guard let subscription = IOReportCreateSubscription(nil, channels, &scratch, 0, nil) else {
    emit(PowerPayload(supported: false, sample_interval_ms: intervalMs, subsystem_power_watts: [:], channels: [], notes: ["IOReport subscription creation failed."]))
}
_ = scratch?.takeRetainedValue()

guard let first = takeSnapshot(subscription: subscription, channels: channels) else {
    emit(PowerPayload(supported: false, sample_interval_ms: intervalMs, subsystem_power_watts: [:], channels: [], notes: ["Initial IOReport sample failed."]))
}

usleep(useconds_t(intervalMs * 1000))

guard let second = takeSnapshot(subscription: subscription, channels: channels) else {
    emit(PowerPayload(supported: false, sample_interval_ms: intervalMs, subsystem_power_watts: [:], channels: [], notes: ["Second IOReport sample failed."]))
}

let seconds = Double(intervalMs) / 1000.0
let order = ["cpu", "gpu", "ane", "dram", "pci"]
var subsystem: [String: Double] = [:]
var channelsOut: [ChannelSample] = []

for key in order {
    guard let end = second[key], let start = first[key] else { continue }
    let deltaJoules = max(0, end.joules - start.joules)
    let watts = deltaJoules / seconds
    subsystem[key] = watts
    channelsOut.append(ChannelSample(name: key, unit: "W", joules: deltaJoules, watts: watts))
}

emit(PowerPayload(supported: !subsystem.isEmpty, sample_interval_ms: intervalMs, subsystem_power_watts: subsystem, channels: channelsOut, notes: ["Non-privileged IOReport Energy Model sampling.", "Values are delta-based average power over the sample window."]))
