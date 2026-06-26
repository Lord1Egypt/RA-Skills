# Security and architecture

## Purpose

Use this reference to explain the deployment shape and the main operational risks before or during setup.

## Target architecture

Deploy Proxima on a remote Ubuntu VPS with:
- repo at `/Proxima`
- dedicated runtime user `proxima`
- Electron app managed by systemd
- virtual desktop on display `:2`
- VNC on `127.0.0.1:5902`
- noVNC on `127.0.0.1:6081`
- REST on `127.0.0.1:3210`
- internal Proxima IPC on `127.0.0.1:19222`
- MCP exposed only through SSH stdio via `proxima-mcp`

The user accesses GUI and REST through SSH local-forwarding and accesses MCP by running:

```bash
ssh -T <ssh-host-alias> proxima-mcp
```

## Risk framing

Use this wording model when asked whether Proxima is safe:
- downloading the source is relatively low risk
- running it on a primary laptop is not recommended
- testing on an isolated VPS or VM is more acceptable
- it does not look like a classic obvious backdoor from the reviewed code path, but it is still high-risk operational software

## Important audit notes

These were the highest-value findings from the prior review of the repository:
- a TLS certificate validation bypass exists in the Electron app for certain AI domains
- dependencies are dated enough to matter
- the app can read local files, store session cookies, and send data to providers by design
- localhost control surfaces exist and should stay private

Do not describe the app as fully safe. Describe it as manageable only with isolation and tight exposure boundaries.

## Model-routing caveat

`/v1/models` in Proxima mainly exposes provider aliases such as:
- `chatgpt`
- `claude`
- `gemini`
- `perplexity`
- `auto`

Do not present that endpoint as proof of the exact underlying premium model the provider is using.

Important source-level caveats already observed:
- ChatGPT engine uses `model: 'auto'`
- Perplexity engine uses `model_preference: 'turbo'`
- Claude and Gemini are not pinned to stable exact model slugs in the reviewed code path

So when a user asks for exact premium model pinning, explain that Proxima is stronger at provider routing than exact model control.

## Non-negotiable deployment rules

- Do not run Electron as root.
- Do not disable Chromium sandbox just to force root execution.
- Do not bind REST, VNC, noVNC, or MCP to `0.0.0.0` unless the user explicitly asks and understands the risk.
- Do not expose MCP as a public TCP port when SSH stdio works.
- Prefer SSH keys for local IDE access because password prompts break many MCP clients.
