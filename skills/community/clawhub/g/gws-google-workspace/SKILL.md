---
name: gws
description: "Google Workspace CLI. Make sure to use this skill whenever the user mentions Gmail, email, inbox, send email, read email, check mail, draft email, send invite; Google Drive, upload file, download file, cloud storage, share file; Google Docs, create a document, write a doc; Google Calendar, schedule meeting, check schedule, view events, agenda, share calendar; Google Sheets, spreadsheet; Google Slides, make a slide, presentation; Google Forms, survey, create a form; Google Tasks, to-do, reminder; Google Meet, meeting recording; Contacts, People, address book, contact list; Classroom — or any Google Workspace / G Suite operation, even if they don't say 'gws'. If authorization fails or scope is missing, guide the user through the complete OAuth setup process."
license: MIT
homepage: https://github.com/googleworkspace/cli
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["gws", "jq", "base64", "python3"],
            "env": ["GOOGLE_WORKSPACE_PROJECT_ID", "GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"],
            "config": ["~/.config/gws/client_secret.json"]
          },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@googleworkspace/cli",
              "global": true,
              "bins": ["gws"],
              "label": "Install gws CLI (npm)",
            },
          ],
      },
  }
---

# GWS — Google Workspace CLI

Google's official Workspace CLI (`@googleworkspace/cli`). Covers Gmail, Drive, Calendar, Sheets, Docs, Slides, Forms, Tasks, People, Meet, and Classroom via Google API Discovery Service.

GitHub: https://github.com/googleworkspace/cli

## Setup

```bash
export GOOGLE_WORKSPACE_PROJECT_ID=<your-project-id>
export GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file
gws auth login          # first-time auth
gws auth login --full   # re-auth with all scopes if 403 error
```

Full setup guide: `references/setup.md`

---

## Global Patterns (ALL commands)

### `tail -n +2` before `jq`

`gws` writes `Using keyring backend: file` to stdout before JSON. Always skip it:

```bash
gws gmail users messages list --params '{"userId":"me"}' 2>/dev/null | tail -n +2 | jq '.'
```

### `--params` vs `--json`

- **`--params`**: URL/query parameters (`userId`, `id`, `q`, `maxResults`)
- **`--json`**: Request body (`removeLabelIds`, `raw`, resource JSON)

```bash
gws gmail users messages modify \
  --json '{"removeLabelIds":["UNREAD"]}' \
  --params '{"userId":"me","id":"MSG_ID"}'
```

### Email body extraction

Most emails have only HTML. Try plain text first, then strip HTML tags:

```bash
raw=$(gws gmail users messages get --params '{"userId":"me","id":"MSG_ID","format":"full"}' 2>/dev/null | tail -n +2)
body=$(echo "$raw" | jq -r '(.payload.parts[]? | select(.mimeType=="text/plain") .body.data // empty)' | head -1 | base64 -d 2>/dev/null)
if [ -z "$body" ] || [ ${#body} -lt 10 ]; then
  body=$(echo "$raw" | jq -r '(.payload.body.data // (.payload.parts[]? | select(.mimeType=="text/html") .body.data // empty))' | head -1 | base64 -d 2>/dev/null | python3 -c "import sys,re; html=sys.stdin.buffer.read().decode('utf-8',errors='ignore'); print(re.sub(r'<[^>]+>',' ',re.sub(r'<style[^>]*>.*?</style>','',html,flags=re.S)).strip()[:500])" 2>/dev/null)
fi
```

### Per-command latency (~2-3s)

Use `batchModify` (up to 1000 IDs) or shell `&` + `wait` for parallel execution.

### Discover any command

```bash
gws schema <service>          # list all methods
gws schema <service.method>   # parameter details
gws <svc> <method> --dry-run  # preview without executing
```

---

## Gmail

### Quick commands

```bash
gws gmail +triage                                                        # unread inbox summary
gws gmail +read --params '{"userId":"me","id":"MSG_ID"}'                 # read message
gws gmail +send --json '{"to":"x@y.com","subject":"Hi","body":"Text"}'   # send email
gws gmail +watch                                                         # stream new emails
```

### Common operations

```bash
# List unread
gws gmail users messages list --params '{"userId":"me","q":"is:unread","maxResults":20}'

# Read headers (match by NAME, never by array index)
gws gmail users messages get --params '{"userId":"me","id":"ID","format":"metadata","metadataHeaders":["From","Subject","Date"]}' 2>/dev/null | tail -n +2 | jq '.payload.headers | map({(.name): .value}) | add'

# Batch mark as read (up to 1000 IDs)
IDS=$(gws gmail users messages list --params '{"userId":"me","q":"is:unread","maxResults":100}' 2>/dev/null | tail -n +2 | jq -c '[.messages[].id]')
gws gmail users messages batchModify --params '{"userId":"me"}' --json "{\"ids\":$IDS,\"removeLabelIds\":[\"UNREAD\"]}"

# Send with attachment: see references/gmail.md
# Labels, threads, attachments: see references/gmail.md
```

