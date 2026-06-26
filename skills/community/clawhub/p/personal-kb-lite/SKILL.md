---
name: personal-kb-lite
description: >
  Local file knowledge base with LLM-powered indexing and Q&A.
  Scans a directory for documents (.txt, .md, .pdf, .docx, .xlsx, .csv),
  extracts metadata (summary, tags, table of contents) using the LLM,
  and answers questions by retrieving relevant files.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: pdfplumber
      - kind: uv
        package: python-docx
      - kind: uv
        package: openpyxl
    keywords:
      - knowledge base
      - document search
      - file indexing
      - RAG
      - Q&A
      - local search
    categories:
      - productivity
      - knowledge-management
    command: kb
    emoji: "📚"
---

## Task: Local Knowledge Base

Arguments: **$ARGUMENTS**

### Mode Selection

- If `$ARGUMENTS` is `--alias <name>`: set a custom command alias — save `{"command_alias": "<name>"}` into `.kb-config.json` (merge with existing fields), then reply: `Command alias set to /<name>`. Terminate.
- If `$ARGUMENTS` is `--alias reset`: remove the `command_alias` field from `.kb-config.json`, then reply: `Command alias reset to default /kb`. Terminate.
- If `$ARGUMENTS` is empty (user only typed `/kb`), execute the **Indexing Workflow** below
- If `$ARGUMENTS` is not empty, treat it as a user question and execute the **Q&A Workflow** below

---

## Indexing Workflow

### Step 1: Confirm Watch Directory

1. Read `.kb-config.json` from the current working directory using the Read tool
2. If the file exists and `watch_dir` is a non-empty string, use it as `WATCH_DIR`
3. If the file does not exist or `watch_dir` is empty, **ask the user**:
   > Please enter the absolute path of the directory to watch:

   Save the user's input as `WATCH_DIR`, and write the following to `.kb-config.json` using the Write tool:
   ```json
   {"watch_dir": "<WATCH_DIR>"}
   ```

4. Verify the directory exists using Bash:
   ```bash
   ls "<WATCH_DIR>" > /dev/null 2>&1 && echo "ok" || echo "not_found"
   ```
   If it returns `not_found`, inform the user and terminate.

### Step 2: Load Existing Metadata

Read `<WATCH_DIR>/.kb-meta.json` using the Read tool.

- If the file exists, parse the JSON and extract the `files` object (keyed by filename)
- If it does not exist, initialize `files = {}`

### Step 3: Scan Directory for New and Modified Files

List files recursively in the directory using Bash:

```bash
find "<WATCH_DIR>" -type f \( -name "*.txt" -o -name "*.md" -o -name "*.docx" -o -name "*.pdf" -o -name "*.xlsx" -o -name "*.csv" \) -not -name ".kb-meta.json" -print
```

For each file found, get its modification time using Bash:

```bash
stat -f "%m" "<filepath>"   # macOS
stat -c "%Y" "<filepath>"   # Linux
```

A file needs (re-)indexing if:
- Its relative path is not in the `files` object, OR
- Its modification time is newer than the `indexed_at` timestamp in the existing entry

Also, remove any entries from `files` whose files **no longer exist on disk** (stale cleanup).

Use the relative path from `WATCH_DIR` as the key (e.g., `subdir/report.pdf`).

If there are no files to process and no stale entries to clean, output:
```
No changes detected (X files already indexed)
```
Then terminate.

### Step 4: Process Each File That Needs Indexing

For each file, follow these steps:

#### 4a. Read File Content

Read the file using the method described in **Appendix: File Reading Methods** below, with `MAX_CHARS = 8000`.

If reading fails, record `"error": "Read failed: <error message>"` in the file's metadata entry and skip to the next file.

#### 4b. Extract Metadata

After reading the file content, generate the following fields:

- **`summary`**: A 100-200 word summary describing the file's core content and purpose
- **`tags`**: 3-8 classification tags as a JSON array
- **`toc`**: A list of the file's major section/chapter titles as a JSON array (max 20 items); return an empty array if no clear structure exists

#### 4c. Update and Save Metadata Immediately

Add the following entry to the `files` object:

```json
"<filename>": {
  "filename": "<filename>",
  "summary": "<summary>",
  "tags": ["tag1", "tag2"],
  "toc": ["section1", "section2"],
  "indexed_at": "<current time, ISO 8601 format>",
  "file_size": <bytes, obtained via Bash wc -c>
}
```

**Write the complete `.kb-meta.json` back to disk immediately after processing each file**, to avoid losing progress if interrupted.

Show progress for each file, e.g.:
```
[1/3] Processing: contract_template.txt ... done
[2/3] Processing: product_manual.pdf ... done
[3/3] Processing: quotation.xlsx ... failed (read error)
```

### Step 5: Output Summary

```
Indexing complete
  Total files scanned: X
  Newly indexed: Y
  Failed/skipped: Z
  Metadata file: <WATCH_DIR>/.kb-meta.json
```

