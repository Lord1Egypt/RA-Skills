# Agent = OpenCode (via opencode acp)

Handler command:

```bash
linkedclaw provider run my-provider.yaml --handler-acp "opencode acp"
```

`opencode acp` is a **tier-1 native** stdio JSON-RPC ACP server (OpenCode v1.4.7+, protocol
version 1). It speaks the same wire protocol as `gemini --acp` and `hermes acp` — no adapter
wrapper is needed.

## Credential

OpenCode's model-selection is separate from credentials:

| Model family | Credential |
|---|---|
| `opencode/*` hosted models (`opencode/big-pickle`, etc.) | No credentials — authenticated through an `opencode auth login` session stored under `~/.local/share/opencode/` (HOME is on the env allowlist, so the session is accessible). Free models work with no setup. |
| `google-vertex/*` models | `GOOGLE_APPLICATION_CREDENTIALS` (path to a service-account JSON) + `GOOGLE_VERTEX_LOCATION` + `GOOGLE_VERTEX_PROJECT`. All three are required; missing any one causes a hard error (`AI_LoadSettingError`). |
| `anthropic/*` / OpenAI / other | `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` (already on the built-in allowlist). |

`GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_VERTEX_LOCATION`, and `GOOGLE_VERTEX_PROJECT` are NOT
on the built-in allowlist — pass them via `--acp-env`:

```bash
linkedclaw provider run my-provider.yaml \
  --handler-acp "opencode acp" \
  --acp-env GOOGLE_APPLICATION_CREDENTIALS \
  --acp-env GOOGLE_VERTEX_LOCATION \
  --acp-env GOOGLE_VERTEX_PROJECT
```

(Or set them as environment variables in the daemon process; `GOOGLE_APPLICATION_CREDENTIALS`
and `OPENCODE_API_KEY` are on the built-in allowlist — no `--acp-env` needed for those two.)

## Model selection

OpenCode reads the model from **`opencode.json`** in the working directory (or any parent).
The ACP worker uses a fresh per-job workspace dir; write the config there:

```json
{
  "model": "opencode/big-pickle"
}
```

All valid model IDs are returned in the `session/new` response under `models.availableModels`.

If no `opencode.json` is found, OpenCode falls back to the last model the user selected
interactively (persisted in `~/.local/share/opencode/opencode.db`).

## How tools are confined (read this — it's the load-bearing part)

**`--acp-permissions reject-all` does NOT confine OpenCode — you MUST set `permission.bash`
in `opencode.json`.** This is the same "own-config confinement" pattern as Gemini.

OpenCode's bash tool runs through its **own internal permission loop** (`permission.bash` in
`opencode.json`), NOT through the ACP permission channel. Therefore `reject-all` and
`_meta.disableBuiltInTools` have no effect on OpenCode's shell execution.

**Verified against the real agent (opencode/big-pickle, opencode v1.4.7, 2026-06-23):**
running under `--acp-permissions reject-all` AND `_meta.disableBuiltInTools`, the prompt
"Run the shell command `id -un` and reply with ONLY its raw output" **executed the shell** —
the reply contained the host OS username. The in-band ACP permission mode is NOT a security
boundary for OpenCode.

To confine OpenCode, disable bash in **OpenCode's own config**:

```json
{
  "model": "opencode/big-pickle",
  "permission": {
    "bash": "deny"
  }
}
```

Write this `opencode.json` into the per-job workspace directory that the ACP worker uses as its
`--cwd`. Options `"ask"` / `"allow"` / `"deny"` — use `"deny"` for marketplace providers (the
model is then text-in/text-out and cannot touch the host).

The permission block also controls `"edit"` (file writes) and `"webfetch"` (HTTP):

```json
{
  "model": "opencode/big-pickle",
  "permission": {
    "bash": "deny",
    "edit": "deny",
    "webfetch": "deny"
  }
}
```

For a text-only marketplace capability (review, analysis, translation) this locks the agent
down completely.

## OS sandbox (required if you keep any tools)

If a capability genuinely needs file or network access, keep `"permission": {"bash": "deny"}`
(never give shell), AND additionally wrap the whole process in
`@anthropic-ai/sandbox-runtime` (`srt`) with a default-deny egress allowlist:

```bash
linkedclaw provider run my-provider.yaml \
  --acp-permissions allow-reads \
  --handler-acp "srt opencode acp"
```

The CLI warns if you keep tools without a detected sandbox wrapper. See
[security.md](security.md) for the full rationale.

## Notes

- OpenCode maintains a per-user SQLite database at `~/.local/share/opencode/opencode.db`.
  `HOME` is on the env allowlist, so the daemon's process can reach it. Do NOT share a
  database path across concurrent workers — OpenCode handles its own session isolation.
- The `opencode.json` config merges from parent directories. Writing it in the per-job workspace
  cwdBase (parent of the per-job sub-dir) is sufficient; you do not need to mutate the user's
  global `~/.config/opencode/` config.
- OpenCode uses `agent_message_chunk` session updates for streaming text (same as other ACP
  agents). Thought chunks (`agent_thought_chunk`) are silently discarded by the bridge.
