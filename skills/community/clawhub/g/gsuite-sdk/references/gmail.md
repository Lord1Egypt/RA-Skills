# Gmail

`Gmail(auth)` from `gsuite_gmail`. Needs the default login scopes.

## Reading

```python
from gsuite_core import GoogleAuth
from gsuite_gmail import Gmail, query

auth = GoogleAuth()
gmail = Gmail(auth)

unread = gmail.get_unread(max_results=10)
found = gmail.search("from:billing@example.com has:attachment newer_than:30d", max_results=50)
found = gmail.search(query.from_("billing@example.com") & query.has_attachment() & query.newer_than(days=30))

msg = gmail.get_message("MESSAGE_ID")       # None if it doesn't exist
if msg is not None:
    print(msg.subject, msg.sender, msg.recipient, msg.cc, msg.date)
    print(msg.body)                          # plain text, else HTML
    for attachment in msg.attachments:
        attachment.save("/tmp/")             # or attachment.download() -> bytes
```

`query` builders: `from_`, `to`, `subject`, `has_words`, `label`, `filename`,
`has_attachment`, `is_unread`, `is_read`, `is_starred`, `is_important`,
`in_inbox`, `in_sent`, `in_drafts`, `in_spam`, `in_trash`,
`newer_than(days=, months=)`, `older_than(...)`, `after("2026/01/31")`,
`before(...)`, `size_larger`, `size_smaller`, `category`, `raw`. Combine with
`&` (and) and `|` (or).

Threads: `gmail.get_thread(thread_id)` (or `None`) has `messages`,
`subject`, `participants`, `message_count`, `has_unread`.
`get_thread(..., format="metadata", headers=["From", "To", "Subject", "Date"])`
skips the bodies.

Keeping a local copy in sync (IDs only, then what changed):

```python
start = gmail.get_history_id()                        # after the first full import
ids = list(gmail.iter_message_ids("newer_than:30d"))  # no message is fetched
delta = gmail.history(start)                          # .added, .deleted, .labels_changed
start = delta.history_id
```

`history` raises `SyncTokenExpiredError` when the ID is older than about a
week: list again and start over from `get_history_id()`.

`list_message_ids(query, page_token=...)` returns one page and its
`next_page_token`, to stop a long listing and resume it later.
`delta.added_labels` maps each added message to its label IDs, and
`message.raw` / `thread.raw` hold the API resource as fetched.

## Sending and replying

```python
gmail.send(
    to=["ana@example.com"],
    subject="Monthly report",
    body="<p>Attached.</p>",
    html=True,
    cc=["boss@example.com"],
    attachments=["report.pdf"],        # paths or (filename, bytes) tuples
)

msg.reply("Thanks, received.")                 # keeps the thread
msg.reply("Adding everyone.", reply_all=True)
msg.forward(["ana@example.com"], body="FYI")   # attachments included by default
```

`gmail.reply(message, body, ...)` and `gmail.forward(message, to, ...)` do the
same from the client.

## Drafts

```python
draft = gmail.create_draft(to=["ana@example.com"], subject="Draft", body="Check this first")
gmail.send_draft(draft.id)
drafts = gmail.list_drafts()
```

## Organizing

```python
msg.mark_as_read()
msg.star()
msg.archive()
msg.add_label("Invoices")
msg.trash()

labels = gmail.get_labels()                    # .name, .messages_unread
gmail.create_label("Invoices")
gmail.batch_modify(["ID1", "ID2"], add_labels=["Invoices"], remove_labels=["UNREAD"])
```

## CLI

```bash
gsuite gmail list --unread --limit 20 -o json
gsuite gmail list --from billing@example.com -o json
gsuite gmail read MESSAGE_ID -o json            # -o text | json | html
gsuite gmail read MESSAGE_ID --mark-read
gsuite gmail send --to ana@example.com --cc boss@example.com --subject "Hi" --body "Hello" --attach notes.pdf
gsuite gmail reply MESSAGE_ID --body "Thanks!" --all
gsuite gmail mark MESSAGE_ID --read --star
gsuite gmail archive MESSAGE_ID
gsuite gmail trash MESSAGE_ID
gsuite gmail labels
gsuite gmail profile
```

`gsuite gmail send --body` can be omitted to read the body from stdin.
