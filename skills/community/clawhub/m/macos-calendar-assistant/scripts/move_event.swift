import EventKit
import Foundation

let store = EKEventStore()
let calendar = Calendar.current
let dateFormatter = ISO8601DateFormatter()
dateFormatter.formatOptions = [.withInternetDateTime, .withDashSeparatorInDate, .withColonSeparatorInTime, .withTimeZone]

func parseDate(_ iso: String) -> Date? {
    return dateFormatter.date(from: iso)
}

if CommandLine.arguments.count < 5 {
    print("Usage: move_event.swift <Title> <Calendar> <NewStartISO> <DurationMinutes> [--original-start <ISO>] [--search-days <N>]")
    exit(1)
}

let targetTitle = CommandLine.arguments[1]
let targetCalendarName = CommandLine.arguments[2]
let newStartISO = CommandLine.arguments[3]
let durationMinutes = Double(CommandLine.arguments[4])!

var originalStart: Date? = nil
var searchDays = 7

var i = 5
while i < CommandLine.arguments.count {
    let arg = CommandLine.arguments[i]
    if arg == "--original-start", i + 1 < CommandLine.arguments.count {
        originalStart = parseDate(CommandLine.arguments[i + 1])
        i += 2
        continue
    }
    if arg == "--search-days", i + 1 < CommandLine.arguments.count {
        searchDays = max(1, Int(CommandLine.arguments[i + 1]) ?? 7)
        i += 2
        continue
    }
    i += 1
}

guard let newStartDate = parseDate(newStartISO) else {
    print("Error: Invalid date format (use ISO8601)")
    exit(1)
}

let semaphore = DispatchSemaphore(value: 0)

store.requestAccess(to: .event) { granted, _ in
    guard granted else {
        print("Access denied")
        semaphore.signal()
        return
    }

    let calendars = store.calendars(for: .event)
    guard let cal = calendars.first(where: { $0.title == targetCalendarName }) else {
        print("Error: Calendar '\(targetCalendarName)' not found")
        semaphore.signal()
        return
    }

    let startSearch: Date
    let endSearch: Date

    if let o = originalStart {
        let dayStart = calendar.startOfDay(for: o)
        startSearch = calendar.date(byAdding: .day, value: -1, to: dayStart)!
        endSearch = calendar.date(byAdding: .day, value: 2, to: dayStart)!
    } else {
        let now = Date()
        let dayStart = calendar.startOfDay(for: now)
        startSearch = calendar.date(byAdding: .day, value: -searchDays, to: dayStart)!
        endSearch = calendar.date(byAdding: .day, value: searchDays + 1, to: dayStart)!
    }

    let predicate = store.predicateForEvents(withStart: startSearch, end: endSearch, calendars: [cal])
    let events = store.events(matching: predicate)

    let matched: EKEvent?
    if let o = originalStart {
        matched = events.first(where: { $0.title == targetTitle && abs($0.startDate.timeIntervalSince(o)) < 60 })
            ?? events.first(where: { $0.title == targetTitle })
    } else {
        matched = events.first(where: { $0.title == targetTitle })
    }

    if let event = matched {
        event.startDate = newStartDate
        event.endDate = newStartDate.addingTimeInterval(durationMinutes * 60)

        do {
            try store.save(event, span: .thisEvent)
            print("moved: \(event.title ?? targetTitle) -> \(newStartDate)")
        } catch {
            print("Error saving: \(error)")
        }
    } else {
        print("Error: Event '\(targetTitle)' not found in search window")
    }

    semaphore.signal()
}

semaphore.wait()
