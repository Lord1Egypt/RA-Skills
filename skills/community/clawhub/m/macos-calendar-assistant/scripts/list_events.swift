#!/usr/bin/env swift
import EventKit
import Foundation

// Define output structure
struct EventInfo: Codable {
    let uid: String
    let title: String
    let start: Double // Timestamp
    let end: Double   // Timestamp
    let isAllDay: Bool
    let calendar: String
    let location: String?
    let notes: String?
}

struct Output: Codable {
    let events: [EventInfo]
}

let store = EKEventStore()

// Args: start ISO8601, end ISO8601
// Example: 2026-03-03T00:00:00+08:00 2026-03-03T23:59:59+08:00
let args = CommandLine.arguments
guard args.count >= 3 else {
    // Return empty list if args missing (or error)
    print("{\"events\": []}")
    exit(0)
}

let isoFormatter = ISO8601DateFormatter()
guard let startDate = isoFormatter.date(from: args[1]),
      let endDate = isoFormatter.date(from: args[2]) else {
    print("{\"error\": \"Invalid ISO format\"}")
    exit(1)
}

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
    print("{\"events\": [], \"error\": \"Calendar access denied\"}")
    exit(0)
}

// Fetch events
let calendars = store.calendars(for: .event) // All calendars
let predicate = store.predicateForEvents(withStart: startDate, end: endDate, calendars: nil)
let events = store.events(matching: predicate)

var outputEvents: [EventInfo] = []

for event in events {
    outputEvents.append(EventInfo(
        uid: event.calendarItemIdentifier,
        title: event.title,
        start: event.startDate.timeIntervalSince1970,
        end: event.endDate.timeIntervalSince1970,
        isAllDay: event.isAllDay,
        calendar: event.calendar.title,
        location: event.location,
        notes: event.notes
    ))
}

let output = Output(events: outputEvents)
let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted
if let data = try? encoder.encode(output), let jsonString = String(data: data, encoding: .utf8) {
    print(jsonString)
}
