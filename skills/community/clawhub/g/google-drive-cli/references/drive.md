# Google Drive Operations

Use `drivectl` to interact with files in Google Drive. Always use `-O json` for programmatic parsing.

## Listing Files

To list files, use `drivectl list`. It supports querying with Google Drive search syntax.

**Basic list (default 100 items):**
```bash
drivectl list -O json
```

**List with limit:**
```bash
drivectl list --limit 5 -O json
```

**Search by name:**
```bash
drivectl list -q "name contains 'Project'" -O json
```

**Search for Google Docs specifically:**
```bash
drivectl list -q "mimeType='application/vnd.google-apps.document'" -O json
```

## Downloading / Getting File Content

To download a file or its raw content to stdout:
```bash
drivectl get <file-id>
```

*(Note: For Google Workspace documents, you often want to convert them during export. For example, to convert Google Docs to Markdown, see docs.md).*

## Revisions and Comments

**View the revision history:**
```bash
drivectl revisions <file-id> -O json
```

**View threaded comments:**
```bash
drivectl comments <file-id> -O json
```
