---
name: google-sheets-soha
description: Read and analyze data from Google Sheets. Trigger when the user mentions "Google Sheet", "spreadsheet", "sheet", sends a docs.google.com/spreadsheets link, or asks questions about data in a sheet — including casual requests like "check my sheet", "read that sheet", or "analyze my spreadsheet data".
metadata:
  version: "1.0.0"
  openclaw:
    requires:
      env:
        - name: GOOGLE_SERVICE_ACCOUNT_JSON
          description: Path to Google Service Account JSON file. Required for private sheets.
          required: false
        - name: GOOGLE_API_KEY
          description: Google API Key for accessing public sheets (Anyone with the link).
          required: false
      bins:
        - python3
        - curl
    primaryEnv: GOOGLE_SERVICE_ACCOUNT_JSON
    homepage: https://github.com/your-username/google-sheets-soha
    repository: https://github.com/your-username/google-sheets-soha
    license: MIT-0
    security:
      dataAccess: read-only
      externalRequests:
        - host: sheets.googleapis.com
          purpose: Fetch spreadsheet data via Google Sheets API v4
        - host: oauth2.googleapis.com
          purpose: Authenticate Service Account credentials
      noDataExfiltration: true
      noCodeExecution: false
      execDescription: Runs python3 scripts locally to fetch and cache sheet data. No code is sent externally.
---

# Google Sheets Skill

Fetches data from Google Sheets via the Google Sheets API v4, caches it on disk, and answers user questions about the data.

---

## Session Memory

Maintain the following context throughout the conversation. Update it as new information is learned:

```
SHEET_CONTEXT = {
  spreadsheetId: null,   // Active Sheet ID
  activeTab: null,       // Current tab being worked on
  tabs: [],              // Cached list of tab names
  headers: {},           // Cached headers per tab: { tabName: [...] }
  rawData: {},           // Cached rows per tab: { tabName: [[...]] }
  cacheFile: null,       // Path to on-disk cache file
}
```

**Rules:**
- Once `spreadsheetId` is known → use it for all subsequent turns, never ask again
- Once a cache file exists and is within TTL → skip the API call
- Always check session context before asking the user for anything

---

## Step 1 — Get the Sheet ID

Check in this order:
1. `SHEET_CONTEXT.spreadsheetId` already set → use it directly
2. URL in the message → extract the ID between `/d/` and `/edit`:
   `https://docs.google.com/spreadsheets/d/**SHEET_ID**/edit`
3. User provides the ID directly → save and use it
4. Not found anywhere → ask **exactly once**:

> "Could you share the Google Sheet link or Sheet ID? I'll remember it for the rest of our conversation 😊"

Once received → save to `SHEET_CONTEXT.spreadsheetId` immediately and proceed.

---

## Step 2 — Fetch Data from Google Sheets API

Use **Google Sheets API v4**. Choose the auth method based on the sheet type:

### Option A: Public sheet (Anyone with the link)

```bash
# List tabs
curl -s "https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?key={GOOGLE_API_KEY}&fields=sheets.properties" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); [print(s['properties']['title']) for s in d['sheets']]"

# Fetch tab data
curl -s "https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{TAB_NAME}!A1:Z1000?key={GOOGLE_API_KEY}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('values',[])))"
```

### Option B: Private sheet (Service Account)

```python
import os, json
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file(
    os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"],
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)
service = build("sheets", "v4", credentials=creds)

# List tabs
meta = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
tabs = [s["properties"]["title"] for s in meta["sheets"]]

# Fetch tab data
result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range=f"{TAB_NAME}!A1:Z1000"
).execute()
rows = result.get("values", [])
```

Save results to `SHEET_CONTEXT.headers[tabName]` and `SHEET_CONTEXT.rawData[tabName]`.

---

## Step 3 — Disk Cache

Cache fetched data to avoid redundant API calls across turns.

