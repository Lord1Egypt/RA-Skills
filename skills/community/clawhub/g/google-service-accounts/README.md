# awesome-google-service-accounts

A Google **service account** is a Google account for a script instead of a person. It's how you let a
program — or an AI agent — read and write your Google Docs, Sheets, Drive, or Calendar without a
browser popup, a "click to authorize" screen, or a refresh-token dance: you make an account for a
robot, download its key, and share a file with it the way you'd share with a coworker.

Most people never reach for this. The usual way to give a program access to your Google data is
through an *app* — you either trust someone else's app with your account, or stand up your own Google
Cloud app (consent screen, OAuth client, verification) just to authorize yourself. That app
machinery is built for serving *other people's* logins; using it to let your own agent touch your own
documents is a lot of plumbing for a one-person job. A service account skips the app entirely — it's
an identity you share a document *to*, like adding a coworker. You're just sharing your own file with
your own agent.

This repo is an explainer for that, with runnable examples. It walks through what a service account
is, how to set one up, what it can and can't reach, and how to drive the key from Python — written
for both the person doing the setup and an agent that's been handed a key. It also ships as an
installable agent skill — see [`SKILL.md`](SKILL.md).

---

## A service account is a robot with an email — you share files with it

Three things define it:

- It has an email — `my-bot@my-project.iam.gserviceaccount.com` — just like you have one.
- It logs in with a **key file** instead of a password.
- It starts with access to **nothing.** You grant access to a specific file by hitting **Share**
  and pasting its email, exactly like sharing with a person.

That last point is the trick the whole thing rests on, and the one every other tutorial buries in a
footnote. **If your code can't see a file, you forgot to share the file with the robot's email.**
Memorize that; it's 90% of the errors you'll hit.

### For an agent, the win is that nobody has to click "Allow"

OAuth — the "Sign in with Google → allow access?" flow — exists to let an app borrow **a human's**
identity, so a human has to be there to click "Allow." An autonomous agent isn't. A service account
is its *own* identity: headless, no consent screen, no token expiry to babysit — exactly what you
want for a bot that runs at 3am.

---

## It's free on a personal gmail account — no credit card needed

**A free, personal `gmail.com` account works — no credit card, no billing account.** Creating a
project, a service account, and a JSON key are free, and the Sheets / Docs / Drive / Calendar APIs
are *"available at no additional cost"* within generous daily quotas (e.g. Sheets allows 300 reads +
300 writes/min; Calendar 1M queries/day). You do **not** have to link a billing account the way other
Google Cloud products (Compute Engine, Maps, BigQuery) require.

<sub>Honest caveat: Google has announced that *opt-in* quota overages above the free daily limits
*"are planned to incur charges later in 2026,"* with at least 90 days' notice. Normal usage under the
limit stays free and unbilled. You won't be charged by accident — billing only applies if you
deliberately request a paid quota increase.</sub>

## Six gcloud commands take you from zero to a key file

If you have the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install), the entire setup is
scriptable. This is the fastest zero-to-key path:

```bash
gcloud auth login                                  # one-time, opens a browser

PROJECT="sheet-bot-$(date +%s)"
gcloud projects create "$PROJECT"
gcloud config set project "$PROJECT"

gcloud services enable sheets.googleapis.com drive.googleapis.com \
  docs.googleapis.com calendar-json.googleapis.com

gcloud iam service-accounts create sheet-bot --display-name="Sheet Bot"
SA="sheet-bot@${PROJECT}.iam.gserviceaccount.com"
gcloud iam service-accounts keys create credentials.json --iam-account="$SA"

echo "Now share your Sheet/Doc with: $SA"
```

The one thing `gcloud` can't do is share the file — that's a Drive action. Open your Sheet → **Share**
→ paste the email it printed → Send. Then `python quickstart.py sheets "My Spreadsheet"`.

## No terminal? Click through the console in about 20 steps

Never opened Google Cloud Console before? It's about 20–30 clicks. None of it costs anything.

