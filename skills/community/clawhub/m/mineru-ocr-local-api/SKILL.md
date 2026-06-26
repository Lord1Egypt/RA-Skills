---
name: mineru-ocr-local-api
description: Parse complex PDFs and document images with MinerU through either the hosted MinerU API or the local open-source MinerU runtime. Use when Codex, OpenClaw, Claude Code, or similar coding agents need MinerU-based OCR, layout-aware Markdown extraction, formula extraction, local-file upload to the MinerU API, local MinerU CLI parsing from https://github.com/opendatalab/MinerU, mode selection between api and local, task polling, archive download, or complete document text extraction.
metadata:
  openclaw:
    homepage: https://github.com/opendatalab/MinerU
    primaryEnv: MINERU_API_TOKEN
    requires:
      anyBins:
        - python
        - python.exe
    envVars:
      - name: MINERU_API_TOKEN
        required: false
        description: Required for hosted MinerU API mode.
      - name: MINERU_API_BASE_URL
        required: false
        description: Optional MinerU API base URL override.
      - name: MINERU_API_TIMEOUT
        required: false
        description: Optional HTTP timeout for MinerU API mode.
      - name: MINERU_API_POLL_TIMEOUT
        required: false
        description: Optional polling timeout for MinerU API mode.
      - name: MINERU_API_POLL_INTERVAL
        required: false
        description: Optional polling interval for MinerU API mode.
      - name: MINERU_LOCAL_CMD
        required: false
        description: Optional path to mineru or mineru.exe for local mode.
      - name: MINERU_LOCAL_PYTHON
        required: false
        description: Optional Python interpreter for python -m mineru.cli.client.
      - name: MINERU_LOCAL_BACKEND
        required: false
        description: Optional local MinerU backend override.
      - name: MINERU_LOCAL_METHOD
        required: false
        description: Optional local MinerU parse method override.
      - name: MINERU_LOCAL_LANG
        required: false
        description: Optional local MinerU language hint.
      - name: MINERU_LOCAL_MODEL_SOURCE
        required: false
        description: Optional local MinerU model source override.
      - name: MINERU_LOCAL_DEVICE_MODE
        required: false
        description: Optional local MinerU device override.
      - name: MINERU_LOCAL_TIMEOUT
        required: false
        description: Optional timeout for local MinerU mode.
    dependencies:
      - name: httpx
        type: pip
        version: ">=0.27"
        url: https://pypi.org/project/httpx/
        repository: https://github.com/encode/httpx
---

# MinerU OCR Local API

## Hard Rules

1. Use `python scripts/mineru_caller.py` for every MinerU request.
2. Do not parse the document yourself as a fallback.
3. If MinerU returns an error, show the error and stop.
4. Treat the saved JSON envelope and generated artifact files as the source of truth.
5. Prefer the top-level `text` field when the user asks for the full extracted document.

## Choose The Mode

- Use `--mode api` when the user wants the hosted MinerU service, already has `MINERU_API_TOKEN`, needs URL input, or wants the official cloud API workflow.
- Use `--mode local` when the user wants the open-source MinerU runtime from `https://github.com/opendatalab/MinerU`, wants data to stay local, or explicitly asks for local parsing.
- Use `--mode auto` only when the user does not care which mode is used. `auto` prefers API when `MINERU_API_TOKEN` is configured and falls back to local only for local files.

## Standard Workflow

1. For a hosted API parse from URL:

   ```bash
   python scripts/mineru_caller.py --mode api --file-url "https://example.com/paper.pdf" --pretty
   ```

2. For a hosted API parse from a local file:

   ```bash
   python scripts/mineru_caller.py --mode api --file-path "C:/docs/paper.pdf" --pretty
   ```

3. For a local open-source MinerU parse:

   ```bash
   python scripts/mineru_caller.py --mode local --file-path "C:/docs/paper.pdf" --pretty
   ```

4. When the input is a local file and the user will need an IDE-accessible path, prefer saving beside the source file:

   ```bash
   python scripts/mineru_caller.py --mode local --file-path "C:/docs/paper.pdf" --download-dir "C:/docs/paper.mineru" --pretty
   ```

