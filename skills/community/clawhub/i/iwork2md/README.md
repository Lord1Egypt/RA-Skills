# iwork2md

Convert Apple iWork documents — **Pages (`.pages`)**, **Numbers (`.numbers`)**, and **Keynote (`.key`)** — into Markdown. Pure Python, **no third-party dependencies**.

`iwork2md` reads the iWork '13+ bundle format directly:

```
file.pages / file.numbers / file.key   (ZIP or directory bundle)
└── Index.zip
    └── *.iwa                           (Snappy-framed Protobuf payloads)
```

It decodes the non-standard Snappy framing and Protobuf containers, extracts text and media references, and **reconstructs modern Numbers tables** (row/column grids with strings, numbers, and formulas).

---

## Features

- **No dependencies** — pure Python 3 standard library (`zipfile`, `struct`, `re`). Works on any macOS/Linux/Windows box.
- **Text extraction** — Pages body text, Numbers cell/header text, Keynote slide text, speaker notes, and comments.
- **Numbers table reconstruction** — resolves `Table (6001)` → `DataList (6005)` linkages and rebuilds the full grid, decoding:
  - **strings** (field 3)
  - **numbers** (IEEE-754 doubles, field 5 → `f42`)
  - **formulas** (rendered as `=formula`)
  - empty cells are padded so the layout is preserved
- **Robust layout handling** — works on both ZIP-bundle files and `.pages` directory packages.
- **Noise filtering** — drops locale codes (`en_HK`), timezones, month-name lists, and number-format strings that would otherwise pollute the output.
- **SkillHub-ready** — ships with `SKILL.md` (slug/version/displayName), `LICENSE.txt` (MIT), and a `references/FORMAT.md` format note.

---

## Installation

Clone the repo:

```bash
git clone https://github.com/slearnAI/iwork2md.git
cd iwork2md
```

No `pip install` required — just run the script. (Optional: `chmod +x scripts/iwork2md.py`.)

---

## Usage

Convert a single file:

```bash
python3 scripts/iwork2md.py path/to/document.numbers
```

Write to a specific output path:

```bash
python3 scripts/iwork2md.py path/to/deck.key output.md
```

If no output path is given, Markdown is printed to **stdout**.

### As an OpenClaw skill

Drop the folder into your skills directory:

```bash
cp -r iwork2md ~/.qclaw/skills/
```

Then ask naturally: *"convert this .pages file to markdown"*, *"extract text from my Numbers sheet"*, *"read that Keynote file"* — the skill triggers and runs the bundled converter.

---

## Output format

- **Pages / Keynote** → headings, paragraphs, lists, and a `## Media` section listing referenced images/video by filename.
- **Numbers** → a `## Tables` section with one Markdown table per sheet, plus any stray text fragments under `## Other text`.

Example (Numbers):

```markdown
# My Spreadsheet

## Tables

| 南航積分 | 酒店積分 | 曼谷 |
| --- | --- | --- |
| CZ3062 | 機票 | 稅費 |
| =formula |  |  |
```

---

## How it works

The underlying decoder (`scripts/iwa.py`) handles three layers:

1. **Bundle** — unzip the `.iwa` files (or walk a directory package).
2. **Snappy framing** — each `.iwa` is a sequence of chunks: `1-byte type` + `3-byte little-endian length` + raw Snappy stream. The raw stream begins with an uncompressed-length varint.
3. **Protobuf container** — `varint(archiveInfoLength)` + `ArchiveInfo{identifier, message_infos[]}` + payload. The message `type` selects the schema; `Table (6001)` and `DataList (6005)` drive table reconstruction.

See [`references/FORMAT.md`](references/FORMAT.md) for the full field-by-field mapping and the engineering notes behind table extraction.

---

## Testing

A self-test decodes a synthetic `.iwa` round-trip:

```bash
python3 scripts/test_iwa.py
# OK: parser decodes synthetic .iwa correctly
```

---

## License

[MIT](LICENSE.txt) © 2026 Stephen Lau
