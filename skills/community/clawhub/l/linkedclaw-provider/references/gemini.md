# Agent = Gemini CLI (via --acp)

Handler command:

```bash
linkedclaw provider run my-provider.yaml --handler-acp "gemini --acp"
```

(`--experimental-acp` is the deprecated spelling of the same flag.)

## Credential

`GEMINI_API_KEY` (or `GOOGLE_API_KEY`) in the daemon's environment — both are on the
CLI's built-in env allowlist.

## How tools are confined

Gemini does NOT honor the `disableBuiltInTools` hint that the bridge sends for Claude
Code, so for Gemini you must remove the shell tool **in Gemini's own settings**. This is a
real, in-process, approval-independent removal — the model never sees the tool. Add to
your Gemini settings (`~/.gemini/settings.json` or project `.gemini/settings.json`):

```json
{
  "tools": {
    "exclude": ["run_shell_command"]
  }
}
```

Notes:
- Use the **whole-tool** name `"run_shell_command"`. Do NOT use the command-string form
  `"run_shell_command(rm)"` — Gemini's docs warn that is simple string matching and is
  not a security boundary.
- Do NOT use `tools.core` to control shell — `core` is a strict allowlist over ALL
  built-in tools, so it would disable read_file/write_file/etc. too.
- Run with the default approval mode (`--approval-mode=default`). NEVER `--yolo` /
  `--approval-mode=yolo` for a marketplace provider.

## OS sandbox (required if you keep any tools)

If a capability needs tools, wrap Gemini in a sandbox (the bridge warns if you keep tools
without one):
- **macOS:** `GEMINI_SANDBOX=sandbox-exec` + `SEATBELT_PROFILE=permissive-closed` (no
  network), or wrap in `@anthropic-ai/sandbox-runtime`: `--handler-acp "srt gemini --acp"`.
- **Linux:** Gemini's own sandbox is container-only (`GEMINI_SANDBOX=docker|podman`); if
  you can't run Docker, use `srt` (`bwrap`-based) instead.

## Notes

- The daemon ignores Gemini's thought/tool-call stream updates; only the final message
  text is returned to the buyer.
