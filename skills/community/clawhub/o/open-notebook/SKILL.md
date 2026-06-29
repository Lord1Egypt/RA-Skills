---
name: open-notebook
description: Access and manage a self-hosted Open Notebook research system (NotebookLM alternative). Create notebooks, add sources (text/URL/file), cross-notebook search, and RAG-chat with your research notes. Use only when the user explicitly asks to save, search, or ask about specific content they have stored.
version: 1.3.2
homepage: "https://github.com/Crabsticksalad/open-notebook-skill"
permissions:
  network:
    - 127.0.0.1:5077
metadata:
  openclaw:
    emoji: "📓"
    primaryEnv: OPEN_NOTEBOOK_API_KEY
    requires:
      bins: [curl, jq]
    config:
      env:
        OPEN_NOTEBOOK_API_KEY:
          description: "Per-agent API key issued by the bridge in agents.json"
          required: true
        OPEN_NOTEBOOK_BRIDGE_URL:
          description: "Bridge base URL (default http://127.0.0.1:5077)"
          required: true
---

# Open Notebook

Self-hosted NotebookLM alternative for OpenClaw agents. The agent reaches open-notebook through a local FastAPI bridge that adds per-agent auth, a per-notebook allowlist, and an audit log.

> 🔒 **Security:** Calls go over loopback to a local bridge. The bridge's `X-API-Key` header is the only auth.

## Compatibility

- **open-notebook:** v1.9.0 or later
- **Bridge endpoint contract:** `DELETE /v1/sources/{id}`, `GET /v1/sources/{id}`, `GET /v1/notebooks/{id}`  -  all required
- **Tested embedding model:** `perplexity/pplx-embed-v1-4b` (OpenRouter)

## When to use

- "Save this to my research" / "Add this to my [topic] notebook"
- "What did I save about X?" / "Find my notes on Y"
- "Create a new notebook for Z"
- "Chat with my [topic] research" / "Ask my notes about…"

**Do NOT use for:** secrets, credentials, ephemeral scratch work. Notebooks are stored unencrypted at rest.

## Install / Setup

This skill is a **bridge client**  -  it does nothing on its own. You need a running open-notebook deployment and the bridge service.

### 1. Deploy open-notebook

