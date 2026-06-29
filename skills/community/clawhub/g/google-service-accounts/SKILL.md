---
name: google-service-accounts
description: Read or write a user's Google Sheets, Docs, Drive, or Calendar from code via a Google service account — headless, no OAuth browser flow. Use when handed a credentials.json or CREDS_JSON, or when the user wants to set one up (including walking them through the free signup, which needs only a basic Google account).
---

# Google service accounts

A service account is a Google account for a script: it has an email, logs in with a key file, and
reaches any Doc / Sheet / Drive file / Calendar **that's been shared with its email** — exactly like
sharing with a coworker. No browser consent, no human clicking "Allow," no token to refresh.

## 1. Do you already have a key?

Look for `credentials.json` in the working directory, or a `CREDS_JSON` env var holding the JSON. The
service account's address is the `client_email` field inside it
(`name@project.iam.gserviceaccount.com`). If you have it, skip to **3**.

## 2. No key yet — walk the human through setup

Tell them plainly: **this is free and needs nothing but a basic Google account.** A personal
`gmail.com` works — no credit card, no billing account. Creating the project, the service account,
and the key all cost nothing, and the Sheets / Docs / Drive / Calendar APIs are free within generous
daily quotas. The setup is one-time and takes a few minutes.

If they have the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install), hand them this to run:

```bash
gcloud auth login
PROJECT="agent-bot-$(date +%s)"
gcloud projects create "$PROJECT"
gcloud config set project "$PROJECT"
gcloud services enable sheets.googleapis.com drive.googleapis.com \
  docs.googleapis.com calendar-json.googleapis.com
gcloud iam service-accounts create agent-bot --display-name="Agent Bot"
SA="agent-bot@${PROJECT}.iam.gserviceaccount.com"
gcloud iam service-accounts keys create credentials.json --iam-account="$SA"
echo "Now share your file/calendar with: $SA"
```

No CLI? Point them at the console walkthrough in `README.md` ("Click through the console") — about
20 clicks, still free. Either path ends the same: a `credentials.json` file and a `client_email`.

## 3. The one rule: share the file

The service account starts with access to **nothing.** For every file you need to touch, the human
must open it → **Share** → paste the `client_email` → **Editor** (or **Viewer** for read-only) →
Send. For a calendar: its settings → *Share with specific people*.

**If you get `SpreadsheetNotFound` or `403 PERMISSION_DENIED`, it's almost never a code bug — the
file isn't shared.** Tell the human *exactly which file and which `client_email`* so they fix it in
one click. Don't retry blindly.

## 4. Use the key

Runnable examples live in `quickstart.py` (`python quickstart.py sheets|docs|calendar`). The core
patterns:

**Sheets** (via `gspread`, the friendly wrapper — its default scopes include `drive`, so `open()` by
name works):

```python
import gspread
gc = gspread.service_account(filename="credentials.json")
sh = gc.open("My Spreadsheet")                 # only works because it's shared with the SA
sh.sheet1.update(values=[["hello", "from a robot"]])
sh.sheet1.append_row(["logged", "by agent"])   # the most common agent move
```

**Any other API** (Docs, Calendar, Drive, …) via `google-api-python-client` — one credentials object
drives all of them; only the scope list changes:

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    "credentials.json", scopes=["https://www.googleapis.com/auth/documents"])
docs = build("docs", "v1", credentials=creds)
```

In a container or CI, load the key from an env var instead of a file:

```python
import os, json, gspread
gc = gspread.service_account_from_dict(json.loads(os.environ["CREDS_JSON"]))
```

## 5. Boundaries — don't route around these

- Request the **least** scope you need; add `.readonly` unless you're writing. **Read a document
  before you edit it.**
- A service account **cannot** read the human's private Gmail, personal Calendar, or whole Drive —
  only what's explicitly shared with it. That data needs the human's *own* OAuth browser consent;
  don't try to substitute the service account for it.
- Calendar: a shared calendar's id is its **owner's email** (`calendarId="primary"` is the robot's
  own empty calendar), and a service account **cannot add attendees** to an event — Google rejects
  it with `forbiddenForServiceAccounts`. Create/edit/delete events freely; never try to send invites.
- The service account's email is an identity, not a mailbox — mail sent to it bounces. It can't sign
  up for services or receive confirmation links.
- Treat `credentials.json` as a password: anyone holding it *is* the service account. Never commit
  it or paste it anywhere shared.

See `README.md` for the full explainer — why this beats standing up your own OAuth app, the free-tier
details, scope reference, and troubleshooting.
