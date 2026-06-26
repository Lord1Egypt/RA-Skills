# openclaw-agent-compute

Public Clawdbot/OpenClaw skill that exposes `compute.*` tools by calling a **private** Compute Gateway over **HTTPS**.

## Install

### Option A — ClawdHub

```bash
clawdhub install openclaw-agent-compute
```

### Option B — from GitHub (dev)

```bash
git clone https://github.com/aleksandrkrivolap/openclaw-agent-compute-skill
cd openclaw-agent-compute-skill
npm i
```

## Configuration

Copy the example env file and set:

- `MCP_COMPUTE_URL` — base URL of your Compute Gateway (e.g. `https://compute.example.com`)
- `MCP_COMPUTE_API_KEY` — Bearer token

```bash
cp .env.example .env
# edit .env
```

## Smoke test

From this folder:

```bash
npm i
npm run lint
npm run example:exec
```

## Artifacts (planned)

The private gateway contract also includes artifact upload/download/list endpoints. The client exports helper functions:

- `computeArtifactsList({ session_id })`
- `computeArtifactPut({ session_id, path, bytes })`
- `computeArtifactGet({ session_id, path })`
- `computeArtifactDelete({ session_id, path })`

## Repository

https://github.com/aleksandrkrivolap/openclaw-agent-compute-skill