Search syntax: `is:unread`, `from:xxx`, `subject:keyword`, `label:xxx`, `has:attachment`, `newer_than:1d`, `category:primary|social|updates`

📖 More: labels, attachments, threads, parallel batch read → `references/gmail.md`

---

## Drive

### Common operations

```bash
# List files
gws drive files list --params '{"pageSize":10,"orderBy":"modifiedTime desc"}'
gws drive files list --params '{"q":"mimeType=\"application/vnd.google-apps.spreadsheet\""}'

# Upload (two-step: upload → rename, because files create ignores name)
cd ~/Downloads
gws drive files create --params '{}' --upload file.pdf --upload-content-type application/pdf
FILE_ID=$(gws drive files create --params '{}' --upload file.pdf --upload-content-type application/pdf 2>/dev/null | tail -n +2 | jq -r '.id')
gws drive files update --params "{\"fileId\":\"$FILE_ID\"}" --json '{"name":"file.pdf"}'

# Create folder
gws drive files create --params '{}' --json '{"name":"Folder","mimeType":"application/vnd.google-apps.folder"}'

# Download / Export
gws drive files get --params '{"fileId":"ID","alt":"media"}' --output file.txt
gws drive files export --params '{"fileId":"ID","mimeType":"application/pdf"}' --output doc.pdf
```

⚠️ `--upload` and `--output` only accept relative paths. `cd` to the directory first.
⚠️ `files delete` returns a `saved_file` field — ignore it.

📖 More: copy/move, permissions, storage → `references/drive.md`

---

## Calendar

All time parameters use RFC 3339 format.

```bash
# List events
gws calendar events list --params '{"calendarId":"primary","timeMin":"TODAY_START","timeMax":"TODAY_END","maxResults":20}'

# Create event
gws calendar events insert --json '{"summary":"Meeting","start":{"dateTime":"START_TIME","timeZone":"TIMEZONE"},"end":{"dateTime":"END_TIME","timeZone":"TIMEZONE"}}' --params '{"calendarId":"primary"}'

# Free/busy
gws calendar freebusy query --json '{"timeMin":"START","timeMax":"END","items":[{"id":"primary"}]}'
```

📖 More: update/delete events, ACL, calendar management → `references/calendar.md`

---

## Sheets

```bash
# Read
gws sheets spreadsheets values get --params '{"spreadsheetId":"ID","range":"Sheet1!A1:B10"}'

# Write values (RAW)
gws sheets spreadsheets values update --params '{"spreadsheetId":"ID","range":"Sheet1!A1","valueInputOption":"RAW"}' --json '{"values":[["Value"]]}'

# Write formulas (must use USER_ENTERED)
gws sheets spreadsheets values update --params '{"spreadsheetId":"ID","range":"Sheet1!C1","valueInputOption":"USER_ENTERED"}' --json '{"values":[["=SUM(A1:B10)"]]}'

# Append rows
gws sheets spreadsheets values append --params '{"spreadsheetId":"ID","range":"Sheet1!A1","valueInputOption":"RAW"}' --json '{"values":[["col1","col2"]]}'
```

📖 More: row/column ops, formatting, conditional formatting → `references/sheets.md`

---

## Docs

```bash
DOC_ID=$(gws docs documents create --json '{"title":"My Doc"}' --params '{}' 2>/dev/null | tail -n +2 | jq -r '.documentId')
gws docs documents get --params '{"documentId":"ID"}' 2>/dev/null | tail -n +2 | jq '[.body.content[]|select(.paragraph)|.paragraph.elements[]?|select(.textRun)|.textRun.content]|join("")'
gws docs documents batchUpdate --json '{"requests":[{"insertText":{"location":{"index":1},"text":"Hello\n"}}]}' --params '{"documentId":"ID"}'
```

📖 More: bold, headings, images, bullet lists → `references/docs-slides-forms.md`

---

## Slides

Coordinates use EMU units (1 inch = 914400 EMU).

