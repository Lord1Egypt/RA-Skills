# Drive

`Drive(auth)` from `gsuite_drive`. Needs the Drive scope (in the default
login since 0.2.0; older tokens need `gsuite auth login --force`).

## Finding files

```python
from gsuite_core import GoogleAuth
from gsuite_drive import Drive

auth = GoogleAuth()
drive = Drive(auth)

recent = drive.list_files(max_results=20)                     # newest first
in_folder = drive.list_files(parent_id="FOLDER_ID")
pdfs = drive.list_files(query="mimeType = 'application/pdf' and name contains 'invoice'")
matches = drive.search("invoice")                              # name contains, escaped for you
for file in matches:
    print(file.id, file.name, file.mime_type, file.size, file.modified_time, file.web_view_link)

file = drive.get("FILE_ID")                                    # None if it doesn't exist
```

`query` is Drive's [search syntax](https://developers.google.com/drive/api/guides/search-files).

## Downloading and exporting

```python
drive.download("FILE_ID", "/tmp/report.pdf")
drive.download("DOC_ID", "/tmp/notes.pdf", export_format="pdf")   # Google Docs need a format
pdf_bytes = drive.export("DOC_ID", "pdf")                          # pdf, docx, xlsx, pptx, csv, txt, ...
```

Without `export_format`, Google Docs/Sheets/Slides download as docx/xlsx/pptx.

## Uploading and organizing

```python
uploaded = drive.upload("report.pdf", parent_id="FOLDER_ID")      # resumable for big files
note = drive.upload_content(b"hello", "note.txt", mime_type="text/plain")
folder = drive.create_folder("Reports 2026", parent_id="PARENT_ID")
drive.move(uploaded.id, folder.id)
copy = drive.copy(uploaded.id, name="report (copy).pdf")
drive.trash(copy.id)          # recoverable; drive.delete(id) is permanent
```

## Sharing

```python
drive.share(uploaded.id, "ana@example.com", role="writer")                 # reader | commenter | writer
drive.add_permission(uploaded.id, role="reader", type="anyone")            # anyone with the link
drive.add_permission(uploaded.id, role="reader", type="domain", domain="example.com")
for permission in drive.list_permissions(uploaded.id):
    print(permission.role, permission.email_address or permission.domain or permission.type)
```

## What changed

```python
page_token = drive.get_start_page_token()      # "from now on"; keep it
delta = drive.changes(page_token)              # later: delta.changed (files), delta.removed (IDs)
page_token = delta.page_token
```

Push instead of polling: `channel = drive.watch_changes("https://host/hook", token="secret", page_token=page_token)`
makes Google POST to that HTTPS URL on every change (the token comes back in
`X-Goog-Channel-Token`). Channels expire; `drive.stop_channel(channel)` ends one.

## CLI

```bash
gsuite drive list --name invoice -o json
gsuite drive list FOLDER_ID -o json
gsuite drive info FILE_ID -o json
gsuite drive download FILE_ID --out ./report.pdf
gsuite drive download DOC_ID --export pdf --out ./notes.pdf
gsuite drive upload ./report.pdf --to FOLDER_ID --name "Report.pdf"
gsuite drive mkdir "Reports 2026" --in PARENT_ID
gsuite drive move FILE_ID FOLDER_ID
gsuite drive share FILE_ID ana@example.com --role writer
gsuite drive share FILE_ID --anyone             # anyone with the link
gsuite drive delete FILE_ID                    # to the trash; --permanent deletes
```
