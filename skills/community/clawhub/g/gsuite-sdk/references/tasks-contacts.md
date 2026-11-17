# Tasks and Contacts

Not in the default login. Enable the **Google Tasks API** / **People API** in
the Cloud project and log in with their scopes:

```bash
gsuite auth login --force --scopes default,tasks,contacts
```

Without them, calls fail with `PermissionDeniedError`.

## Tasks

`Tasks(auth, tasklist_id="@default")` from `gsuite_tasks`. Methods take an
optional `tasklist_id`; the default is the user's main list.

```python
from datetime import date

from gsuite_core import GoogleAuth
from gsuite_tasks import Tasks

auth = GoogleAuth()
tasks = Tasks(auth)

for tl in tasks.list_tasklists():
    print(tl.id, tl.title)

pending = tasks.list_tasks(show_completed=False, due_max=date(2026, 3, 31))
for t in pending:
    print(t.id, t.title, t.due, "OVERDUE" if t.is_overdue else "")

task = tasks.create_task("Pay rent", due=date(2026, 3, 1), notes="Before the 5th")
tasks.create_task("Transfer", parent=task.id)        # subtask
tasks.update_task(task.id, due=None)                 # None clears a field
tasks.complete_task(task.id)
tasks.reopen_task(task.id)
tasks.move_task(task.id, previous="OTHER_TASK_ID")
tasks.delete_task(task.id)                           # False if it didn't exist
tasks.clear_completed()                              # hide completed tasks

work = tasks.create_tasklist("Work")
tasks.create_task("Prepare demo", tasklist_id=work.id)
```

`due` is a `date`: the Tasks API keeps only the day.

## Contacts

`Contacts(auth)` from `gsuite_contacts` (People API). IDs are `c123` or
`people/c123`.

```python
from gsuite_contacts import Contacts

contacts = Contacts(auth)

matches = contacts.search("ana", max_results=30)     # prefix of name, email, phone or company; max 30
for c in matches:
    print(c.id, c.display_name, c.email, c.phone, c.organization)

everyone = contacts.list_contacts(sort_order="FIRST_NAME_ASCENDING")
contact = contacts.get("c123")                       # None if it doesn't exist

ana = contacts.create(given_name="Ana", family_name="Pérez", emails=["ana@example.com"])
contacts.update(ana.id, phones=["+54 11 5555-5555"])  # lists replace the old values
contacts.update(ana.id, given_name="Anita")            # keeps the family name
contacts.delete(ana.id)
```

`update` raises `NotFoundError` for a missing contact and refuses to
overwrite a concurrent change (etag).

Groups (labels) and keeping a local copy in sync:

```python
for group in contacts.list_groups():               # system groups have group.is_system
    print(group.id, group.name, group.member_count)
work = contacts.create_group("Work")
contacts.modify_group(work.id, add=["c123"], remove=["c456"])  # returns the IDs Google skipped
members = contacts.get_many(contacts.group_members(work.id))
contacts.delete_group(work.id)                     # its contacts stay

delta = contacts.sync()                            # first time: every contact
delta = contacts.sync(delta.sync_token)            # later: delta.changed, delta.deleted
```

`sync` raises `SyncTokenExpiredError` when the token is too old (about a week):
call it again without one.

Callers that build People API bodies themselves: `contacts.create(raw_fields=body)`
and `contacts.update_raw(contact_id, body, ["names", "urls"])` (the body carries
its `etag`; nothing is read first).

## CLI

```bash
gsuite tasks lists -o json
gsuite tasks list -o json                          # pending; --all includes completed
gsuite tasks list --list LIST_ID --due-before 2026-03-31 -o json
gsuite tasks add "Pay rent" --due 2026-03-01 --notes "Before the 5th"
gsuite tasks add "Transfer" --parent TASK_ID
gsuite tasks done TASK_ID
gsuite tasks reopen TASK_ID
gsuite tasks delete TASK_ID
gsuite tasks clear

gsuite contacts search ana -o json
gsuite contacts list --limit 200 -o json
gsuite contacts show CONTACT_ID -o json
gsuite contacts add --given Ana --family Pérez --email ana@example.com --phone "+54 11 5555-5555"
gsuite contacts delete CONTACT_ID --yes
gsuite contacts groups list -o json
gsuite contacts groups create Work
gsuite contacts groups members GROUP_ID -o json
gsuite contacts groups add GROUP_ID CONTACT_ID CONTACT_ID
gsuite contacts groups remove GROUP_ID CONTACT_ID
gsuite contacts groups delete GROUP_ID --yes
```