```bash
# Create presentation
SLIDE_ID=$(gws slides presentations create --json '{"title":"My Slides"}' --params '{}' 2>/dev/null | tail -n +2 | jq -r '.presentationId')

# Add text box
gws slides presentations batchUpdate --json '{"requests":[{"createShape":{"objectId":"s1","shapeType":"TEXT_BOX","elementProperties":{"pageObjectId":"p1","size":{"width":{"magnitude":4000000,"unit":"EMU"},"height":{"magnitude":300000,"unit":"EMU"}},"transform":{"scaleX":1,"scaleY":1,"translateX":100000,"translateY":100000,"unit":"EMU"}}}},{"insertText":{"objectId":"s1","text":"Hello!"}}]}' --params '{"presentationId":"ID"}'

# Add new slide
gws slides presentations batchUpdate --json '{"requests":[{"createSlide":{"objectId":"slide2"}}]}' --params '{"presentationId":"ID"}'

# Insert image
gws slides presentations batchUpdate --json '{"requests":[{"createImage":{"url":"https://example.com/img.png","elementProperties":{"pageObjectId":"p1","size":{"width":{"magnitude":3000000,"unit":"EMU"},"height":{"magnitude":2000000,"unit":"EMU"}}}}}]}' --params '{"presentationId":"ID"}'
```

📖 More → `references/docs-slides-forms.md`

## Forms

```bash
# Create form
FORM_ID=$(gws forms forms create --json '{"info":{"title":"Survey"}}' --params '{}' 2>/dev/null | tail -n +2 | jq -r '.formId')

# Add question (text)
gws forms forms batchUpdate --json '{"requests":[{"createItem":{"location":{"index":0},"item":{"title":"Your name?","questionItem":{"question":{"required":true,"textQuestion":{}}}}}}]}' --params '{"formId":"ID"}'

# Add question (radio / checkbox / dropdown / date / scale)
gws forms forms batchUpdate --json '{"requests":[{"createItem":{"location":{"index":1},"item":{"title":"Rate 1-5","questionItem":{"question":{"required":true,"scaleQuestion":{"low":1,"high":5}}}}}}]}' --params '{"formId":"ID"}'

# View responses
gws forms forms responses list --params '{"formId":"ID"}'
```

📖 More question types → `references/docs-slides-forms.md`

## Tasks

```bash
gws tasks tasklists list 2>/dev/null | tail -n +2 | jq '.items[]|{title,id}'
gws tasks tasks list --params '{"tasklist":"@default"}'
gws tasks tasks insert --json '{"title":"Task","notes":"Desc"}' --params '{"tasklist":"@default"}'
gws tasks tasks patch --params '{"tasklist":"@default","task":"TASK_ID"}' --json '{"status":"completed"}'
gws tasks tasks delete --params '{"tasklist":"@default","task":"TASK_ID"}'
```

📖 More → `references/tasks-people-other.md`

## People / Contacts

`searchContacts` requires `readMask` — omitting causes 400 error.

```bash
gws people people get --params '{"resourceName":"people/me","personFields":"names,emailAddresses"}'
gws people people searchContacts --params '{"query":"john","pageSize":10,"readMask":"names,emailAddresses,phoneNumbers"}'
gws people connections list --params '{"resourceName":"people/me","personFields":"names,emailAddresses","pageSize":10}'
gws people people createContact --json '{"names":[{"givenName":"First","familyName":"Last"}],"emailAddresses":[{"value":"e@example.com"}]}' --params '{"readMask":"names,emailAddresses"}'
gws people contactGroups list --params '{"pageSize":10}'
```

📖 More → `references/tasks-people-other.md`

## Meet / Classroom

```bash
gws meet conferenceRecords list --params '{"pageSize":10}'
gws classroom courses list --params '{"pageSize":10}'
gws classroom courses students list --params '{"courseId":"COURSE_ID"}'
gws classroom courses courseWork list --params '{"courseId":"COURSE_ID"}'
```

📖 More → `references/tasks-people-other.md`

---

## Workflow Helpers

```bash
gws workflow +standup-report                   # today's meetings + tasks
gws workflow +meeting-prep                     # next meeting prep
gws workflow +weekly-digest                    # weekly meetings + unread count
gws workflow +email-to-task --message-id "ID"  # Gmail → Tasks
```

---

## Can't find the right command?

1. **Discover all methods for a service:** `gws schema <service>` (e.g. `gws schema drive`, `gws schema gmail`)
2. **Get parameter details:** `gws schema <service.method>` (e.g. `gws schema drive.files.copy`)
3. **Dry-run to preview:** `gws <svc> <method> --dry-run`
4. **Check references/** for detailed examples per service
5. **Official docs:** https://github.com/googleworkspace/cli

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 403 Insufficient scopes | `gws auth login --full` |
| No OAuth client | Check `~/.config/gws/client_secret.json` |
| API not enabled | Enable in GCP Console → APIs & Services |
| jq parse error | Add `tail -n +2` to skip keyring prefix |
| Upload shows "Untitled" | Rename with `files update` after upload |
| File not found on upload | Use relative paths, `cd` first |
