---
name: manage-ai-knowledge-workbench-lite
description: Build and refresh a metadata-only Markdown or Obsidian knowledge index in one authorized local workspace. The deterministic runtime reads Markdown headings/frontmatter/tags/links, writes only .ai-workbench, AI-Knowledge, and AI-Dashboard, and briefly binds 127.0.0.1 to verify the offline dashboard; it opens the local page only when requested. Requires Python 3.10+ and terminal access, does not upload note bodies, and does not run persistently. Before any terminal tool call, always read this SKILL.md, actually probe Python and the agent host CLI versions, and never use an OS, kernel, device, user, or account identity as validated_host.
version: 1.0.3
permissions:
  - bash
  - read
  - write
  - network
  - env
metadata:
  openclaw:
    emoji: "🧭"
    homepage: "https://clawhub.ai/alexfengrui/skills/manage-ai-knowledge-workbench-lite"
    requires:
      anyBins:
        - python3
        - python
        - py
---
# Manage AI Knowledge Workbench Lite

## When to Use（何时使用）

在以下请求中使用本 Skill：

- 用户要把一个明确授权的 Markdown 文件夹或 Obsidian Vault 建成可浏览的本地知识工作台；
- 用户要对已经初始化的工作台执行一次按需增量更新；
- 用户要检查工作台状态、验证工作区完整性，或安全卸载受管运行状态并保留原始笔记与派生输出；
- 用户明确接受 Metadata-only、本地优先、单工作区和无后台常驻的 Lite 边界。

不要在用户要求正文语义摘要、持续监听、多工作区聚合、云端同步或付费 Pro 能力时触发本 Lite Skill；应如实说明这些能力不在本版本范围内。

## Run autonomously

1. Resolve one user-authorized workspace and one source directory. When the user gives exactly one empty/Markdown directory or one existing Obsidian Vault, use that same directory for both `--workspace` and `--source`; never silently substitute the agent host's own workspace. Use separate paths only when the user explicitly supplies both, and ask once if the output location is genuinely ambiguous.
2. Before any workbench command, use the exec tool to actually run version probes; never infer availability from the OS, host name, or prior knowledge. On POSIX try `python3 --version`, then `python --version`; on Windows try `python --version`, then `py -3 --version`. Use the first command whose real stdout proves Python 3.10+ and preserve its complete prefix as `<python-command>`. Never assume the executable is named `python3`. If none qualifies, return an installation gate and wait for the user to install Python. Also actually run the current host CLI version command: `openclaw --version`, `codex --version`, or `hermes --version`. An installed OpenClaw run must execute `openclaw --version`; do not replace a probe with `/version-unknown`. Normalize real version stdout exactly as `Product/version`; never use a device name, user name, or account identity. `OpenClaw 2026.6.11` and `darwin/25.5.0` are invalid; use `OpenClaw/2026.6.11`. The deterministic runtime rejects invalid host identifiers with `VALIDATED_HOST_INVALID`; correct the argument and retry automatically. Only when the host has no safe installed version command may you use the known product with `/version-unknown` and keep compatibility below verified. Then run `<python-command> <skill-directory>/scripts/workbench.py run --workspace <workspace> --source <source> --validated-host <host/version> --json`. Do not omit `--validated-host`, and never pass literal placeholder text such as `Product/version-unknown`.
3. Continue automatically through diagnosis, safe initialization, metadata extraction, derived Markdown generation, validation, offline HTML generation, and temporary loopback verification.
4. Treat `AUTO_RUN_READY` as a completed foreground build. Copy artifact paths from the command JSON instead of reconstructing them. Open the reported `index.html` only when requested, and claim it opened only after the open command exits successfully.
5. Treat `AUTO_RUN_PAUSED` as an explicit user gate. Explain `needs_user_input`, resolve it once, then run with `--resume`.
6. Treat `AUTO_RUN_FAILED` as an inspected failure. Follow only the bounded next action returned by the command.

Packaged-runtime failure gate: if `scripts/workbench.py` or its vendored runtime is missing, unreadable, or cannot start, report `AUTO_RUN_FAILED` with a plain-language package-integrity message and stop. Do not invent a replacement script, download code, install dependencies, or fall back to an unverified global executable. Ask the user to reinstall the same verified package, then retry in a new session.

