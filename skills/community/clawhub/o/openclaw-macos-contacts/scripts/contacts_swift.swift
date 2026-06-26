#!/usr/bin/env swift
import Foundation
import Contacts

struct ContactOut: Codable {
    let identifier: String
    let displayName: String
    let givenName: String
    let familyName: String
    let organization: String
    let jobTitle: String
    let phones: [String]
    let emails: [String]
}

struct DuplicateGroup: Codable {
    let key: String
    let count: Int
    let items: [ContactOut]
}

struct Envelope<T: Codable>: Codable {
    let ok: Bool
    let count: Int?
    let query: String?
    let created: Bool?
    let updated: Bool?
    let deleted: Bool?
    let reason: String?
    let item: T?
    let items: [T]?
    let error: String?
}

struct DupEnvelope: Codable {
    let ok: Bool
    let count: Int
    let items: [DuplicateGroup]
}

func printJSON<T: Codable>(_ value: T) {
    let enc = JSONEncoder()
    enc.outputFormatting = [.prettyPrinted, .sortedKeys]
    if let data = try? enc.encode(value), let s = String(data: data, encoding: .utf8) {
        print(s)
    } else {
        print("{\"ok\":false,\"error\":\"encode_failed\"}")
        exit(1)
    }
}

func mapContact(_ c: CNContact) -> ContactOut {
    let phones = c.phoneNumbers.map { $0.value.stringValue }
    let emails = c.emailAddresses.map { String($0.value) }
    let display = CNContactFormatter.string(from: c, style: .fullName) ?? [c.givenName, c.familyName].joined(separator: " ").trimmingCharacters(in: .whitespaces)
    return ContactOut(
        identifier: c.identifier,
        displayName: display,
        givenName: c.givenName,
        familyName: c.familyName,
        organization: c.organizationName,
        jobTitle: c.jobTitle,
        phones: phones,
        emails: emails
    )
}

let args = Array(CommandLine.arguments.dropFirst())
if args.isEmpty {
    printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: "missing_command"))
    exit(2)
}

let store = CNContactStore()
let status = CNContactStore.authorizationStatus(for: .contacts)
if status == .notDetermined {
    let sem = DispatchSemaphore(value: 0)
    var granted = false
    store.requestAccess(for: .contacts) { ok, _ in granted = ok; sem.signal() }
    sem.wait()
    if !granted {
        printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: "contacts_access_denied"))
        exit(3)
    }
} else if status != .authorized {
    printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: "contacts_access_denied"))
    exit(3)
}

let keys: [CNKeyDescriptor] = [
    CNContactIdentifierKey as CNKeyDescriptor,
    CNContactGivenNameKey as CNKeyDescriptor,
    CNContactFamilyNameKey as CNKeyDescriptor,
    CNContactOrganizationNameKey as CNKeyDescriptor,
    CNContactJobTitleKey as CNKeyDescriptor,
    CNContactPhoneNumbersKey as CNKeyDescriptor,
    CNContactEmailAddressesKey as CNKeyDescriptor,
    CNContactFormatter.descriptorForRequiredKeys(for: .fullName)
]

func allContacts() throws -> [CNContact] {
    var results: [CNContact] = []
    let req = CNContactFetchRequest(keysToFetch: keys)
    try store.enumerateContacts(with: req) { c, _ in results.append(c) }
    return results
}

func arg(_ name: String) -> String? {
    if let i = args.firstIndex(of: name), i + 1 < args.count { return args[i+1] }
    return nil
}

switch args[0] {
case "count":
    do {
        let count = try allContacts().count
        printJSON(Envelope<ContactOut>(ok: true, count: count, query: nil, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: nil))
    } catch {
        printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: String(describing: error)))
        exit(1)
    }

case "find":
    let q = arg("--query") ?? ""
    let phone = arg("--phone")
    let email = arg("--email")
    do {
        let contacts = try allContacts().filter { c in
            let hay = [
                CNContactFormatter.string(from: c, style: .fullName) ?? "",
                c.givenName, c.familyName, c.organizationName, c.jobTitle,
                c.phoneNumbers.map{$0.value.stringValue}.joined(separator: " "),
                c.emailAddresses.map{String($0.value)}.joined(separator: " ")
            ].joined(separator: " ").lowercased()
            let qok = q.isEmpty ? false : hay.contains(q.lowercased())
            let pok = phone == nil ? false : c.phoneNumbers.contains { $0.value.stringValue == phone! }
            let eok = email == nil ? false : c.emailAddresses.contains { String($0.value) == email! }
            return qok || pok || eok
        }
        let items = contacts.map(mapContact)
        printJSON(Envelope(ok: true, count: items.count, query: q.isEmpty ? nil : q, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: items, error: nil))
    } catch {
        printJSON(Envelope<ContactOut>(ok: false, count: nil, query: q, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: String(describing: error)))
        exit(1)
    }

