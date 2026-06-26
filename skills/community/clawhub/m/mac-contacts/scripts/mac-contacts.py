#!/usr/bin/env python3
import Contacts
import argparse
import re
import sys
import subprocess
try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)
from Foundation import NSDateComponents

def get_store():
    """Returns the shared CNContactStore."""
    return Contacts.CNContactStore.alloc().init()

def get_keys_to_fetch():
    """Returns a comprehensive list of keys to fetch for a complete CLI."""
    return [
        Contacts.CNContactIdentifierKey,
        Contacts.CNContactNamePrefixKey,
        Contacts.CNContactGivenNameKey,
        Contacts.CNContactMiddleNameKey,
        Contacts.CNContactFamilyNameKey,
        Contacts.CNContactNameSuffixKey,
        Contacts.CNContactNicknameKey,
        Contacts.CNContactOrganizationNameKey,
        Contacts.CNContactJobTitleKey,
        Contacts.CNContactDepartmentNameKey,
        Contacts.CNContactNoteKey,
        Contacts.CNContactPhoneNumbersKey,
        Contacts.CNContactEmailAddressesKey,
        Contacts.CNContactPostalAddressesKey,
        Contacts.CNContactUrlAddressesKey,
        Contacts.CNContactSocialProfilesKey,
        Contacts.CNContactBirthdayKey,
        Contacts.CNContactDatesKey,
        Contacts.CNContactThumbnailImageDataKey,
    ]

def request_access():
    """Requests access to contacts if not already granted."""
    status = Contacts.CNContactStore.authorizationStatusForEntityType_(Contacts.CNEntityTypeContacts)
    if status != Contacts.CNAuthorizationStatusAuthorized:
        store = get_store()
        success = store.requestAccessForEntityType_(Contacts.CNEntityTypeContacts)
        if not success:
            print(f"Error: Access denied to contacts.")
            sys.exit(1)

def find_group(name, store=None):
    """Finds a group by name."""
    if store is None: store = get_store()
    all_groups, error = store.groupsMatchingPredicate_error_(None, None)
    if error or not all_groups:
        return None
    for g in all_groups:
        if g.name() == name:
            return g
    return None

def get_contact_groups(contact_id, store):
    """Returns list of group names the contact belongs to."""
    all_groups, _ = store.groupsMatchingPredicate_error_(None, None)
    if not all_groups:
        return []
    id_keys = [Contacts.CNContactIdentifierKey]
    member_groups = []
    for group in all_groups:
        pred = Contacts.CNContact.predicateForContactsInGroupWithIdentifier_(group.identifier())
        members, _ = store.unifiedContactsMatchingPredicate_keysToFetch_error_(pred, id_keys, None)
        for m in (members or []):
            if m.identifier() == contact_id:
                member_groups.append(group.name())
                break
    return member_groups

def enumerate_contacts(store, keys, filter_fn):
    """Single-pass enumeration over all contacts. Returns those passing filter_fn."""
    request = Contacts.CNContactFetchRequest.alloc().initWithKeysToFetch_(keys)
    results = []
    def handler(contact, stop):
        try:
            if filter_fn(contact):
                results.append(contact)
        except Exception:
            pass
    store.enumerateContactsWithFetchRequest_error_usingBlock_(request, None, handler)
    return results

def labeled_str(label):
    """Localize a CNLabeledValue label string."""
    if not label:
        return ""
    result = Contacts.CNLabeledValue.localizedStringForLabel_(label)
    return str(result) if result else ""


def parse_birthday(s):
    """Parse YYYY-MM-DD or --MM-DD into NSDateComponents, or exit on bad input."""
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', s)
    if m:
        comps = NSDateComponents.alloc().init()
        comps.setYear_(int(m.group(1)))
        comps.setMonth_(int(m.group(2)))
        comps.setDay_(int(m.group(3)))
        return comps
    m = re.match(r'^--(\d{2})-(\d{2})$', s)
    if m:
        comps = NSDateComponents.alloc().init()
        comps.setMonth_(int(m.group(1)))
        comps.setDay_(int(m.group(2)))
        return comps
    print(f"Error: --birthday must be YYYY-MM-DD or --MM-DD, got: {s!r}")
    sys.exit(1)