---

## Q&A Workflow

User question: **$ARGUMENTS**

### Step 1: Load Configuration and Metadata

1. Read `.kb-config.json` from the current working directory using the Read tool, and get the `watch_dir` field (referred to as `WATCH_DIR`)

   If the file does not exist or `watch_dir` is empty, reply:
   > Knowledge base directory not configured. Please run `/kb` first to set up the index.

   Then terminate.

2. Read `<WATCH_DIR>/.kb-meta.json` using the Read tool

   If the file does not exist or `files` is an empty object, reply:
   > Knowledge base index is empty. Please run `/kb` first to build the index.

   Then terminate.

### Step 2: Build File Index Summary

Organize each entry in `files` into a single line of plain text:

```
File: contract_template.txt, Summary: Standard procurement contract template with rights and obligations..., Tags: contract, procurement, template, TOC: Article 1 Definitions, Article 2 Rights, Article 3 Breach
File: product_manual.pdf, Summary: Technical specifications and installation guide for Product A..., Tags: product, specs, TOC: Overview, Installation, FAQ
```

- If a field is empty or missing, omit it
- `toc`: show at most the first 15 items, comma-separated
- `tags`: comma-separated

### Step 3: Identify Relevant Files

Based on the index summary and user question, determine which files **may** contain the answer.

Criteria:
- The file's summary, tags, or table of contents contain information semantically related to the question
- Prefer including a marginally relevant file over missing a potentially useful one

**If no files are possibly relevant**, reply directly:
> Sorry, no files related to your question were found in the knowledge base.
>
> Current indexed file count: X
> Suggestion: Verify the question falls within the knowledge base scope, or run `/kb` to update the index.

Then terminate.

Record the matched filenames as an internal variable `MATCHED_FILES` (do not show this list to the user).

### Step 4: Read Full Content of Relevant Files

For each filename in `MATCHED_FILES`, read the file using the method described in **Appendix: File Reading Methods** below (no truncation, omit `MAX_CHARS`).

If a file fails to read, skip it and continue with the remaining files.

### Step 5: Generate Answer

Based on the content of the retrieved files, answer the user's question.

Requirements:

1. **Answer directly**, preferring to quote the file's original text, data, or specific statements
2. If multiple files contain relevant information, synthesize the answer and note which file each part comes from
3. If the file content can only partially answer the question, indicate which parts could not be found in the knowledge base
4. Append **citation sources** at the end of the answer, formatted as:

```
---
Sources:
[1] contract_template.txt
[2] product_manual.pdf
```

Only list files actually used in the answer; do not include matched but unused files.

---

## Appendix: File Reading Methods

Use the following methods based on file extension. All Bash commands pass the file path via the `KB_FILE` environment variable to avoid filename injection issues.

Optional parameter `MAX_CHARS`: if provided, truncate output to that many characters; if omitted, output the full content.

- **`.txt` / `.md` / `.csv`**: Read using the Read tool at `<WATCH_DIR>/<filename>`. If `MAX_CHARS` is set, only read the first `MAX_CHARS` characters (approximately `MAX_CHARS / 40` lines).

- **`.docx`**: Run via Bash:
  ```bash
  KB_FILE="<WATCH_DIR>/<filename>" python3 -c "
  import docx, os
  doc = docx.Document(os.environ['KB_FILE'])
  text = '\n'.join(p.text for p in doc.paragraphs if p.text.strip())
  limit = int(os.environ.get('KB_MAX_CHARS', '0'))
  print(text[:limit] if limit else text)
  "
  ```

- **`.pdf`**: Run via Bash:
  ```bash
  KB_FILE="<WATCH_DIR>/<filename>" python3 -c "
  import pdfplumber, os
  with pdfplumber.open(os.environ['KB_FILE']) as pdf:
      text = '\n'.join(p.extract_text() or '' for p in pdf.pages)
  limit = int(os.environ.get('KB_MAX_CHARS', '0'))
  print(text[:limit] if limit else text)
  "
  ```

- **`.xlsx`**: Run via Bash:
  ```bash
  KB_FILE="<WATCH_DIR>/<filename>" python3 -c "
  import openpyxl, os
  wb = openpyxl.load_workbook(os.environ['KB_FILE'], data_only=True)
  rows = []
  for ws in wb.worksheets:
      for row in ws.iter_rows(values_only=True):
          line = '\t'.join(str(v) for v in row if v is not None)
          if line.strip():
              rows.append(line)
  text = '\n'.join(rows)
  limit = int(os.environ.get('KB_MAX_CHARS', '0'))
  print(text[:limit] if limit else text)
  "
  ```

When `MAX_CHARS` is needed, prepend `KB_MAX_CHARS="<value>"` to the environment variables, e.g.:
```bash
KB_FILE="..." KB_MAX_CHARS="8000" python3 -c "..."
```
