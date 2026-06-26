# Agent = Hermes Agent (via hermes acp)

Handler command:

```bash
linkedclaw provider run my-provider.yaml --handler-acp "hermes acp"
```

`hermes acp` is Hermes Agent's native ACP server (stdio JSON-RPC), the same mode Zed /
VS Code / JetBrains drive. The daemon spawns one instance per job.

## Credential

Hermes reads its model credential and config from `~/.hermes` (set up once with
`hermes setup` / `hermes login`). The daemon reaches it via `HOME` — no LinkedClaw env var
is passed to the agent.

## How tools are confined — IMPORTANT: default is NOT safe

**`hermes acp` uses a hardcoded `hermes-acp` toolset** that always includes
`terminal`, `process`, and `execute_code`. This toolset is defined in the installed
Hermes source (`~/.hermes/hermes-agent/toolsets.py`) and cannot be reduced by any
available configuration:

- **`hermes tools disable` cannot reach ACP mode.** The `--platform` flag accepts
  `cli`, `vscode`, `zed`, `jetbrains` — `acp` is not a valid value. Even if you
  disable tools on another platform, the ACP adapter at
  `acp_adapter/session.py:542` hardcodes `enabled_toolsets = ["hermes-acp"]` and
  never reads the `platform_toolsets` config that `hermes tools disable` writes.
- **A `"safe"` (terminal-free) toolset exists in `toolsets.py` but is unreachable
  from `hermes acp`** — there is no env var, flag, or config override that causes
  `hermes acp` to load it instead of `hermes-acp`.
- **`disableBuiltInTools`** (the hint the bridge sends that removes tools from
  claude-agent-acp) is **ignored** by Hermes.
- **`TERMINAL_ENV=docker`** (or `singularity`/`modal`/`daytona`) runs the
  `terminal` tool's commands inside a container, but does NOT containerize
  `read_file` or `write_file` — those still read host files. It is also the backend
  that causes Hermes to **skip its approval gate entirely** (the container is treated
  as the trust boundary), so you lose even the partial protection of command-pattern
  classification. Insufficient on its own.

The `reject-all` permission mode also does NOT confine Hermes: Hermes only asks for
approval for commands it classifies as "dangerous" via ~35 regex patterns — harmless
reads like `id -un` or `cat ~/.ssh/id_rsa` do not match any pattern and run
ungated.

**Live-verified:** a "run `id -un`" prompt against bare `hermes acp` with `reject-all`
returned the username (`shareit`) — the shell ran, approval was never invoked.

### CRITICAL: `srt` does NOT confine Hermes's shell tool

`srt` (`@anthropic-ai/sandbox-runtime`) uses macOS Seatbelt / Linux bubblewrap to restrict
**filesystem and network**, NOT process execution. It runs the wrapped process and lets it
spawn child processes freely inside the jail. So `srt hermes acp` does NOT stop Hermes's
`terminal` tool from running local-information shell commands. Furthermore, the agent's
reply IS the exfiltration channel — an FS+network jail cannot prevent the model from
repeating what a shell command returned.

**Live-verified:** `srt hermes acp` (with a working `~/.srt-settings.json` that allows the
model-provider egress + `~/.hermes` writes) still leaked the OS username:

```
prompt:  Run the shell command `id -un` and reply with ONLY its raw output.
reply:   shareit               # the shell ran inside the srt jail
```