def contact_to_dict(contact, store=None, full=False):
    """Build a plain dict from a CNContact for YAML serialization.

    full=False (search): compact — flat phone/email/address string lists.
    full=True  (show):   all fields, nested label/value dicts, groups.
    """
    d = {}

    d['id'] = str(contact.identifier())

    if contact.namePrefix():       d['name_prefix']  = str(contact.namePrefix())
    if contact.givenName():        d['given_name']   = str(contact.givenName())
    if contact.middleName():       d['middle_name']  = str(contact.middleName())
    if contact.familyName():       d['family_name']  = str(contact.familyName())
    if contact.nameSuffix():       d['name_suffix']  = str(contact.nameSuffix())
    if contact.nickname():         d['nickname']     = str(contact.nickname())
    if contact.organizationName(): d['organization'] = str(contact.organizationName())

    if full:
        if contact.jobTitle():       d['job_title']  = str(contact.jobTitle())
        if contact.departmentName(): d['department'] = str(contact.departmentName())

    if full:
        phones = []
        for p in (contact.phoneNumbers() or []):
            entry = {'number': str(p.value().stringValue())}
            lbl = labeled_str(p.label())
            if lbl: entry['label'] = lbl
            phones.append(entry)
        emails = []
        for e in (contact.emailAddresses() or []):
            entry = {'address': str(e.value())}
            lbl = labeled_str(e.label())
            if lbl: entry['label'] = lbl
            emails.append(entry)
        addrs = []
        for a in (contact.postalAddresses() or []):
            v = a.value()
            entry = {}
            lbl = labeled_str(a.label())
            if lbl:            entry['label']   = lbl
            if v.street():     entry['street']  = str(v.street())
            if v.city():       entry['city']    = str(v.city())
            if v.state():      entry['state']   = str(v.state())
            if v.postalCode(): entry['zip']     = str(v.postalCode())
            if v.country():    entry['country'] = str(v.country())
            addrs.append(entry)
    else:
        phones = [str(p.value().stringValue()) for p in (contact.phoneNumbers() or [])]
        emails = [str(e.value())               for e in (contact.emailAddresses() or [])]
        addrs  = []
        for a in (contact.postalAddresses() or []):
            v = a.value()
            parts = [v.city(), v.state(), v.country()]
            s = ', '.join(p for p in parts if p)
            if s: addrs.append(s)

    if phones: d['phones']    = phones
    if emails: d['emails']    = emails
    if addrs:  d['addresses'] = addrs

    if full:
        urls = []
        for u in (contact.urlAddresses() or []):
            entry = {'url': str(u.value())}
            lbl = labeled_str(u.label())
            if lbl: entry['label'] = lbl
            urls.append(entry)
        if urls: d['urls'] = urls

        social = []
        for s in (contact.socialProfiles() or []):
            social.append({'service': str(s.value().service()),
                           'username': str(s.value().username())})
        if social: d['social'] = social

        if contact.birthday():
            bday = contact.birthday()
            y = bday.year()
            d['birthday'] = (f'{y:04d}-{bday.month():02d}-{bday.day():02d}'
                             if y and y != 1
                             else f'--{bday.month():02d}-{bday.day():02d}')

        dates = []
        for dt in (contact.dates() or []):
            dc = dt.value()
            y = dc.year()
            date_str = (f'{y:04d}-{dc.month():02d}-{dc.day():02d}'
                        if y and y != 1
                        else f'--{dc.month():02d}-{dc.day():02d}')
            entry = {'date': date_str}
            lbl = labeled_str(dt.label())
            if lbl: entry['label'] = lbl
            dates.append(entry)
        if dates: d['dates'] = dates

        try:
            note = contact.note()
            if note: d['note'] = str(note)
        except Exception:
            pass

        if store:
            groups = get_contact_groups(contact.identifier(), store)
            if groups: d['lists'] = groups

    return d


