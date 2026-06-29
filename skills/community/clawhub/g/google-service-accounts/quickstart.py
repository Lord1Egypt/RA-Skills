#!/usr/bin/env python3
"""Minimal, runnable service-account examples for Google Sheets, Docs, and Calendar.

Prereqs (see README): a service account JSON key saved as `credentials.json`,
and the target file/calendar SHARED with the service account's client_email.

Usage:
  python quickstart.py sheets   "My Spreadsheet"
  python quickstart.py docs     <DOC_ID>
  python quickstart.py calendar <OWNER_EMAIL>   # the shared calendar's id is its owner's email
"""
import sys

CREDS = "credentials.json"


def sheets(name):
    import gspread
    gc = gspread.service_account(filename=CREDS)   # default scopes: spreadsheets + drive
    sh = gc.open(name)                             # works only if shared with the SA email
    ws = sh.sheet1
    print("Before:", ws.get_all_values())
    ws.update(values=[["hello", "from a robot"]])
    print("After: ", ws.get_all_values())


def _build(api, version, scopes):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_file(CREDS, scopes=scopes)
    return build(api, version, credentials=creds)


def docs(doc_id):
    svc = _build("docs", "v1", ["https://www.googleapis.com/auth/documents"])
    doc = svc.documents().get(documentId=doc_id).execute()
    print("Title:", doc.get("title"))
    # Look before you leap: confirm what you're editing before mutating a live doc.
    svc.documents().batchUpdate(documentId=doc_id, body={"requests": [
        {"insertText": {"location": {"index": 1}, "text": "Edited by a robot.\n"}}
    ]}).execute()
    print("Inserted a line at the top.")


def calendar(calendar_id):
    svc = _build("calendar", "v3", ["https://www.googleapis.com/auth/calendar.readonly"])
    events = svc.events().list(calendarId=calendar_id, maxResults=10,
                               singleEvents=True, orderBy="startTime").execute()
    for e in events.get("items", []):
        start = e["start"].get("dateTime", e["start"].get("date"))
        print(start, "-", e.get("summary", "(no title)"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "sheets":
        sheets(sys.argv[2])
    elif cmd == "docs":
        docs(sys.argv[2])
    elif cmd == "calendar":
        calendar(sys.argv[2])
    else:
        print(__doc__)
