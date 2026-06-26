---
name: mac-contacts
description: >
  CLI for reading and managing macOS Contacts (CNContactStore). Supports
  searching by name, email, phone number, city, or country; showing all
  fields for a contact including list membership; creating and updating
  contacts with name, org, phone, email, and postal address; deleting
  contacts; and managing group (list) membership. Use when asked to look up,
  add, edit, remove, or organise contacts on macOS, or when you need a
  contact's phone number, email, address, or which lists they belong to.
compatibility: >
  Requires macOS with Contacts access granted to Terminal/your agent host.
  Requires Python 3, pyobjc-framework-Contacts, and PyYAML
  (pip install pyobjc-framework-Contacts pyyaml).
metadata:
  author: bdwelle
---

# mac-contacts

macOS Contacts CLI backed by `CNContactStore`. All reads use unified contact
views (iCloud + local + Exchange merged). All writes are atomic via
`CNSaveRequest`. Group membership removal uses `osascript` to work around a
silent no-op in `CNSaveRequest.removeMember_fromGroup_` for iCloud-backed
groups.

## Dependencies

```bash
pip install pyobjc-framework-Contacts
```

```bash
pip install pyyaml
```

Grant Contacts access to Terminal (or your agent host) when prompted on first
run, or via **System Settings → Privacy & Security → Contacts**.

## Invocation

```bash
python3 skill://mac-contacts/scripts/mac-contacts.py <subcommand> [options]
```

All examples below use `mac-contacts` as shorthand for the full invocation.

---

## Subcommands

### search

Search contacts. With a positional query, performs a single-pass search
across **name, organisation, note, email, phone** (digits normalised), and
**postal address** fields. Use explicit flags to restrict to a specific field.

```
search [QUERY]
       [--list LIST]
       [--email EMAIL]
       [--phone PHONE]
       [--city CITY]
       [--country COUNTRY]
```

| Flag | Description |
|------|-------------|
| `QUERY` | Comprehensive search across all fields. Phone digits are matched fuzzily (query digits must appear in contact's digit-stripped number; minimum 4 digits required for phone matching). |
| `--list LIST` | Return only contacts that are members of the named list/group. |
| `--email EMAIL` | Match by email address (uses the CNContact native email predicate — efficient). |
| `--phone PHONE` | Match by phone number; non-digit characters stripped before comparison. Minimum 4 digits. |
| `--city CITY` | Match by city in any postal address. |
| `--country COUNTRY` | Match by country in any postal address. |

**Examples:**

```bash
# Comprehensive — finds by name, org, email, phone, address
mac-contacts search "John"
mac-contacts search "john@example.com"   # auto-matches email
mac-contacts search "415-555"            # auto-matches phone (≥4 digits)
mac-contacts search "San Francisco"      # auto-matches city

# Explicit field targeting
mac-contacts search --email "john@acme.com"
mac-contacts search --phone "415"        # error: fewer than 4 digits
mac-contacts search --phone "4155551234"
mac-contacts search --city "London"
mac-contacts search --country "Germany"

# Filter to list members
mac-contacts search --list "Work"
```

Output per contact: name, organisation, phone(s), email(s), address(es).

---

### show

Show every available field for a contact, including list membership.

```
show NAME
```

Output includes: full name (with prefix/middle/suffix), nickname,
organisation, job title, department, phones, emails, postal addresses,
URLs, social profiles, birthday, dates, note (if readable), and **Lists**.

```bash
mac-contacts show "Jane Doe"
mac-contacts show "Apple"        # matches any contact whose name contains "Apple"
```

> **Note:** If multiple contacts match `NAME`, only the first result is shown.

---

### create

Create a new contact. All flags except `--first-name` are optional.

```
create --first-name NAME
       [--last-name NAME]
       [--organization ORG]
       [--email EMAIL]     (repeatable)
       [--phone PHONE]     (repeatable)
       [--street STREET]
       [--city CITY]
       [--state STATE]
       [--zip ZIP]
       [--country COUNTRY]
       [--url URL]         (repeatable)
       [--birthday DATE]
```

```bash
mac-contacts create --first-name "Jane" --last-name "Doe" \
    --organization "Acme" \
    --email "jane@acme.com" --email "jane.personal@gmail.com" \
    --phone "415-555-0100" \
    --street "123 Main St" --city "San Francisco" \
    --state "CA" --zip "94102" --country "United States" \
    --url "https://jane.acme.com" \
    --birthday "1985-03-22"
```

> **Note:** The `--note` flag is intentionally absent. Writing contact notes
> requires the `com.apple.developer.contacts.notes` entitlement, which
> Terminal-based tools do not hold.

> **`--birthday` format:** `YYYY-MM-DD` for a full date (e.g. `1985-03-22`),
> or `--MM-DD` to store month/day without a year (e.g. `--03-22`).

---

### update

Update fields on an existing contact. Phone and email values are **appended**
to existing values (not replaced). A new postal address block is appended if
any address flag is provided.

```
update NAME
       [--organization ORG]
       [--email EMAIL]     (repeatable, appends)
       [--phone PHONE]     (repeatable, appends)
       [--street STREET]
       [--city CITY]
       [--state STATE]
       [--zip ZIP]
       [--country COUNTRY]
       [--url URL]         (repeatable, appends)
       [--birthday DATE]   (replaces existing)
```

```bash
mac-contacts update "Jane Doe" --phone "415-555-0199"
mac-contacts update "Jane Doe" --organization "New Corp" --city "Oakland"
mac-contacts update "Jane Doe" --birthday "1985-03-22"
mac-contacts update "Jane Doe" --url "https://jane.dev"
```

---

### delete

Delete a contact. Prompts for confirmation unless `--force` is given.

```
delete NAME [--force]
```

```bash
mac-contacts delete "Jane Doe"           # prompts y/N
mac-contacts delete "Jane Doe" --force   # no prompt
```

---

### add_to_list

Add a contact to a named list (CNGroup). Creates the list if it does not
exist.

```
add_to_list NAME LIST
```

```bash
mac-contacts add_to_list "Jane Doe" "Work"
```

---

### remove_from_list

Remove a contact from a named list.

```
remove_from_list NAME LIST
```

```bash
mac-contacts remove_from_list "Jane Doe" "Work"
```

> **Implementation note:** Uses `osascript` (Contacts.app) because
> `CNSaveRequest.removeMember_fromGroup_` silently no-ops for iCloud-backed
> groups.

---

### list_groups

List all contact groups (lists) in the store.

```
list_groups
```

```bash
mac-contacts list_groups
```

---

## Output conventions

- `search`, `show`, and `list_groups` emit **YAML** (requires `pyyaml`).
  `search` and `list_groups` return a YAML list; `show` returns a single YAML mapping.
  Parse with `python3 -c "import sys,yaml; print(yaml.safe_load(sys.stdin))"` or `yq`.
- Success messages begin with `Success:`.
- Error messages begin with `Error:` or `[FATAL]`.
- `search` and `list_groups` exit with code 1 when no results are found.
- All other commands exit 1 on any failure.

## Known limitations

- **Notes (write):** Setting a contact note requires the
  `com.apple.developer.contacts.notes` entitlement. `create` and `update`
  do not expose `--note` for this reason. Existing notes on contacts are
  readable via `show`.
- **`update` replaces nothing:** Phone, email, and address values are always
  appended, never replaced. To change a value, delete and recreate the
  contact, or edit via Contacts.app.
- **`show` NAME matching:** Uses `CNContact.predicateForContactsMatchingName_`
  which matches substrings across name fields. If ambiguous, the first result
  is returned.