5. Read these output fields before answering:
   - `mode`: actual execution mode used
   - `text`: complete document Markdown from `full.md` or `<file_stem>.md`
   - `result.submit`: raw task-creation response for API URL parsing
   - `result.batch`: raw upload-batch response for API local-file parsing
   - `result.poll`: final API task-status payload
   - `result.local`: local MinerU CLI invocation summary
   - `artifacts.full_md_path`: absolute path to the main Markdown file
   - `artifacts.local_parse_dir`: local MinerU parse directory when using `--mode local`
   - `artifacts.downloaded_zip`: downloaded MinerU archive when using `--mode api`

## Useful Flags

- `--mode api|local|auto`: choose hosted API, local runtime, or automatic selection
- `--no-wait`: return after submission without polling; API mode only
- `--no-download`: skip downloading `full_zip_url`; API mode only
- `--download-dir DIR`: store API downloads or local MinerU outputs in a specific directory
- `--language en`: pass a language hint
- `--ocr`: force OCR mode
- `--disable-formula`: turn off formula extraction
- `--local-cmd PATH`: explicit path to `mineru.exe` or `mineru`
- `--local-python PATH`: explicit Python path for `python -m mineru.cli.client`
- `--local-backend pipeline`: choose the local MinerU backend
- `--local-method auto|txt|ocr`: choose the local MinerU parse method
- `--local-model-source modelscope`: useful in environments where Hugging Face access is restricted
- `--local-device cpu`: force a local inference device when needed

## Present Results

- If the user asks for all text, show the top-level `text` field.
- If the user asks where files were saved, report the paths in `artifacts`.
- If the output is large, give the saved file paths first and then the requested excerpt or summary.
- If API mode completed but archive download failed, report `artifacts.full_zip_url`.

## Configuration

For API mode:

```text
MINERU_API_TOKEN
MINERU_API_BASE_URL=https://mineru.net
MINERU_API_TIMEOUT=60
MINERU_API_POLL_TIMEOUT=900
MINERU_API_POLL_INTERVAL=5
```

Windows PowerShell examples:

```powershell
$env:MINERU_API_TOKEN="YOUR_MINERU_TOKEN"
setx MINERU_API_TOKEN "YOUR_MINERU_TOKEN"
```

Use the first command for the current terminal only. Use `setx` to persist it for future terminals, then restart Codex/Cursor or open a new terminal.

For local mode, configure at least one runtime entry point:

```text
MINERU_LOCAL_CMD=C:\path\to\mineru.exe
MINERU_LOCAL_PYTHON=C:\path\to\python.exe
MINERU_LOCAL_BACKEND=pipeline
MINERU_LOCAL_METHOD=auto
MINERU_LOCAL_LANG=ch
MINERU_LOCAL_MODEL_SOURCE=modelscope
MINERU_LOCAL_DEVICE_MODE=cpu
MINERU_LOCAL_TIMEOUT=3600
```

Local mode only supports `--file-path`. It does not accept `--file-url`.

## Error Handling

- Missing API token: show the configuration error, tell the user to set `MINERU_API_TOKEN`, and include one-shot plus persistent commands.
- Missing local runtime: show the configuration error and stop.
- Failed task or failed local CLI run: show the error and stop.
- Poll timeout: tell the user the task id and that polling timed out.
- API archive download TLS error: rely on the built-in `curl` fallback before reporting failure.
- Missing expected output files: return any artifact paths that do exist and report the missing output.

## References

- `references/output_schema.md`: JSON envelope and artifact layout for both modes.

Load the reference file when:
- You need to explain which saved files matter.
- You need to inspect mode-specific artifacts such as `downloaded_zip`, `local_parse_dir`, `middle_json`, or `content_list`.

## Verification

Validate the skill folder:

```bash
python /path/to/quick_validate.py /path/to/mineru-ocr-api-local
```

Run a local runtime check against a sample PDF:

```bash
python scripts/mineru_caller.py --mode local --file-path "D:/path/to/file.pdf" --pretty --stdout
```

Run an API runtime check against a remote PDF:

```bash
python scripts/mineru_caller.py --mode api --file-url "https://example.com/file.pdf" --pretty --stdout
```