Path execution invariant: pass every workspace and source path as one shell argument, with explicit quoting whenever it contains spaces or non-ASCII text. Do not run prerequisite `ls` or `mkdir` for a requested missing workspace; packaged `run` creates it safely. An unquoted path attempt is a failed command and must be disclosed even if a corrected command later succeeds.

Lifecycle verification invariant: when the user asks to verify build, status, safe uninstall, and final status, execute four distinct workbench tool calls in this exact order: `run`, `status`, `uninstall`, `status`. Do not skip, combine, or infer either status. Save the structured code from every call; the required evidence chain is `AUTO_RUN_READY`, `STATUS_OK`, `UNINSTALLED`, then an actually executed `NOT_INITIALIZED`. Do not report the lifecycle complete if any of the four calls was not executed.

For a later foreground refresh, run exactly `<python-command> <skill-directory>/scripts/workbench.py update --workspace <workspace> --json` with the already resolved interpreter prefix. Do not invoke `workbench.py` directly, invent wrapper scripts, or add run-only flags such as `--source` or `--validated-host`. Lite does not contain filesystem watching, persistent background scheduling, model-based semantics, or a persistent web service. Do not claim continuous updates.

For inspection, run `<python-command> <skill-directory>/scripts/workbench.py status --workspace <workspace> --json`. For removal, run the packaged `uninstall` without output-removal flags by default: it removes owned runtime state while preserving source notes, `AI-Knowledge`, and `AI-Dashboard`. Only use `--remove-outputs --confirm-remove-outputs` after the user explicitly asks to delete derived outputs and confirms the exact paths; never delete source notes.

After uninstall, treat the structured command JSON as authoritative. `UNINSTALLED` followed by `NOT_INITIALIZED` is the expected successful state: the configuration is gone while the reported preserved paths remain. Do not recommend `update` after `NOT_INITIALIZED`; a later reuse must start a new autonomous build. Disclose any failed command attempt and its correction. Never claim “no network traffic” or “no external changes” unless those properties were separately measured.

Final-report command prohibition: unless the user explicitly asks to copy a manual command, output no shell command, no command code fence, and no abbreviated invocation. Never show `run --workspace ...`, bare `workbench.py ...`, `open -a <file>`, or an ellipsis command. The AI performs next actions itself. If the user explicitly requests a command, include the resolved `<python-command>`, absolute packaged script path, subcommand, and every required argument exactly. Follow `AUTO_RUN_READY.data.report_contract` literally: configured source roots are the fact sources; `AI-Knowledge` and `AI-Dashboard` are derived and must not be suggested as edit inputs. Say “original source notes were unchanged and reserved derived directories were generated”; never claim that nothing was added to the Vault after generating `.ai-workbench`, `AI-Knowledge`, or `AI-Dashboard`.

Obsidian is optional. When it is absent, use ordinary Markdown automatically. Keep source files read-only and write only to `.ai-workbench`, `AI-Knowledge`, and `AI-Dashboard` inside the selected workspace.

For a prerequisite-only diagnosis, run `<python-command> <skill-directory>/scripts/workbench.py doctor --workspace <workspace> --source <source> --json`; never invoke a bare `doctor` executable. `AI-Knowledge` is derived output, not an input folder: tell users to add or edit notes in the configured source directory, then run `update`.

## Privacy default

Lite is fixed to Metadata-only. The deterministic local parser may read Markdown to extract frontmatter, headings, tags, and links, but it does not send file bodies to a model and does not embed note bodies, secrets, or absolute source paths in the dashboard.

## Declared capabilities

- Terminal: probe the Python and agent-host CLI versions and run the packaged foreground commands.
- File read: inspect Markdown only inside the user-authorized source boundary.
- File write: write only `.ai-workbench`, `AI-Knowledge`, and `AI-Dashboard` inside the selected workspace.
- Network: bind only an ephemeral `127.0.0.1` loopback service for dashboard verification; do not call external APIs or upload note bodies.
- Environment: read only process/runtime values needed for deterministic local execution; never print secrets.

Read `references/RUNTIME_CONTRACT.md` for command results, `references/PRIVACY.md` for the exact privacy boundary, and `references/AUTONOMY_GATES.md` before permission, destructive, installation, or external actions.