case "create":
    let first = arg("--first-name") ?? ""
    let last = arg("--last-name") ?? ""
    let org = arg("--organization") ?? ""
    let title = arg("--job-title") ?? ""
    let phone = arg("--phone")
    let email = arg("--email")
    do {
        let contacts = try allContacts()
        let dup = contacts.first { c in
            let phoneMatch = phone != nil && !phone!.isEmpty && c.phoneNumbers.contains { $0.value.stringValue == phone! }
            let emailMatch = email != nil && !email!.isEmpty && c.emailAddresses.contains { String($0.value) == email! }
            let fullNameMatch = !first.isEmpty && !last.isEmpty && c.givenName == first && c.familyName == last
            if phoneMatch || emailMatch { return true }
            if phone == nil && email == nil && fullNameMatch { return true }
            return false
        }
        if let dup = dup {
            printJSON(Envelope(ok: false, count: 1, query: nil, created: false, updated: nil, deleted: nil, reason: "duplicate_detected", item: mapContact(dup), items: nil, error: nil))
            exit(0)
        }
        let contact = CNMutableContact()
        contact.givenName = first
        contact.familyName = last
        contact.organizationName = org
        contact.jobTitle = title
        if let phone = phone, !phone.isEmpty {
            contact.phoneNumbers = [CNLabeledValue(label: CNLabelPhoneNumberMobile, value: CNPhoneNumber(stringValue: phone))]
        }
        if let email = email, !email.isEmpty {
            contact.emailAddresses = [CNLabeledValue(label: CNLabelWork, value: email as NSString)]
        }
        let save = CNSaveRequest()
        save.add(contact, toContainerWithIdentifier: nil)
        try store.execute(save)
        let created = try store.unifiedContact(withIdentifier: contact.identifier, keysToFetch: keys)
        printJSON(Envelope(ok: true, count: 1, query: nil, created: true, updated: nil, deleted: nil, reason: nil, item: mapContact(created), items: nil, error: nil))
    } catch {
        printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: String(describing: error)))
        exit(1)
    }

case "update":
    guard let identifier = arg("--identifier") else {
        printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: "missing_identifier"))
        exit(2)
    }
    let first = arg("--first-name")
    let last = arg("--last-name")
    let org = arg("--organization")
    let title = arg("--job-title")
    let phone = arg("--phone")
    let email = arg("--email")
    do {
        let current = try store.unifiedContact(withIdentifier: identifier, keysToFetch: keys)
        let mutable = current.mutableCopy() as! CNMutableContact
        if let first = first { mutable.givenName = first }
        if let last = last { mutable.familyName = last }
        if let org = org { mutable.organizationName = org }
        if let title = title { mutable.jobTitle = title }
        if let phone = phone { mutable.phoneNumbers = phone.isEmpty ? [] : [CNLabeledValue(label: CNLabelPhoneNumberMobile, value: CNPhoneNumber(stringValue: phone))] }
        if let email = email { mutable.emailAddresses = email.isEmpty ? [] : [CNLabeledValue(label: CNLabelWork, value: email as NSString)] }
        let save = CNSaveRequest()
        save.update(mutable)
        try store.execute(save)
        let updated = try store.unifiedContact(withIdentifier: identifier, keysToFetch: keys)
        printJSON(Envelope(ok: true, count: 1, query: nil, created: nil, updated: true, deleted: nil, reason: nil, item: mapContact(updated), items: nil, error: nil))
    } catch {
        printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: false, deleted: nil, reason: nil, item: nil, items: nil, error: String(describing: error)))
        exit(1)
    }

case "delete":
    guard let identifier = arg("--identifier") else {
        printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: "missing_identifier"))
        exit(2)
    }
    do {
        let current = try store.unifiedContact(withIdentifier: identifier, keysToFetch: keys)
        let mutable = current.mutableCopy() as! CNMutableContact
        let snapshot = mapContact(current)
        let save = CNSaveRequest()
        save.delete(mutable)
        try store.execute(save)
        printJSON(Envelope(ok: true, count: 1, query: nil, created: nil, updated: nil, deleted: true, reason: nil, item: snapshot, items: nil, error: nil))
    } catch {
        printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: nil, deleted: false, reason: nil, item: nil, items: nil, error: String(describing: error)))
        exit(1)
    }

case "duplicates":
    do {
        let contacts = try allContacts().map(mapContact)
        var groups: [String: [ContactOut]] = [:]
        for c in contacts {
            let name = c.displayName.trimmingCharacters(in: .whitespacesAndNewlines)
            let phone = c.phones.first ?? ""
            let email = c.emails.first ?? ""
            let key = [name, phone, email].joined(separator: " | ")
            if !name.isEmpty { groups[key, default: []].append(c) }
        }
        let dupGroups = groups
            .filter { $0.value.count > 1 }
            .map { DuplicateGroup(key: $0.key, count: $0.value.count, items: $0.value) }
            .sorted { $0.count > $1.count }
        printJSON(DupEnvelope(ok: true, count: dupGroups.count, items: dupGroups))
    } catch {
        printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: String(describing: error)))
        exit(1)
    }

default:
    printJSON(Envelope<ContactOut>(ok: false, count: nil, query: nil, created: nil, updated: nil, deleted: nil, reason: nil, item: nil, items: nil, error: "unknown_command"))
    exit(2)
}