def emit_yaml(data):
    """Print data as YAML to stdout."""
    print(yaml.dump(data, default_flow_style=False, sort_keys=False,
                    allow_unicode=True).rstrip())

# --- Command Functions ---

def cmd_search(args):
    request_access()
    store = get_store()
    keys = get_keys_to_fetch()

    if args.list:
        group = find_group(args.list, store)
        if not group:
            print(f"Error: List '{args.list}' not found.")
            sys.exit(1)
        predicate = Contacts.CNContact.predicateForContactsInGroupWithIdentifier_(group.identifier())
        contacts, error = store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys, None)
        if error:
            print(f"Error searching list: {error.localizedDescription()}")
            sys.exit(1)

    elif args.email:
        # Efficient built-in predicate for email
        predicate = Contacts.CNContact.predicateForContactsMatchingEmailAddress_(args.email)
        contacts, error = store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys, None)
        if error:
            print(f"Search error: {error.localizedDescription()}")
            sys.exit(1)

    elif args.phone:
        q_digits = re.sub(r'\D', '', args.phone)
        if len(q_digits) < 4:
            print("Error: --phone query must contain at least 4 digits.")
            sys.exit(1)
        contacts = enumerate_contacts(store, keys, lambda c: any(
            q_digits in re.sub(r'\D', '', lv.value().stringValue())
            for lv in (c.phoneNumbers() or [])
        ))
        error = None

    elif args.city:
        q = args.city.lower()
        contacts = enumerate_contacts(store, keys, lambda c: any(
            q in (lv.value().city() or '').lower()
            for lv in (c.postalAddresses() or [])
        ))
        error = None

    elif args.country:
        q = args.country.lower()
        contacts = enumerate_contacts(store, keys, lambda c: any(
            q in (lv.value().country() or '').lower()
            for lv in (c.postalAddresses() or [])
        ))
        error = None

    elif args.query:
        # Comprehensive single-pass: name, org, note, email, phone (digits), address
        query = args.query
        q = query.lower()
        q_digits = re.sub(r'\D', '', query)

        # Fast path: try the name predicate first (CNContactStore-optimised)
        predicate = Contacts.CNContact.predicateForContactsMatchingName_(query)
        fast_contacts, _ = store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys, None)
        fast_ids = {c.identifier() for c in (fast_contacts or [])}

        def comprehensive_filter(contact):
            if contact.identifier() in fast_ids:
                return True
            note = ""
            try:
                note = contact.note() or ""
            except Exception:
                pass
            org = contact.organizationName() or ""
            if any(q in f.lower() for f in [org, note]):
                return True
            for lv in (contact.emailAddresses() or []):
                if q in str(lv.value()).lower():
                    return True
            if len(q_digits) >= 4:
                for lv in (contact.phoneNumbers() or []):
                    if q_digits in re.sub(r'\D', '', lv.value().stringValue()):
                        return True
            for lv in (contact.postalAddresses() or []):
                a = lv.value()
                addr = f"{a.street()} {a.city()} {a.state()} {a.postalCode()} {a.country()}".lower()
                if q in addr:
                    return True
            return False

        contacts = enumerate_contacts(store, keys, comprehensive_filter)
        error = None

    elif args.id:
        predicate = Contacts.CNContact.predicateForContactsWithIdentifiers_([args.id])
        contacts, error = store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys, None)
        if error:
            print(f"Search error: {error.localizedDescription()}")
            sys.exit(1)

    else:
        print("Error: Provide a query or a search flag (--id, --email, --phone, --city, --country, --list).")
        sys.exit(1)

    if not contacts:
        print("No contacts found.")
        sys.exit(1)

    emit_yaml([contact_to_dict(c, full=False) for c in contacts])


def cmd_show(args):
    request_access()
    store = get_store()
    keys = get_keys_to_fetch()

    if args.id and args.name:
        print("Error: provide either a name or --id, not both.")
        sys.exit(1)
    if not args.id and not args.name:
        print("Error: provide a contact name or --id.")
        sys.exit(1)

    if args.id:
        predicate = Contacts.CNContact.predicateForContactsWithIdentifiers_([args.id])
        label = args.id
    else:
        predicate = Contacts.CNContact.predicateForContactsMatchingName_(args.name)
        label = args.name

    contacts, error = store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys, None)
    if error or not contacts:
        print(f"Contact '{label}' not found.")
        sys.exit(1)

    contact = contacts[0]

    emit_yaml(contact_to_dict(contact, store=store, full=True))


