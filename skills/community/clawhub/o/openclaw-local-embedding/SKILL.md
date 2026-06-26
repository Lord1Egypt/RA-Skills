---
name: openclaw-local-embedding
description: Initialize and configure OpenClaw local embedding mode on CPU-only machines. Handles network probe, proxy fallback, GGUF model download, cmake/llama.cpp compilation, openclaw.json configuration, and gateway restart. Use when a user wants to enable memory search with local embedding on a machine without GPU, especially when direct internet access is unavailable and an HTTP CONNECT proxy is required.
---

# OpenClaw Local Embedding Setup

Use this skill to enable local embedding for OpenClaw memory search on machines where outbound internet access is restricted to an HTTP CONNECT proxy. Do not use this skill for remote embedding providers (OpenAI, Gemini, Voyage, etc.) or for machines with direct internet access.

## Target environment

- Any Linux machine (cloud VM, on-premises server, or development workstation).
- CPU-only (no GPU required; embedding model is small enough for CPU inference).
- No direct internet access; outbound HTTPS requires an HTTP CONNECT proxy.
- OS: Ubuntu 20.04+ (GLIBC 2.31+).
- Node.js 22+ (required for `NODE_USE_ENV_PROXY` support).
- OpenClaw installed via `npm install -g openclaw` (no source build required).

## Workflow

Follow these steps in order. Do not skip steps.

### Step 1: Check if model is already cached

The default model is `embeddinggemma-300m-qat-Q8_0.gguf` (~313 MB). Check the standard cache directories:

```bash
MODEL_FILE="hf_ggml-org_embeddinggemma-300m-qat-Q8_0.gguf"
for dir in "$HOME/.node-llama-cpp/models" "$HOME/.cache/node-llama-cpp/models"; do
  if [ -f "$dir/$MODEL_FILE" ]; then
    SIZE_MB=$(du -m "$dir/$MODEL_FILE" | cut -f1)
    echo "Model already cached: $dir/$MODEL_FILE ($SIZE_MB MB)"
  fi
done
```

If the model exists and is larger than 100 MB, skip to Step 4 (configuration).

### Step 2: Resolve network and proxy

The model must be downloaded from HuggingFace. Machines without direct internet access need an HTTP CONNECT proxy.

#### Known proxy defaults

| Platform | Proxy address |
|----------|--------------|
| Kuaishou cloud VMs (快手云主机) | `http://10.74.176.8:11080` |

If the machine is a Kuaishou cloud VM and no proxy is configured, try the default above first. If a different proxy was used previously and recorded in `~/.openclaw/workspace/skills/openclaw-local-embedding/.proxy`, load it automatically:

```bash
RECORDED_PROXY=$(cat ~/.openclaw/workspace/skills/openclaw-local-embedding/.proxy 2>/dev/null)
```

**Strategy: progressive fallback.**

1. **Test current environment first** — the user may already have `HTTPS_PROXY` or a recorded proxy configured:

```bash
# Quick connectivity test (5s timeout)
curl -sI --connect-timeout 5 https://huggingface.co -o /dev/null -w "%{http_code}"
```

2. **If direct access fails, try proxies in this order:**

   a. Recorded proxy from previous run (`.proxy` file, see above).

   b. Kuaishou cloud default: `http://10.74.176.8:11080`

   ```bash
   curl -sI --connect-timeout 5 --proxy http://10.74.176.8:11080 https://huggingface.co -o /dev/null -w "%{http_code}"
   ```

   c. If neither works, **ask the user for their proxy address**.

3. **Once a working proxy is confirmed**, record it for future runs:

```bash
mkdir -p ~/.openclaw/workspace/skills/openclaw-local-embedding
echo "http://the-working-proxy:port" > ~/.openclaw/workspace/skills/openclaw-local-embedding/.proxy
```

Then set it **only for the download process** (not permanently):

```bash
export HTTPS_PROXY="http://the-working-proxy:port"  # use the confirmed proxy address
export HTTP_PROXY="$HTTPS_PROXY"
export NODE_USE_ENV_PROXY=1
export NODE_TLS_REJECT_UNAUTHORIZED=0  # set only if the proxy performs TLS inspection (MITM)
```

These environment variables are process-scoped. They do not affect other processes or the gateway.

**Important:** `NODE_TLS_REJECT_UNAUTHORIZED=0` disables TLS certificate verification. Only set it in the download script/process. Never persist it to shell profiles.

### Step 3: Download and verify model

The skill includes a helper script (`scripts/init-model.mjs`) that handles proxy detection, model download, and verification automatically. Run it with the proxy env vars from Step 3 active (or let the script auto-detect):

```bash
# The script is in the skill folder (default clawhub install location):
node ~/.openclaw/workspace/skills/openclaw-local-embedding/scripts/init-model.mjs

# To override proxy explicitly:
node ~/.openclaw/workspace/skills/openclaw-local-embedding/scripts/init-model.mjs --proxy http://your-proxy:port
```

The script will:
1. Auto-detect the OpenClaw installation directory
2. Check if the model is already cached (idempotent — safe to re-run)
3. Probe network connectivity (recorded proxy → env proxy → direct → Kuaishou cloud default)
4. Record a working proxy to `.proxy` for future runs
5. Download the model via `node-llama-cpp`'s `resolveModelFile`