Follow the [lfnovo/open-notebook](https://github.com/lfnovo/open-notebook) deployment guide. Run it locally or on a server.

### 2. Set up the bridge

The bridge is a FastAPI service that wraps the open-notebook API with per-agent auth. See [bridge setup](#bridge-setup) below.

### 3. Install this skill

```bash
clawhub install crabsticksalad/open-notebook
```

### 4. Configure environment

Add to `~/.openclaw/.env`:
```
OPEN_NOTEBOOK_BRIDGE_URL=http://127.0.0.1:5077
OPEN_NOTEBOOK_API_KEY=<your-agent-key>
```

### 5. Restart gateway

```bash
systemctl --user restart openclaw-gateway
```

## Bridge setup

The bridge is a small FastAPI app (`main.py`) that:
- Authenticates agents via `X-API-Key` header
- Audits every call to a log file
- Enforces per-notebook allowlists (using `check_notebook` function)
- Filters `list-notebooks` to only return notebooks the agent is allowed to access
- Verifies source ownership before `get-source` and `delete-source` — agents cannot fetch or delete sources belonging to notebooks they have no access to
- `search` is intentionally cross-notebook (queries all embeddings) — agents should only have access to notebooks they are authorized for via `allowed_notebooks`

### Minimal bridge main.py

```python
#!/usr/bin/env python3
"""Open Notebook Bridge  -  auth + audit + per-agent allowlist wrapper."""
import json, os, logging
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.responses import Response
import httpx, uvicorn

UPSTREAM = "http://127.0.0.1:5055"
BRIDGE_PORT = int(os.environ.get("BRIDGE_PORT", "5077"))
AGENTS_FILE = Path(os.environ.get("AGENTS_FILE", "agents.json")).expanduser()
AUDIT_LOG = Path(os.environ.get("AUDIT_LOG", "audit.log")).expanduser()
ON_PASSWORD = os.environ.get("OPEN_NOTEBOOK_PASSWORD", "")

AGENTS = json.loads(AGENTS_FILE.read_text()) if AGENTS_FILE.exists() else {}
logging.basicConfig(filename=str(AUDIT_LOG), level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
audit = logging.getLogger("audit")

app = FastAPI()

def check_notebook(agent, notebook_id):
    """Enforce allowed_notebooks allowlist. Set allowed_notebooks to ['*'] for full access."""
    allowed = agent.get("allowed_notebooks", [])
    if allowed == "*" or allowed == ["*"]:
        return
    if notebook_id not in allowed:
        audit.warning(f"DENIED {agent['name']} access to {notebook_id}")
        raise HTTPException(403, f"not allowed to access {notebook_id}")

async def auth(x_api_key: str | None = Header(None)):
    if not x_api_key or x_api_key not in AGENTS:
        audit.warning(f"REJECTED unknown api key ...{x_api_key[-8:]}")
        raise HTTPException(401, "invalid api key")
    return AGENTS[x_api_key]

@app.get("/v1/health")
async def health():
    # Returns only a status — no agent count or deployment metadata leaked
    return {"status": "ok"}

@app.get("/v1/notebooks")
async def list_notebooks(agent=Depends(auth)):
    audit.info(f"{agent['name']} GET /v1/notebooks")
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.get(f"{UPSTREAM}/api/notebooks", headers={"Authorization": f"Bearer {ON_PASSWORD}"})
    # Filter to notebooks this agent is allowed to access
    if r.status_code == 200:
        notebooks = r.json()
        allowed = agent.get("allowed_notebooks", [])
        if allowed != "*" and allowed != ["*"]:
            notebooks = [nb for nb in notebooks if nb.get("id") in (allowed or [])]
        return Response(content=json.dumps(notebooks), status_code=r.status_code)
    return Response(content=r.content, status_code=r.status_code)

@app.post("/v1/notebooks")
async def create_notebook(request: Request, agent=Depends(auth)):
    body = await request.json()
    audit.info(f"{agent['name']} POST /v1/notebooks")
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post(f"{UPSTREAM}/api/notebooks", json=body, headers={"Authorization": f"Bearer {ON_PASSWORD}"})
    return Response(content=r.content, status_code=r.status_code)

@app.get("/v1/notebooks/{notebook_id}")
async def get_notebook(notebook_id: str, agent=Depends(auth)):
    check_notebook(agent, notebook_id)
    audit.info(f"{agent['name']} GET /v1/notebooks/{notebook_id}")
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.get(f"{UPSTREAM}/api/notebooks/{notebook_id}", headers={"Authorization": f"Bearer {ON_PASSWORD}"})
    return Response(content=r.content, status_code=r.status_code)

@app.delete("/v1/notebooks/{notebook_id}")
async def delete_notebook(notebook_id: str, agent=Depends(auth)):
    check_notebook(agent, notebook_id)
    audit.info(f"{agent['name']} DELETE /v1/notebooks/{notebook_id}")
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.delete(f"{UPSTREAM}/api/notebooks/{notebook_id}", headers={"Authorization": f"Bearer {ON_PASSWORD}"})
    return Response(content=r.content, status_code=r.status_code)

@app.post("/v1/notebooks/{notebook_id}/sources")
async def add_source(notebook_id: str, request: Request, agent=Depends(auth)):
    check_notebook(agent, notebook_id)
    body = await request.json()
    audit.info(f"{agent['name']} POST /v1/notebooks/{notebook_id}/sources")
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post(f"{UPSTREAM}/api/sources/json", json={**body, "notebook_id": notebook_id}, headers={"Authorization": f"Bearer {ON_PASSWORD}"})
    return Response(content=r.content, status_code=r.status_code)

@app.get("/v1/sources/{source_id}")
async def get_source(source_id: str, agent=Depends(auth)):
    # Verify the source belongs to an allowed notebook before returning details
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.get(f"{UPSTREAM}/api/sources/{source_id}", headers={"Authorization": f"Bearer {ON_PASSWORD}"})
        if r.status_code == 200:
            source = r.json()
            check_notebook(agent, source.get("notebook_id"))
        elif r.status_code == 404:
            pass  # let the 404 propagate — source doesn't exist
        else:
            r.raise_for_status()
    audit.info(f"{agent['name']} GET /v1/sources/{source_id}")
    return Response(content=r.content, status_code=r.status_code)

@app.delete("/v1/sources/{source_id}")
async def delete_source(source_id: str, agent=Depends(auth)):
    # Verify the source belongs to an allowed notebook before deleting it
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.get(f"{UPSTREAM}/api/sources/{source_id}", headers={"Authorization": f"Bearer {ON_PASSWORD}"})
        if r.status_code == 200:
            source = r.json()
            check_notebook(agent, source.get("notebook_id"))
        elif r.status_code == 404:
            return Response(content=r.content, status_code=404)
        else:
            r.raise_for_status()
        audit.info(f"{agent['name']} DELETE /v1/sources/{source_id}")
        r = await c.delete(f"{UPSTREAM}/api/sources/{source_id}", headers={"Authorization": f"Bearer {ON_PASSWORD}"})
    return Response(content=r.content, status_code=r.status_code)

@app.post("/v1/search")
async def search(request: Request, agent=Depends(auth)):
    body = await request.json()
    audit.info(f"{agent['name']} POST /v1/search")
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post(f"{UPSTREAM}/api/search", json=body, headers={"Authorization": f"Bearer {ON_PASSWORD}"})
    return Response(content=r.content, status_code=r.status_code)

@app.post("/v1/notebooks/{notebook_id}/chat")
async def ask(notebook_id: str, request: Request, agent=Depends(auth)):
    check_notebook(agent, notebook_id)
    body = await request.json()
    audit.info(f"{agent['name']} POST /v1/notebooks/{notebook_id}/chat")
    async with httpx.AsyncClient(timeout=120) as c:
        r = await c.post(f"{UPSTREAM}/api/ask", json={**body, "notebook_id": notebook_id}, headers={"Authorization": f"Bearer {ON_PASSWORD}"})
    return Response(content=r.content, status_code=r.status_code)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=BRIDGE_PORT)
```

### agents.json

```json
{
  "<your-agent-key>": {
    "name": "agent-name",
    "allowed_notebooks": "*",
    "readwrite": true
  }
}
```

### Bridge env vars

| Variable | Description |
|---|---|
| `OPEN_NOTEBOOK_PASSWORD` | Password for the open-notebook API (from open-notebook .env) |
| `AGENTS_FILE` | Path to agents.json (default: `agents.json`) |
| `BRIDGE_PORT` | Port to listen on (default: `5077`) |

## How to use

Use the `exec` tool to run `{baseDir}/scripts/on.sh`. All commands return JSON.

| Command | Purpose |
|---|---|
| `on.sh health` | Bridge + upstream liveness |
| `on.sh list-notebooks` | List allowed notebooks |
| `on.sh get-notebook <id>` | Notebook details |
| `on.sh create-notebook "Title" "Description"` | Create a new notebook |
| `on.sh add-source <nb-id> --text "..."` | Add a source (also `--url` / `--file`, optional `--title`) |
| `on.sh get-source <id>` | Check source processing status |
| `on.sh search "natural language query"` | Cross-notebook vector search |
| `on.sh ask <nb-id> "Question?"` | RAG answer with citations, one notebook |
| `on.sh delete-source <id>` | ⚠️ Remove a source (irreversible) |
| `on.sh delete-notebook <id>` | ⚠️ Remove a notebook (irreversible) |

## Conventions

- Notebooks are referenced by their `id` (e.g. `notebook:v9px33nuskufk4snelyt`). When the user says a name, call `list-notebooks` first to resolve.
- `search` is fast and cross-notebook (uses the embedding model). Use it for "find anything I saved about X".
- `ask` is slower, scoped to one notebook, and returns a synthesized answer with citations. Use it for "summarize what I know about X".
- Adding a source is **async** on the upstream side. The `add-source` call returns the new source ID, but embedding/processing happens in the background. Poll with `get-source <id>` until `status` is `processed` or `completed` before relying on the source for `ask` or `search`.

## Errors and recovery

| Symptom | Likely cause | Fix |
|---|---|---|
| `bridge unreachable` (connection refused) | Bridge service down | Restart the bridge service |
| HTTP 401 `{"detail":"missing X-API-Key header"}` | `OPEN_NOTEBOOK_API_KEY` not set | Verify the var is in `~/.openclaw/.env` and restart the gateway |
| HTTP 401 `{"detail":"invalid api key"}` | Wrong key | Compare to your agents.json |
| HTTP 403 `agent ... not allowed to access ...` | This agent's allowlist excludes the notebook | `list-notebooks` to see what this agent can see |
| HTTP 404 | Bad notebook ID | Re-list notebooks to get the correct ID |
| HTTP 500 (get-source) | Bad source ID | Upstream returns 500 for non-existent source IDs  -  verify the source exists before polling |
| Timeout on `ask` (>120s) | Upstream LLM call slow | Narrow the question |

## Privacy

Notebook data (sources, notes, chat, embeddings, files) is **not encrypted at rest** in the upstream open-notebook stack  -  only LLM API keys are encrypted. Do not put secrets, credentials, or sensitive PII into a notebook.

## Files

- `{baseDir}/scripts/on.sh`  -  bridge client (bash, curl + jq with python3 fallback)
- Bridge service: runs locally on port 5077; audit log path is deployment-specific
- Per-agent key registry: deployment-specific path (set during bridge setup)