### Cache path
```
~/.openclaw/workspace/.cache/sheets/{spreadsheetId}/{tabName}.json
```

### Cache file structure
```json
{
  "spreadsheetId": "abc123",
  "tabName": "Sheet1",
  "fetchedAt": 1710000000,
  "ttl": 300,
  "headers": ["Name", "Status", "Date"],
  "rows": [
    ["Task A", "Done", "2024-01-01"],
    ["Task B", "Pending", "2024-01-02"]
  ]
}
```

### Cache script (run via exec tool)

```python
import os, json, time, shutil

CACHE_DIR = os.path.expanduser("~/.openclaw/workspace/.cache/sheets")
TTL = 300  # 5 minutes — increase to 3600 for rarely-changing data

def cache_path(sheet_id, tab):
    d = os.path.join(CACHE_DIR, sheet_id)
    os.makedirs(d, exist_ok=True)  # auto-creates on first use
    return os.path.join(d, f"{tab.replace('/', '_')}.json")

def load_cache(sheet_id, tab):
    path = cache_path(sheet_id, tab)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        c = json.load(f)
    if time.time() - c.get("fetchedAt", 0) > c.get("ttl", TTL):
        return None  # expired — will re-fetch
    return c

def save_cache(sheet_id, tab, headers, rows):
    path = cache_path(sheet_id, tab)
    with open(path, "w") as f:
        json.dump({
            "spreadsheetId": sheet_id,
            "tabName": tab,
            "fetchedAt": int(time.time()),
            "ttl": TTL,
            "headers": headers,
            "rows": rows
        }, f, ensure_ascii=False)

def clear_cache(sheet_id=None):
    target = os.path.join(CACHE_DIR, sheet_id) if sheet_id else CACHE_DIR
    if os.path.exists(target):
        shutil.rmtree(target)
```

### Cache flow

```python
cached = load_cache(SHEET_ID, TAB_NAME)
if cached:
    headers, rows = cached["headers"], cached["rows"]
else:
    # fetch from API...
    headers, rows = fetched_rows[0], fetched_rows[1:]
    save_cache(SHEET_ID, TAB_NAME, headers, rows)
```

### When to clear cache

| User says | Action |
|---|---|
| "refresh", "reload", "get latest data" | `clear_cache(SHEET_ID)` then re-fetch |
| "clear cache" | `clear_cache()` — wipes everything |
| TTL expired | Automatically re-fetches on next request |
| User switches to a new sheet | Keep old cache, create new cache for the new sheet |

---

## Step 4 — Answer the User

- Always state which **sheet/tab** the data is from
- Use **markdown tables** when displaying multiple rows
- Reply in the **same language as the user**
- If data exceeds 500 rows, analyze the first 200 and ask if the user wants to narrow the range

---

## Configuration in openclaw.json

Add under `skills.entries` (top-level, not inside `agents`):

### Public sheet
```json
{
  "skills": {
    "entries": {
      "google-sheets-soha": {
        "enabled": true,
        "env": {
          "GOOGLE_API_KEY": "AIza..."
        }
      }
    }
  }
}
```

### Private sheet
```json
{
  "skills": {
    "entries": {
      "google-sheets-soha": {
        "enabled": true,
        "env": {
          "GOOGLE_SERVICE_ACCOUNT_JSON": "/home/node/.openclaw/google-sa.json"
        }
      }
    }
  }
}
```

---

## Error Handling

| Situation | Action |
|---|---|
| Sheet ID not provided | Ask once, save when received |
| API returns 403 | Sheet is private → guide user to share with service account email |
| API returns 404 | Wrong Sheet ID → ask again |
| `GOOGLE_API_KEY` not set | Guide user to add it in `openclaw.json` |
| Tab not found | List `SHEET_CONTEXT.tabs` and ask user to pick |
| Data too large | Analyze first 200 rows, notify user |
| `python3` not found | Run: `apt-get install -y python3` inside container |