Expected download size: ~313 MB. Speed through proxy: ~5–10 MB/s.

#### cmake troubleshooting

If `node-llama-cpp` cannot find a prebuilt binary (common on Ubuntu 20.04 with GLIBC < 2.32), it falls back to compiling `llama.cpp` from source. This requires cmake >= 3.19.

Check cmake version:

```bash
cmake --version
```

If cmake is < 3.19, install a newer version:

```bash
pip3 install cmake
# Verify: cmake --version should show >= 3.19
```

After cmake is available, re-run the model download. The compilation is automatic and one-time.

### Step 4: Configure openclaw.json

`openclaw config set` (dot-notation path assignment) is a long-standing core feature available in all OpenClaw versions. Use it to apply settings and then verify:

```bash
openclaw config set agents.defaults.memorySearch.enabled true
openclaw config set agents.defaults.memorySearch.provider local
openclaw config set agents.defaults.memorySearch.fallback none
openclaw config set agents.defaults.memorySearch.query.hybrid.enabled true
```

**Verify the result** — the output must show all four fields set correctly:

```bash
openclaw config get agents.defaults.memorySearch
```

Expected output:
```json
{
  "enabled": true,
  "provider": "local",
  "fallback": "none",
  "query": { "hybrid": { "enabled": true } }
}
```

Also run `openclaw config validate` to confirm the full config is well-formed. If it reports errors, fix them before proceeding.

**If `config set` fails** (e.g., exits with a non-zero code or `config get` shows wrong values), fall back to direct JSON editing. Open `~/.openclaw/openclaw.json` and manually add the block under `agents.defaults`:

```json5
// Inside the existing "agents" → "defaults" object:
"memorySearch": {
  "enabled": true,
  "provider": "local",
  "fallback": "none",
  "query": {
    "hybrid": {
      "enabled": true
    }
  }
}
```

Do not set `memorySearch` at the top level. It must be nested under `agents.defaults`.

After manual editing, validate JSON syntax: `openclaw config validate`

### Step 5: Restart gateway

The configuration change requires a gateway restart. Use the standard OpenClaw command:

```bash
openclaw gateway restart
```

This works regardless of how OpenClaw was installed (systemd, launchd, or Windows service). If the gateway is not registered as a supervised service, run it manually in foreground instead:

```bash
openclaw gateway run
```

### Step 6: Verify

After restart, the first `memory_search` tool call triggers model loading (~1.6 seconds, one-time). Subsequent calls use the in-memory model with no network access.

Check gateway status:

```bash
openclaw gateway status
```

For deeper log inspection, use your system's service log viewer:

```bash
# systemd (Linux):
journalctl --user -u openclaw-gateway -n 50 | grep -i "embed\|memory\|llama"

# macOS launchd:
log show --predicate 'subsystem == "ai.openclaw"' --last 2m | grep -i "embed\|llama"
```

## Resource expectations

| Metric | Value |
|--------|-------|
| Model file on disk | ~313 MB |
| Cold start (model load) | ~1.6 seconds (one-time per gateway start) |
| RSS after model load | ~880 MB |
| Per-chunk embedding latency | ~500 ms (400-token chunk, CPU) |
| Minimum available RAM | 2 GB (recommended: 4+ GB) |
| GPU required | No |
| Network required after setup | No (fully offline inference) |

## Common issues

### Model download hangs or times out

- Verify proxy reachability: `curl --proxy "$HTTPS_PROXY" https://huggingface.co`
  (If `HTTPS_PROXY` is not set, try the Kuaishou cloud default: `curl --proxy http://10.74.176.8:11080 https://huggingface.co`)
- Check if a proxy was recorded from a previous run: `cat ~/.openclaw/workspace/skills/openclaw-local-embedding/.proxy`
- Ensure `NODE_USE_ENV_PROXY=1` is set in the download process.
- If the download still fails with TLS errors, set `NODE_TLS_REJECT_UNAUTHORIZED=0` — this is needed when the proxy performs TLS inspection (common in corporate/cloud environments).

### llama.cpp compilation fails

- Check cmake version: must be >= 3.19. Fix: `pip3 install cmake`.
- Check GCC: must be >= 9. Ubuntu 20.04 ships GCC 9.4 which is sufficient.
- Compilation is automatic and happens only once. The built binary is cached at `<openclaw-node-modules>/node-llama-cpp/llama/localBuilds/`.

### GLIBC version mismatch

The prebuilt `node-llama-cpp` binary requires GLIBC >= 2.32. Ubuntu 20.04 has GLIBC 2.31. When this happens, `node-llama-cpp` automatically falls back to source compilation (requires cmake >= 3.19).

### Gateway crash or high memory after enabling

- RSS of ~880 MB is expected and stable. The model weights are memory-mapped.
- If the machine has less than 2 GB available RAM, do not enable local embedding. Use a remote provider instead.
- Memory does not grow over time — the model is loaded once and reused.

## Security notes

- Never persist `NODE_TLS_REJECT_UNAUTHORIZED=0` in shell profiles or system-wide configuration. It disables TLS verification for all Node.js processes.
- The proxy environment variables (`HTTPS_PROXY`, `NODE_USE_ENV_PROXY`) should only be set in the download script, not in the gateway runtime.
- After model download completes, the gateway runs fully offline. No proxy or network configuration is needed.