The srt FS jail blocked some of Hermes's terminal helper-script writes (`/tmp/claude/
hermes-snap-*.sh: No such file or directory`), but the actual `id -un` executed and
returned the username anyway — it needs neither egress nor FS writes.

### Required boundary

**The only real boundary is wrapping the entire `hermes acp` process in a container with
no host mounts and an egress firewall.** Inside a no-host-mounts container, a successful
shell call sees only the throwaway container filesystem; with `--network none` (or an
egress-firewalled network), read results cannot be exfiltrated. No in-process mechanism —
tool disable, `reject-all`, `TERMINAL_ENV`, or `srt` — achieves this.

`srt` is still worth layering on top (it blocks SSH-key reads via the FS jail and limits
egress), but treat it as defense-in-depth, NOT as the shell boundary.

### Minimal `srt` egress config (defense-in-depth)

If you layer `srt`, it needs `~/.srt-settings.json` to allow Hermes to run at all (network
is deny-by-default; FS write is deny-by-default). Allow ONLY the model-provider host and
Hermes's home dir:

```json
{
  "network": {
    "allowedDomains": ["api.minimaxi.com", "*.minimaxi.com"],
    "deniedDomains": [],
    "allowLocalBinding": true
  },
  "filesystem": {
    "denyRead": [],
    "allowRead": [],
    "allowWrite": ["~/.hermes", "/tmp", "/var/folders", "."],
    "denyWrite": []
  }
}
```

Replace `api.minimaxi.com` with whatever model provider your `~/.hermes/config.yaml` points
at. `denyRead`/`deniedDomains`/`allowRead` are REQUIRED keys (srt rejects the config and
falls back to deny-all if any are missing). Without the egress allow, the model call fails;
without the `~/.hermes` write allow, Hermes crashes writing its log.

Two more rules, both load-bearing for an unattended provider:
- **NEVER pass `--accept-hooks`** (or set `HERMES_ACCEPT_HOOKS=1` / `hooks_auto_accept: true`).
  It auto-approves unseen shell hooks without a TTY prompt — i.e. it lets a stranger's prompt
  run shell. Without this flag, shell *hooks* (pre-registered scripts) are not auto-approved
  headless; but note this does NOT prevent the terminal *tool* from running (the approval
  gate for tools is command-classification based, not hook-based).
- **NEVER pass `--yolo`** — it bypasses all approval.

## Text-only capabilities: disable Hermes tools via AGENTS.md

For text-in/text-out capabilities that do not need any tools, add an instruction to
the project's `AGENTS.md` (which Hermes injects into every session — confirmed via
`hermes --help`: `--ignore-rules` "Skip auto-injection of AGENTS.md"):

```markdown
You are running as an unattended marketplace provider. Do NOT use the terminal,
process, execute_code, browser, or file tools — respond with text only.
```

This is a prompt-level instruction (honor-system), not a hard boundary. For any
capability where a stranger's prompt might override it, use the OS sandbox instead.

## Verified behaviors (live run)

- **Round-trip text prompt:** PASS — `hermes acp` responds correctly to a plain
  text prompt via ACP JSON-RPC (both bare and under `srt`).
- **Shell-attempt without sandbox:** UNSAFE — `id -un` prompt executed and returned
  the OS username (`shareit`). Default headless `hermes acp` without `--accept-hooks`
  does NOT prevent the terminal tool from running non-dangerous commands.
- **Shell-attempt with `srt hermes acp` (FS+network sandbox):** STILL UNSAFE — `id -un`
  executed and returned the username inside the srt jail. `srt` restricts filesystem +
  network, not process execution. A filesystem+network sandbox alone does not confine
  Hermes's shell tool. (See the CRITICAL section above.)

## Container boundary (required for all capabilities)

Run `hermes acp` inside a container with no host mounts and an egress firewall (see
"Required boundary" above for the why):

```bash
linkedclaw provider run my-provider.yaml \
  --handler-acp "docker run --rm -i --network none ... your-hermes-image hermes acp"
```

Optionally layer `srt` on top for extra FS/egress hardening, but do not rely on it as the
shell boundary. The CLI warns if you keep agent tools without a detected sandbox wrapper.

## Notes

- The daemon returns only the final message text to the buyer; Hermes's tool-call / thought
  stream updates are ignored.
- `hermes tools disable terminal --platform cli` disables the terminal for interactive
  CLI use but has no effect on ACP mode — do not rely on it for provider security.
- V3 confirmed: Hermes reads `AGENTS.md` for project instructions (same cross-tool
  convention as Codex). `hermes --help` shows `--ignore-rules` "Skip auto-injection of
  AGENTS.md, SOUL.md, .cursorrules, memory, and preloaded skills".
