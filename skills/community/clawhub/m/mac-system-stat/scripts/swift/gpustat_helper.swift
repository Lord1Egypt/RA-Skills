import Foundation
import IOKit

struct GPUCard: Codable {
    let registry_id: UInt64
    let accelerator_class: String?
    let model: String?
    let gpu_core_count: Int?
    let performance_statistics: [String: Int64]
    let registry_properties: [String: String]
}

struct GPUPayload: Codable {
    let kind: String
    let implemented: Bool
    let supported: Bool
    let cards: [GPUCard]
    let notes: [String]

    init(supported: Bool, cards: [GPUCard], notes: [String]) {
        self.kind = "gpustat"
        self.implemented = true
        self.supported = supported
        self.cards = cards
        self.notes = notes
    }
}

let trackedPerfKeys = [
    "Device Utilization %",
    "Renderer Utilization %",
    "Tiler Utilization %",
    "Alloc system memory",
    "In use system memory",
    "In use system memory (driver)",
    "recoveryCount",
    "lastRecoveryTime",
    "SplitSceneCount",
    "TiledSceneBytes",
    "Allocated PB Size",
]

let trackedRegistryKeys = [
    "MetalPluginName",
    "MetalPluginClassName",
    "IOClass",
    "IONameMatched",
    "IOSourceVersion",
]

private func extractInt64(_ value: Any?) -> Int64? {
    switch value {
    case let n as NSNumber:
        return n.int64Value
    case let s as String:
        return Int64(s)
    default:
        return nil
    }
}

private func decodeModel(_ value: Any?) -> String? {
    switch value {
    case let s as String:
        return s
    case let data as Data:
        return String(data: data, encoding: .utf8)?.trimmingCharacters(in: CharacterSet(charactersIn: "\0"))
    case let nsData as NSData:
        return String(data: nsData as Data, encoding: .utf8)?.trimmingCharacters(in: CharacterSet(charactersIn: "\0"))
    default:
        return nil
    }
}

private func copyProperties(entry: io_registry_entry_t) -> [String: Any]? {
    var unmanaged: Unmanaged<CFMutableDictionary>?
    let kr = IORegistryEntryCreateCFProperties(entry, &unmanaged, kCFAllocatorDefault, 0)
    guard kr == KERN_SUCCESS, let dict = unmanaged?.takeRetainedValue() as? [String: Any] else {
        return nil
    }
    return dict
}

private func makeCard(entry: io_registry_entry_t, properties: [String: Any]) -> GPUCard {
    var registryID: UInt64 = 0
    _ = IORegistryEntryGetRegistryEntryID(entry, &registryID)

    let perfRaw = properties["PerformanceStatistics"] as? [String: Any] ?? [:]
    var perf: [String: Int64] = [:]
    for key in trackedPerfKeys {
        if let value = extractInt64(perfRaw[key]) {
            perf[key] = value
        }
    }

    var reg: [String: String] = [:]
    for key in trackedRegistryKeys {
        if let value = properties[key] {
            reg[key] = String(describing: value)
        }
    }

    return GPUCard(
        registry_id: registryID,
        accelerator_class: (properties["IOClass"] as? String) ?? reg["IOClass"],
        model: decodeModel(properties["model"]),
        gpu_core_count: extractInt64(properties["gpu-core-count"]).map(Int.init),
        performance_statistics: perf,
        registry_properties: reg
    )
}

private func loadCards() -> [GPUCard] {
    var iterator: io_iterator_t = 0
    let matching = IOServiceMatching("IOAccelerator")
    let kr = IOServiceGetMatchingServices(kIOMainPortDefault, matching, &iterator)
    guard kr == KERN_SUCCESS else { return [] }
    defer { IOObjectRelease(iterator) }

    var cards: [GPUCard] = []
    while case let entry = IOIteratorNext(iterator), entry != 0 {
        defer { IOObjectRelease(entry) }
        guard let props = copyProperties(entry: entry) else { continue }
        if props["PerformanceStatistics"] == nil && props["model"] == nil { continue }
        cards.append(makeCard(entry: entry, properties: props))
    }
    return cards
}

let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]

func emit(_ payload: GPUPayload) -> Never {
    let data = try! encoder.encode(payload)
    FileHandle.standardOutput.write(data)
    FileHandle.standardOutput.write("\n".data(using: .utf8)!)
    exit(0)
}

let cards = loadCards()
if cards.isEmpty {
    emit(GPUPayload(supported: false, cards: [], notes: ["No IOAccelerator registry entries with GPU statistics were found."]))
}

emit(GPUPayload(supported: cards.contains { !$0.performance_statistics.isEmpty }, cards: cards, notes: ["Non-privileged IOKit registry read via IORegistryEntryCreateCFProperties."]))