def cmd_create(args):
    request_access()
    store = get_store()

    contact = Contacts.CNMutableContact.alloc().init()
    contact.setGivenName_(args.first_name)
    if args.last_name:    contact.setFamilyName_(args.last_name)
    if args.organization: contact.setOrganizationName_(args.organization)

    if args.email:
        contact.setEmailAddresses_([
            Contacts.CNLabeledValue.labeledValueWithLabel_value_(Contacts.CNLabelHome, e)
            for e in args.email
        ])

    if args.phone:
        contact.setPhoneNumbers_([
            Contacts.CNLabeledValue.labeledValueWithLabel_value_(
                Contacts.CNLabelHome,
                Contacts.CNPhoneNumber.phoneNumberWithStringValue_(p)
            )
            for p in args.phone
        ])

    if any([args.street, args.city, args.state, args.zip, args.country]):
        addr = Contacts.CNMutablePostalAddress.alloc().init()
        if args.street:  addr.setStreet_(args.street)
        if args.city:    addr.setCity_(args.city)
        if args.state:   addr.setState_(args.state)
        if args.zip:     addr.setPostalCode_(args.zip)
        if args.country: addr.setCountry_(args.country)
        contact.setPostalAddresses_([
            Contacts.CNLabeledValue.labeledValueWithLabel_value_(Contacts.CNLabelHome, addr)
        ])

    if args.url:
        contact.setUrlAddresses_([
            Contacts.CNLabeledValue.labeledValueWithLabel_value_(
                Contacts.CNLabelURLAddressHomePage, u)
            for u in args.url
        ])

    if args.birthday:
        contact.setBirthday_(parse_birthday(args.birthday))

    save_request = Contacts.CNSaveRequest.new()
    save_request.addContact_toContainerWithIdentifier_(contact, None)
    success, error = store.executeSaveRequest_error_(save_request, None)
    if success:
        print(f"Success: Contact '{args.first_name}' created.")
    else:
        print(f"Error creating contact: {error.localizedDescription()}")
        sys.exit(1)


def cmd_update(args):
    request_access()
    store = get_store()
    keys = get_keys_to_fetch()

    predicate = Contacts.CNContact.predicateForContactsMatchingName_(args.name)
    contacts, error = store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys, None)
    if error or not contacts:
        print(f"Contact '{args.name}' not found.")
        sys.exit(1)

    contact = contacts[0].mutableCopy()

    if args.organization: contact.setOrganizationName_(args.organization)

    if args.email:
        existing = list(contact.emailAddresses())
        for e in args.email:
            existing.append(Contacts.CNLabeledValue.labeledValueWithLabel_value_(Contacts.CNLabelHome, e))
        contact.setEmailAddresses_(existing)

    if args.phone:
        existing = list(contact.phoneNumbers())
        for p in args.phone:
            existing.append(Contacts.CNLabeledValue.labeledValueWithLabel_value_(
                Contacts.CNLabelHome,
                Contacts.CNPhoneNumber.phoneNumberWithStringValue_(p)
            ))
        contact.setPhoneNumbers_(existing)

    if any([args.street, args.city, args.state, args.zip, args.country]):
        addr = Contacts.CNMutablePostalAddress.alloc().init()
        if args.street:  addr.setStreet_(args.street)
        if args.city:    addr.setCity_(args.city)
        if args.state:   addr.setState_(args.state)
        if args.zip:     addr.setPostalCode_(args.zip)
        if args.country: addr.setCountry_(args.country)
        existing = list(contact.postalAddresses())
        existing.append(Contacts.CNLabeledValue.labeledValueWithLabel_value_(Contacts.CNLabelHome, addr))
        contact.setPostalAddresses_(existing)

    if args.url:
        existing = list(contact.urlAddresses() or [])
        for u in args.url:
            existing.append(Contacts.CNLabeledValue.labeledValueWithLabel_value_(
                Contacts.CNLabelURLAddressHomePage, u))
        contact.setUrlAddresses_(existing)

    if args.birthday:
        contact.setBirthday_(parse_birthday(args.birthday))

    save_request = Contacts.CNSaveRequest.new()
    save_request.updateContact_(contact)
    success, error = store.executeSaveRequest_error_(save_request, None)
    if success:
        print(f"Success: Contact '{args.name}' updated.")
    else:
        print(f"Error updating contact: {error.localizedDescription()}")
        sys.exit(1)


