#!/usr/bin/env swift
import EventKit
import Foundation

// Define output structures
struct CalendarInfo: Codable {
    let name: String
    let account: String
    let type: String
    let writable: Bool
    let isCloud: Bool
}

struct Output: Codable {
    let calendars: [CalendarInfo]
}

let store = EKEventStore()

// Request calendar access (macOS 14+ uses requestFullAccessToEvents)
let semaphore = DispatchSemaphore(value: 0)
var accessGranted = false

if #available(macOS 14.0, *) {
    store.requestFullAccessToEvents { granted, error in
        accessGranted = granted
        semaphore.signal()
    }
} else {
    store.requestAccess(to: .event) { granted, error in
        accessGranted = granted
        semaphore.signal()
    }
}
semaphore.wait()

guard accessGranted else {
    print("{\"calendars\": [], \"error\": \"Calendar access denied\"}")
    exit(0)
}

let calendars = store.calendars(for: .event)

var infos: [CalendarInfo] = []

for cal in calendars {
    guard let source = cal.source else { continue }
    
    var typeString = "Unknown"
    var isCloud = false
    
    switch source.sourceType {
    case .local:
        typeString = "Local"
        isCloud = false
    case .exchange:
        typeString = "Exchange"
        isCloud = true
    case .calDAV:
        typeString = "CalDAV (iCloud/Google)"
        isCloud = true
    case .mobileMe:
        typeString = "MobileMe"
        isCloud = true
    case .subscribed:
        typeString = "Subscribed"
        isCloud = true
    case .birthdays:
        typeString = "Birthdays"
        isCloud = false // Treated as local read-only usually
    @unknown default:
        typeString = "Other"
    }
    
    // Check writability
    let isWritable = cal.allowsContentModifications
    
    infos.append(CalendarInfo(
        name: cal.title,
        account: source.title,
        type: typeString,
        writable: isWritable,
        isCloud: isCloud
    ))
}

// Output JSON
let output = Output(calendars: infos)
let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted
if let data = try? encoder.encode(output), let jsonString = String(data: data, encoding: .utf8) {
    print(jsonString)
}
