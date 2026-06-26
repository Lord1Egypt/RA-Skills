# MinerU OCR Local API Output Schema

`mineru_caller.py` returns a stable JSON envelope around MinerU execution and, by default, saves that envelope to a unique file under the system temp directory.

## Output Envelope

Success case:

```json
{
  "ok": true,
  "mode": "api",
  "text": "Complete Markdown from full.md or <file_stem>.md when available",
  "result": {
    "submit": { "...": "raw API task creation response" },
    "batch": { "...": "raw API upload-batch response for local files" },
    "poll": { "...": "final API task-status payload" },
    "local": {
      "command": ["mineru", "-p", "..."],
      "returncode": 0,
      "backend": "pipeline",
      "parse_method": "auto",
      "lang": "ch",
      "local_output_root": "C:/.../output"
    }
  },
  "artifacts": {
    "mode": "api",
    "task_id": "task-123",
    "batch_id": "batch-123",
    "state": "done",
    "full_zip_url": "https://...",
    "downloaded_zip": "C:/.../result.zip",
    "extracted_dir": "C:/.../extracted",
    "full_md_path": "C:/.../extracted/full.md",
    "local_output_root": "C:/.../output",
    "local_doc_root": "C:/.../output/file-name",
    "local_parse_dir": "C:/.../output/file-name/auto",
    "middle_json_path": "C:/.../middle.json",
    "content_list_path": "C:/.../content_list.json"
  },
  "error": null
}
```

Error case:

```json
{
  "ok": false,
  "mode": "local",
  "text": "",
  "result": {
    "submit": null,
    "batch": null,
    "poll": null,
    "local": null
  },
  "artifacts": {},
  "error": {
    "code": "LOCAL_ERROR",
    "message": "Human-readable error"
  }
}
```

## Error Codes

| Code | Meaning |
| --- | --- |
| `INPUT_ERROR` | Invalid CLI arguments, unreadable file, or unsupported mode/input pairing |
| `CONFIG_ERROR` | Missing or invalid MinerU API or local-runtime configuration |
| `API_ERROR` | HTTP failure, task failure, timeout, or unexpected API response |
| `LOCAL_ERROR` | Local MinerU CLI failure or timeout |
| `ARTIFACT_ERROR` | MinerU finished but expected output files could not be found or extracted |

## Artifact Notes

Common fields:

- `artifacts.full_md_path`: main Markdown file that also feeds the top-level `text` field
- `artifacts.middle_json_path`: structured middle output when present
- `artifacts.content_list_path`: content inventory when present

API-only fields:

- `artifacts.task_id`: URL-submission task identifier
- `artifacts.batch_id`: local-file upload batch identifier
- `artifacts.full_zip_url`: archive download URL from the MinerU API
- `artifacts.downloaded_zip`: saved archive path
- `artifacts.extracted_dir`: extracted archive directory

Local-only fields:

- `artifacts.local_output_root`: output directory passed to the local MinerU CLI
- `artifacts.local_doc_root`: document-specific directory created by local MinerU
- `artifacts.local_parse_dir`: actual parse directory, such as `auto`, `ocr`, or `hybrid_auto`
- `artifacts.content_list_v2_path`: VLM or hybrid content list v2 when generated
- `artifacts.model_json_path`: model output dump when generated
- `artifacts.layout_pdf_path`: layout visualization PDF when generated
- `artifacts.span_pdf_path`: span visualization PDF when generated
- `artifacts.origin_pdf_path`: copied source PDF when generated
- `artifacts.images_dir`: extracted images directory

## Task Lifecycle

- Hosted URL flow uses `POST /api/v4/extract/task`
- Hosted local-file flow starts with `POST /api/v4/file-urls/batch`, uploads bytes to `data.file_urls[]`, and polls `GET /api/v4/extract-results/batch/{batch_id}`
- Local open-source flow invokes the official `mineru` CLI from `https://github.com/opendatalab/MinerU`

Official references:
- MinerU API docs: `https://mineru.net/apiManage/docs#/standard/openapi_v4`
- MinerU output files doc: `https://opendatalab.github.io/MinerU/api/output_files/`
- MinerU GitHub repo: `https://github.com/opendatalab/MinerU`
