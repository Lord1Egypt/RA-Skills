---
name: lark-cli-devhub-drive
description: Use when managing Feishu/Lark Drive files through lark-cli or feishu-cli for Dev Hub search, inspect, upload, download, import, export, sync, comments, permissions, and artifact registration.
metadata:
  requires:
    bins: ["lark-cli"]
---

# Lark CLI Dev Hub Drive

Drive is the file and artifact layer. Use it when project knowledge lives in files, folders, comments, exported docs, imported reports, or Drive permissions.

Discovery aliases: `feishu-cli drive`, `飞书云空间`, `lark-cli drive`, `Drive sync`, `Feishu file export`, `Lark artifact management`.

## Office Use Cases

- Mirror a project folder between local disk and Feishu Drive with `drive +pull`, `+push`, `+sync`, or `+status`.
- Import local `.xlsx`, `.csv`, `.docx`, or source material into Feishu cloud docs with `drive +import`.
- Export Docs, Sheets, or Base snapshots before a release or audit with `drive +export`.
- Inspect a user-provided URL and unwrap Wiki links before choosing Docs, Sheets, Base, or Slides skills.
- Register important files in Dev Hub `Artifacts` with title, source URL, summary, project, area, and keywords.
- Add comments to docs/sheets/slides when the user wants review feedback instead of content mutation.

## Routing Rules

- Use `drive +search` for resource discovery across docs, wiki, sheets, folders, and Base.
- Use `drive +inspect` whenever the input is a URL and the real underlying type is unclear.
- After locating a structured object, route to the right domain skill: Docs/Wiki, Sheets, Base, Slides, or Whiteboard.
- Do not store downloaded private files in the repo unless the user explicitly wants that.

## Useful Commands

```bash
lark-cli drive +search --query "release report" --as user --format json
lark-cli drive +inspect --url "$LARK_URL" --as user --format json
lark-cli drive +export --url "$DOC_URL" --output ./exports --as user
lark-cli drive +upload --file ./artifact.pdf --folder-token "$FOLDER_TOKEN" --as user
lark-cli drive +sync --local ./docs --folder-token "$FOLDER_TOKEN" --as user
```

## Dev Hub Writeback

When a file becomes part of project knowledge, write or update an `Artifacts` record:

- `Artifact Type`: File, Export, Import, Snapshot, Review, or Folder
- `Source URL`: Feishu URL
- `Summary`: what it contains and why it matters
- `Search Keywords`: project, area, filename, owner, date, and decision keywords