1. **Create or pick a project** at [console.cloud.google.com](https://console.cloud.google.com).
   *First visit only:* pick your country and accept the Terms of Service. Everything you do is scoped
   to the **project** selected in the top-bar dropdown. (Personal accounts have *no organization* —
   that's normal, not an error.)
2. **Enable the APIs** you'll use — [Sheets](https://console.cloud.google.com/apis/library/sheets.googleapis.com),
   [Docs](https://console.cloud.google.com/apis/library/docs.googleapis.com),
   [Drive](https://console.cloud.google.com/apis/library/drive.googleapis.com),
   [Calendar](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com).
   Each is enabled separately. (Opening a Sheet *by name* needs the Drive API too — Sheets are Drive
   files.) After clicking **Enable**, give it a minute to propagate before your first call.
3. **Create the service account:** *APIs & Services → Credentials → Create Credentials → **Service
   account**.* Name it after the job (`sheet-bot`). Skip the optional roles — for Workspace files,
   *sharing* grants access, not IAM roles.
   > That menu offers three things; pick the right one. **API key** = public data only, can't touch
   > private files. **OAuth client ID** = acts as *a human* with a browser consent screen.
   > **Service account** = the robot identity you want here.
4. **Make a key:** open the service account → **Keys** tab → *Add key → Create new key → JSON →
   Create.* It downloads **once** and can't be re-downloaded. This is your `credentials.json`.
5. **Copy the robot's email** — it's the `client_email` field inside that JSON (or shown in the
   console). Looks like `sheet-bot@my-project.iam.gserviceaccount.com`.
6. **Share your file with it.** Open your Sheet/Doc/Drive folder → **Share** → paste the email → pick
   **Editor** or **Viewer** → Send. Done.

> The whole concept in one screenshot: the Google **Share** dialog with a `…gserviceaccount.com`
> address typed into it.

---

## Sheets in five lines

```python
import gspread
gc = gspread.service_account(filename="credentials.json")
sh = gc.open("My Spreadsheet")          # works ONLY because you shared it in step 6
print(sh.worksheet("Sheet1").get_all_values())
sh.worksheet("Sheet1").update(values=[["hello", "from a robot"]])
```

`gspread` is the friendly wrapper for the Sheets case. By default it requests the `spreadsheets` +
`drive` scopes, which is why `gc.open("by name")` can find the file.

**The #1 error:** `gspread.exceptions.SpreadsheetNotFound` (or a `403 PERMISSION_DENIED`) almost
always means **the file isn't shared with the service account's email.** Not a code bug. Go share it.

The most common agent move is *appending a row* — a bot logging what it did to a shared sheet:

```python
sh.sheet1.append_row(["2026-07-01 10:00", "agent-7", "summarized inbox", "ok"])
```

You can even have the robot share files itself, since it has edit access to the ones you shared with it:

```python
sh.share("teammate@example.com", perm_type="user", role="writer")
```

---

## The same key reaches every Google API, not just Sheets

`gspread` is just a convenience. The general pattern is **one credentials object → every Google
API**, via `google-api-python-client`. The same key drives Docs, Calendar, Drive, Gmail, and the
rest.

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    "credentials.json",
    scopes=["https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/calendar"])

docs     = build("docs",     "v1", credentials=creds)
calendar = build("calendar", "v3", credentials=creds)
```

**Docs** — read a document, then insert text at the top. Note the look-before-you-leap check: an
agent editing a *live* document should confirm what it's editing before it mutates anything.

```python
DOC_ID = "1RRCTvA_...your_doc_id..."

doc = docs.documents().get(documentId=DOC_ID).execute()
first = doc["body"]["content"][1]["paragraph"]["elements"][0]["textRun"]["content"]
assert first.startswith("Draft"), f"unexpected doc start, aborting: {first!r}"

docs.documents().batchUpdate(documentId=DOC_ID, body={"requests": [
    {"insertText": {"location": {"index": 1}, "text": "Edited by a robot.\n"}}
]}).execute()
```

**Calendar** — list and create events. (You share a *calendar* with the robot's email under that
calendar's settings → *Share with specific people* — same idea as sharing a file. Sharing covers
every event on the calendar, past and future; there is no per-event sharing to manage.)

```python
events = calendar.events().list(calendarId="you@gmail.com", maxResults=10).execute()
for e in events.get("items", []):
    print(e["start"].get("dateTime", e["start"].get("date")), e.get("summary"))

calendar.events().insert(calendarId="you@gmail.com", body={
    "summary": "Created by a robot",
    "start": {"dateTime": "2026-07-01T10:00:00-04:00"},
    "end":   {"dateTime": "2026-07-01T10:30:00-04:00"},
}).execute()
```

Two calendar-specific gotchas. First, the id of a shared calendar is its **owner's email** —
`calendarId="primary"` means the robot's *own* calendar, which is empty. Second, a service account
**cannot put attendees on an event**: Google rejects the call with `forbiddenForServiceAccounts`,
and the only override is domain-wide delegation (below), which needs a Workspace admin. On a
personal gmail account the robot can create, edit, and delete events on your calendar — but it can
never send an invite to a person.

The scope list is the only thing that changes per API. See the [scope table](#scope-reference).

---

## It can't read a user's private inbox or Drive — that needs OAuth

Be honest about the boundary. A service account can touch files and calendars **it owns, or that
were shared with it.** It **cannot** read *your personal* Gmail, your private calendar, or your whole
Drive — because you can't "Share" all of that to a robot the way you share one file.

For **a user's own private data**, you need the browser-consent flow (**3-legged OAuth**): the human
clicks "Allow" once, you save a token, you reuse it.

```python
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json", scopes=["https://www.googleapis.com/auth/calendar.readonly"])
creds = flow.run_local_server(port=0)   # opens a browser the FIRST time, then save creds.to_json()
```

**Domain-wide delegation**, in two sentences: if you run a Google **Workspace** organization, a
super-admin can authorize the service account to *impersonate* your users (by its Client ID + an
explicit scope list, in the Admin console). Powerful, admin-only, easy to over-reach — Google itself
says avoid it when plain sharing works. It only works inside a domain you administer, never against
arbitrary external Gmail accounts.

| I want to… | Use |
|---|---|
| Let a bot read/edit a Sheet, Doc, or Calendar I own | **Service account** + share the file with its email |
| Read my *own* personal Gmail / private Calendar | **3-legged OAuth** (browser consent, save token) |
| Have a bot send calendar invites to other people | **3-legged OAuth** (or domain-wide delegation in a Workspace org) |
| A bot acting as *any user* in my Workspace org | **Domain-wide delegation** (admin-authorized) |

---

## A service account email can't receive mail — it's an identity, not a mailbox

A service account's address (`name@project.iam.gserviceaccount.com`) is an *identity, not a mailbox.*
The `iam.gserviceaccount.com` domain publishes no mail records (no MX), so anything sent to it
hard-bounces. You **cannot** use it to sign up for a service that emails a confirmation link, and
there's no inbox to read — the Gmail API never gives a service account one.

If you actually want a programmatic mailbox, make a normal `@gmail.com` account and read it with
**OAuth** + the Gmail API. Mental model: **a service account is a robot you give *access to files* —
not a robot with an *email address you can write to.***

## In production, inject the key as a secret and use one account per job

**The key is a password.** Anyone holding `credentials.json` *is* your robot. `.gitignore` it. Never
commit it. Rotate it if it leaks (delete the key in the console, make a new one).

**Containers and agents don't ship a file — they inject the key as one secret.** Put the whole JSON
in an env var and load it from a dict:

```python
import os, json, gspread
gc = gspread.service_account_from_dict(json.loads(os.environ["CREDS_JSON"]))
# google-auth equivalent: service_account.Credentials.from_service_account_info(dict, scopes=[...])
```

**One service account per job, least privilege.** Give a read-only bot a read-only scope
(`spreadsheets.readonly`) and share files to it as **Viewer**. Use a separate SA for each agent so
revoking one (unshare, or delete the SA) has a blast radius of exactly one.

**On Google Cloud, skip the key entirely.** If your code runs on Cloud Run / Compute Engine / Cloud
Functions, *attach* a service account to the resource and the libraries pick up credentials
automatically (Application Default Credentials) — no JSON key to leak. For CI or other clouds, use
**Workload Identity Federation**. Google's official stance is to avoid downloaded keys whenever
there's an alternative. For a script on your own laptop, a JSON key is still the normal, fine path.

---

## Most access errors mean you forgot to share the file

| Symptom | Cause |
|---|---|
| `SpreadsheetNotFound` / `403 PERMISSION_DENIED` | **File not shared** with the service account's email. (90% of cases.) |
| `403 ... API has not been used/disabled` | You didn't **enable that API** in the project. |
| `403 ... insufficient ... scopes` on write | Missing or **read-only** scope — check your `scopes=[...]` list. |
| Works elsewhere but `gc.open("name")` fails | Missing the **Drive** scope (needed to find files by name). |
| Can't create a JSON key | Org policy `iam.disableServiceAccountKeyCreation` blocks it — ask an admin or use a personal project. |
| `client_email` is `…@appspot.gserviceaccount.com` | That's an old App Engine default SA; modern ones are `…@PROJECT_ID.iam.gserviceaccount.com`. |

---

## Scope reference

Pass scopes as a **list** in the client libraries. Request the least you need; add `.readonly` when
you only read.

| API | Scope | Access |
|---|---|---|
| Sheets | `https://www.googleapis.com/auth/spreadsheets` | read/write |
| Sheets | `https://www.googleapis.com/auth/spreadsheets.readonly` | read-only |
| Docs | `https://www.googleapis.com/auth/documents` | read/write |
| Docs | `https://www.googleapis.com/auth/documents.readonly` | read-only |
| Drive | `https://www.googleapis.com/auth/drive` | full Drive |
| Drive | `https://www.googleapis.com/auth/drive.file` | only files the app creates/opens |
| Drive | `https://www.googleapis.com/auth/drive.readonly` | read-only |
| Calendar | `https://www.googleapis.com/auth/calendar` | read/write |
| Calendar | `https://www.googleapis.com/auth/calendar.readonly` | read-only |
| Calendar | `https://www.googleapis.com/auth/calendar.events` | events read/write |

---

## If you are an AI agent reading this

Here's the short version for you: ask your human to do the [setup](#no-terminal-click-through-the-console-in-about-20-steps) once and
hand you a `credentials.json` (or a `CREDS_JSON` env var). To touch any file, that file must be
**shared with your `client_email`** — if you get a 403, tell your human *which file and which email*
so they can fix it in one click, rather than retrying. Request **read-only** scopes unless you have a
reason to write, and **read a document before you edit it.** You cannot reach your human's private
Gmail or personal Calendar this way by design — that needs their explicit browser consent, so don't
try to route around it.

---

## Run the examples

```bash
pip install -r requirements.txt
# put your real key next to these files as credentials.json (it's gitignored)
python quickstart.py
```

### What's inside the key file

You don't write this — Google generates it. It's plain JSON with these fields. The two that matter to
you are `client_email` (the address you **share files with**) and `private_key` (the secret — guard it
like a password):

| field | what it is |
|---|---|
| `type` | always `service_account` |
| `project_id` | your GCP project |
| `client_email` | the robot's address — `name@project.iam.gserviceaccount.com`, **share files with this** |
| `private_key` | a long PEM block — the actual secret; anyone with it *is* your robot |
| `private_key_id`, `client_id` | identifiers for the key / account |
| `token_uri`, `auth_uri`, `*_x509_cert_url` | fixed Google endpoints; same for everyone |

---

## Sources

- gspread — Authentication: <https://docs.gspread.org/en/latest/oauth2.html>
- Google Workspace — Create access credentials: <https://developers.google.com/workspace/guides/create-credentials>
- Service accounts overview (IAM): <https://cloud.google.com/iam/docs/service-account-overview>
- Using OAuth 2.0 for server-to-server applications (service accounts): <https://developers.google.com/identity/protocols/oauth2/service-account>
- OAuth 2.0 scopes for Google APIs: <https://developers.google.com/identity/protocols/oauth2/scopes>
- Best practices for service accounts (avoid keys): <https://cloud.google.com/iam/docs/best-practices-service-accounts>
- google-auth `service_account` reference: <https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html>

## License

MIT — see [LICENSE](LICENSE).
