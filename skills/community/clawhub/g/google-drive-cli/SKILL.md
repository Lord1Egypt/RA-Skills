---
name: google-drive-cli
description: Interact with Google Drive, Docs, and Sheets using the drivectl CLI. Use this skill when asked to list Drive files, download files, read/update Sheets, or create/export Google Docs.
metadata:
  discovery_doc_drive_v3: "https://www.googleapis.com/discovery/v1/apis/drive/v3/rest"
---
# google-drive-cli

This skill provides guidance on using the `drivectl` command-line tool to interact with Google Workspace (Drive, Docs, Sheets).

## Prerequisites & Authentication

- Ensure `drivectl` is available in your PATH or in the current working directory (e.g., `./drivectl`).
  *If it is not installed, you can quickly download the latest prebuilt binary by running the bundled script: `scripts/install.sh`.*
- **Crucial Rule:** Always append `-O json` to `drivectl` commands when you need to parse the output programmatically or return structured information.

### First-time Authentication

The user must authenticate before using `drivectl`. It securely caches tokens locally so this only needs to happen once. If the user hasn't authenticated, guide them to do so:

```bash
drivectl auth login --secret-file /path/to/your/client_secret.json
```

*(If operating on a headless system or inside an agent environment without a browser, append the `--no-browser-auth` flag to print a manual authorization URL that the user can click).*

## Available Modules

The `drivectl` tool provides several subcommands organized by Workspace service. Pick the correct reference depending on the user's request.

- **Google Drive (Files/Folders)**: See [references/drive.md](references/drive.md) for listing, querying, searching, and downloading files.
- **Google Docs**: See [references/docs.md](references/docs.md) for creating docs from Markdown, reading docs, converting to Markdown, and exploring tab structures.
- **Google Sheets**: See [references/sheets.md](references/sheets.md) for reading ranges, updating cells, and exporting sheets to CSV.

## Dynamic Discovery (Fallback)

If the built-in commands (`list`, `docs`, `sheets`) do not cover the requirement, you can use the `call` subcommand to dynamically invoke *any* Google Workspace API endpoint using Google Discovery.

See [references/discovery.md](references/discovery.md) for detailed instructions on how to formulate and execute these dynamic API calls.