def cmd_delete(args):
    request_access()
    store = get_store()
    keys = [Contacts.CNContactGivenNameKey, Contacts.CNContactFamilyNameKey]

    predicate = Contacts.CNContact.predicateForContactsMatchingName_(args.name)
    contacts, error = store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys, None)
    if error or not contacts:
        print(f"Contact '{args.name}' not found.")
        sys.exit(1)

    if not args.force:
        ans = input(f"Are you sure you want to delete '{args.name}'? [y/N] ")
        if ans.lower() != 'y': return

    save_request = Contacts.CNSaveRequest.new()
    save_request.deleteContact_(contacts[0].mutableCopy())
    success, error = store.executeSaveRequest_error_(save_request, None)
    if success:
        print(f"Success: Contact '{args.name}' deleted.")
    else:
        print(f"Error deleting contact: {error.localizedDescription()}")
        sys.exit(1)


def cmd_add_to_list(args):
    request_access()
    store = get_store()
    keys = get_keys_to_fetch()

    predicate = Contacts.CNContact.predicateForContactsMatchingName_(args.name)
    contacts, error = store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys, None)
    if error or not contacts:
        print(f"Contact '{args.name}' not found.")
        sys.exit(1)
    contact = contacts[0]

    group = find_group(args.list, store)
    save_request = Contacts.CNSaveRequest.new()

    if not group:
        new_group = Contacts.CNMutableGroup.alloc().init()
        new_group.setName_(args.list)
        save_request.addGroup_toContainerWithIdentifier_(new_group, None)
        success, error = store.executeSaveRequest_error_(save_request, None)
        if not success:
            print(f"Error creating list: {error.localizedDescription()}")
            sys.exit(1)
        group = find_group(args.list, store)
        if not group:
            print("Critical Error: Created group but couldn't find it.")
            sys.exit(1)
        save_request = Contacts.CNSaveRequest.new()

    save_request.addMember_toGroup_(contact, group)
    success, error = store.executeSaveRequest_error_(save_request, None)
    if success:
        print(f"Success: Added '{args.name}' to list '{args.list}'.")
    else:
        print(f"Error adding to list: {error.localizedDescription()}")
        sys.exit(1)


def cmd_remove_from_list(args):
    request_access()
    store = get_store()

    if not find_group(args.list, store):
        print(f"List '{args.list}' not found.")
        sys.exit(1)

    keys = [Contacts.CNContactGivenNameKey, Contacts.CNContactFamilyNameKey]
    pred = Contacts.CNContact.predicateForContactsMatchingName_(args.name)
    candidates, error = store.unifiedContactsMatchingPredicate_keysToFetch_error_(pred, keys, None)
    if error:
        print(f"Error searching for contact: {error.localizedDescription()}")
        sys.exit(1)
    if not candidates:
        print(f"Contact '{args.name}' not found.")
        sys.exit(1)

    # CNSaveRequest.removeMember_fromGroup_ silently no-ops for iCloud-backed groups.
    # Use osascript (Contacts.app) which handles iCloud sync correctly.
    safe_name = args.name.replace('"', '\\"')
    safe_list = args.list.replace('"', '\\"')
    script = (
        f'tell application "Contacts"\n'
        f'  set theGroup to group "{safe_list}"\n'
        f'  set thePeople to (every person in theGroup whose name is "{safe_name}")\n'
        f'  repeat with p in thePeople\n'
        f'    remove p from theGroup\n'
        f'  end repeat\n'
        f'  save\n'
        f'end tell'
    )
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error removing from list: {result.stderr.strip() or result.stdout.strip()}")
        sys.exit(1)
    print(f"Success: Removed '{args.name}' from list '{args.list}'.")


