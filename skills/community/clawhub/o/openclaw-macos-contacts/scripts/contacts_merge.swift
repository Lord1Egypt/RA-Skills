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

struct MergePlan: Codable {
    let key: String
    let keepIdentifier: String
    let dropIdentifiers: [String]
    let merged: ContactOut
    let originals: [ContactOut]
}

struct Envelope<T: Codable>: Codable {
    let ok: Bool
    let count: Int?
    let item: T?
    let items: [T]?
    let applied: Bool?
    let error: String?
}

func printJSON<T: Codable>(_ value: T) {
    let enc = JSONEncoder()
    enc.outputFormatting = [.prettyPrinted, .sortedKeys]
    let data = try! enc.encode(value)
    print(String(data: data, encoding: .utf8)!)
}

func mapContact(_ c: CNContact) -> ContactOut {
    let phones = c.phoneNumbers.map { $0.value.stringValue }
    let emails = c.emailAddresses.map { String($0.value) }
    let display = CNContactFormatter.string(from: c, style: .fullName) ?? [c.givenName, c.familyName].joined(separator: " ").trimmingCharacters(in: .whitespaces)
    return ContactOut(identifier: c.identifier, displayName: display, givenName: c.givenName, familyName: c.familyName, organization: c.organizationName, jobTitle: c.jobTitle, phones: phones, emails: emails)
}

let args = Array(CommandLine.arguments.dropFirst())
func arg(_ name: String) -> String? { if let i = args.firstIndex(of: name), i + 1 < args.count { return args[i+1] } ; return nil }
func flag(_ name: String) -> Bool { args.contains(name) }

let store = CNContactStore()
let status = CNContactStore.authorizationStatus(for: .contacts)
if status != .authorized {
    let sem = DispatchSemaphore(value: 0)
    var granted = false
    if status == .notDetermined {
        store.requestAccess(for: .contacts) { ok, _ in granted = ok; sem.signal() }
        sem.wait()
    }
    if !(status == .authorized || granted) {
        printJSON(Envelope<MergePlan>(ok: false, count: nil, item: nil, items: nil, applied: nil, error: "contacts_access_denied"))
        exit(3)
    }
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

func score(_ c: ContactOut) -> Int {
    var s = 0
    if !c.organization.isEmpty { s += 3 }
    if !c.jobTitle.isEmpty { s += 3 }
    s += c.phones.count * 2
    s += c.emails.count * 2
    if !c.givenName.isEmpty { s += 1 }
    if !c.familyName.isEmpty { s += 1 }
    return s
}

func mergedContact(from contacts: [ContactOut], keep: ContactOut) -> ContactOut {
    let phones = Array(Set(contacts.flatMap { $0.phones })).sorted()
    let emails = Array(Set(contacts.flatMap { $0.emails })).sorted()
    let org = keep.organization.isEmpty ? (contacts.first { !$0.organization.isEmpty }?.organization ?? "") : keep.organization
    let title = keep.jobTitle.isEmpty ? (contacts.first { !$0.jobTitle.isEmpty }?.jobTitle ?? "") : keep.jobTitle
    return ContactOut(identifier: keep.identifier, displayName: keep.displayName, givenName: keep.givenName, familyName: keep.familyName, organization: org, jobTitle: title, phones: phones, emails: emails)
}

if args.isEmpty { printJSON(Envelope<MergePlan>(ok: false, count: nil, item: nil, items: nil, applied: nil, error: "missing_command")); exit(2) }

switch args[0] {
case "plan-duplicates":
    let all = try allContacts().map(mapContact)
    var groups: [String: [ContactOut]] = [:]
    for c in all {
        let name = c.displayName.trimmingCharacters(in: .whitespacesAndNewlines)
        let phone = c.phones.first ?? ""
        let email = c.emails.first ?? ""
        let key = [name, phone, email].joined(separator: " | ")
        if !name.isEmpty { groups[key, default: []].append(c) }
    }
    let plans = groups.values.filter { $0.count > 1 }.map { grp -> MergePlan in
        let sorted = grp.sorted { score($0) > score($1) }
        let keep = sorted[0]
        let merged = mergedContact(from: grp, keep: keep)
        return MergePlan(key: [keep.displayName, keep.phones.first ?? "", keep.emails.first ?? ""].joined(separator: " | "), keepIdentifier: keep.identifier, dropIdentifiers: sorted.dropFirst().map{$0.identifier}, merged: merged, originals: grp)
    }
    printJSON(Envelope(ok: true, count: plans.count, item: nil, items: plans, applied: false, error: nil))

case "apply-plan":
    guard let keepId = arg("--keep") else { printJSON(Envelope<MergePlan>(ok: false, count: nil, item: nil, items: nil, applied: nil, error: "missing_keep")); exit(2) }
    let dropIds = args.enumerated().compactMap { idx, val in val == "--drop" && idx + 1 < args.count ? args[idx+1] : nil }
    if dropIds.isEmpty { printJSON(Envelope<MergePlan>(ok: false, count: nil, item: nil, items: nil, applied: nil, error: "missing_drop")); exit(2) }
    let contacts = try allContacts()
    let mapped = contacts.map(mapContact)
    guard let keep = mapped.first(where: { $0.identifier == keepId }) else { printJSON(Envelope<MergePlan>(ok: false, count: nil, item: nil, items: nil, applied: nil, error: "keep_not_found")); exit(2) }
    let originals = mapped.filter { [$0.identifier].contains(where: { _ in false }) }
    let allSet = mapped.filter { ([keepId] + dropIds).contains($0.identifier) }
    let merged = mergedContact(from: allSet, keep: keep)
    let current = try store.unifiedContact(withIdentifier: keepId, keysToFetch: keys)
    let mutable = current.mutableCopy() as! CNMutableContact
    mutable.organizationName = merged.organization
    mutable.jobTitle = merged.jobTitle
    mutable.phoneNumbers = merged.phones.map { CNLabeledValue(label: CNLabelPhoneNumberMobile, value: CNPhoneNumber(stringValue: $0)) }
    mutable.emailAddresses = merged.emails.map { CNLabeledValue(label: CNLabelWork, value: $0 as NSString) }
    let save = CNSaveRequest()
    save.update(mutable)
    for id in dropIds {
        if let c = try? store.unifiedContact(withIdentifier: id, keysToFetch: keys) {
            save.delete(c.mutableCopy() as! CNMutableContact)
        }
    }
    try store.execute(save)
    let final = try store.unifiedContact(withIdentifier: keepId, keysToFetch: keys)
    let plan = MergePlan(key: [keep.displayName, keep.phones.first ?? "", keep.emails.first ?? ""].joined(separator: " | "), keepIdentifier: keepId, dropIdentifiers: dropIds, merged: mapContact(final), originals: allSet)
    printJSON(Envelope(ok: true, count: 1, item: plan, items: nil, applied: true, error: nil))

default:
    printJSON(Envelope<MergePlan>(ok: false, count: nil, item: nil, items: nil, applied: nil, error: "unknown_command"))
    exit(2)
}
