# ComfyUI Safe Connector - Endpoints

The runner uses these ComfyUI endpoints:

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/queue` | Health check and queue status |
| POST | `/prompt` | Submit workflow |
| GET | `/history/{prompt_id}` | Fetch execution result |
| GET | `/view` | Download rendered image |
| POST | `/queue` | Clear queue |
| POST | `/interrupt` | Stop current run |

## Workflow input

The runner accepts raw workflow JSON from:
- `--workflow-file`
- `--workflow-stdin`
- `--workflow-json`

It also still supports built-in template JSON files in `workflows/`.

## Output handling

When a run finishes, the script:
- fetches every image in the result history
- saves them in `generated/`
- returns `view_url` plus `local_path` for each output

Use `python3 scripts/serve_generated.py` if you want a temporary local browser server for `generated/`.