def cmd_list_groups(args):
    request_access()
    store = get_store()

    all_groups, error = store.groupsMatchingPredicate_error_(None, None)
    if error:
        print(f"Error fetching lists: {error.localizedDescription()}")
        sys.exit(1)

    if not all_groups:
        print("No lists found.")
        return

    emit_yaml([str(g.name()) for g in all_groups])


def main():
    parser = argparse.ArgumentParser(
        description="A modern CLI for macOS Contacts using the Contacts framework."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = subparsers.add_parser("search", help="Search for contacts.")
    p_search.add_argument("query", nargs="?", default=None,
        help="Query searched across name, org, email, phone, and address.")
    p_search.add_argument("--list",    help="Filter to contacts in a specific list/group.")
    p_search.add_argument("--email",   help="Search by exact email address.")
    p_search.add_argument("--phone",   help="Search by phone number (digits matched fuzzily).")
    p_search.add_argument("--city",    help="Search by city.")
    p_search.add_argument("--country", help="Search by country.")
    p_search.add_argument("--id",      help="Fetch by exact CNContact identifier.")
    p_search.set_defaults(func=cmd_search)

    # show
    p_show = subparsers.add_parser("show", help="Show all details for a contact.")
    p_show.add_argument("name", nargs="?", default=None, help="Name of the contact.")
    p_show.add_argument("--id", help="CNContact identifier (from search or show output).")
    p_show.set_defaults(func=cmd_show)

    # create
    p_create = subparsers.add_parser("create", help="Create a new contact.")
    p_create.add_argument("--first-name", required=True)
    p_create.add_argument("--last-name")
    p_create.add_argument("--organization")
    p_create.add_argument("--email",   action="append")
    p_create.add_argument("--phone",   action="append")
    p_create.add_argument("--street")
    p_create.add_argument("--city")
    p_create.add_argument("--state")
    p_create.add_argument("--zip")
    p_create.add_argument("--country")
    p_create.add_argument("--url",      action="append", help="URL (repeatable).")
    p_create.add_argument("--birthday", help="Birthday as YYYY-MM-DD or --MM-DD (no year).")
    p_create.set_defaults(func=cmd_create)

    # update
    p_update = subparsers.add_parser("update", help="Update a contact.")
    p_update.add_argument("name")
    p_update.add_argument("--organization")
    p_update.add_argument("--email",   action="append")
    p_update.add_argument("--phone",   action="append")
    p_update.add_argument("--street")
    p_update.add_argument("--city")
    p_update.add_argument("--state")
    p_update.add_argument("--zip")
    p_update.add_argument("--country")
    p_update.add_argument("--url",      action="append", help="URL to append.")
    p_update.add_argument("--birthday", help="Birthday as YYYY-MM-DD or --MM-DD (replaces existing).")
    p_update.set_defaults(func=cmd_update)

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete a contact.")
    p_delete.add_argument("name")
    p_delete.add_argument("--force", action="store_true")
    p_delete.set_defaults(func=cmd_delete)

    # add_to_list
    p_add = subparsers.add_parser("add_to_list", help="Add a contact to a list.")
    p_add.add_argument("name", help="Name of the contact.")
    p_add.add_argument("list", help="Name of the list.")
    p_add.set_defaults(func=cmd_add_to_list)

    # remove_from_list
    p_remove = subparsers.add_parser("remove_from_list", help="Remove a contact from a list.")
    p_remove.add_argument("name", help="Name of the contact.")
    p_remove.add_argument("list", help="Name of the list.")
    p_remove.set_defaults(func=cmd_remove_from_list)

    # list_groups
    p_groups = subparsers.add_parser("list_groups", help="Show all lists.")
    p_groups.set_defaults(func=cmd_list_groups)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
