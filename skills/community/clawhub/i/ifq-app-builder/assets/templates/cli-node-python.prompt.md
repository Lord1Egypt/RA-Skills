---
templateId: T-cli-node-python
ifqMode: A-12
stack: "Node 20 + TypeScript + commander  ·or·  Python 3.11 + typer"
artifact: "npm package (npx-runnable) or pipx-installable wheel"
---

# T-cli-node-python · command-line tool · ifq-app-builder

Fork, fill, verify, hand off.

## S1 — WHO + WHAT
<replace: who runs this CLI, what they do, what files/streams go in and out>

## S2 — WHERE
- Runtimes: <replace: Node 20 + macOS/Linux/Windows · or Python 3.11 + macOS/Linux>
- Stack (pinned): TypeScript 5 + commander 12 + zod  ·or·  typer + rich + pydantic 2
- Distribution: <replace: npm public · npm private registry · pipx · single static binary via pkg/PyInstaller>
- Telemetry: off by default; opt-in only

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements describing a successful first run on a fresh laptop>

## Acceptance (binary, yes/no observable)
- [ ] `<slug> --help` prints a styled help in under 200ms
- [ ] Primary workflow from S1 works with <replace: real sample input file>
- [ ] Exit codes: `0` success, `1` user error, `2` system error, `130` SIGINT
- [ ] `<slug> --version` prints semver + git short SHA + the IFQ colophon line
- [ ] Localized messages: `zh-CN` + `en` (auto-detect via `LC_ALL`/`LANG`)
- [ ] `npm test` (or `pytest`) covers core commands

## Scaffold (run order — Node variant)
1. `mkdir <slug> && cd <slug> && npm init -y`
2. `npm install commander zod chalk picocolors`
3. `npm install -D typescript @types/node tsx vitest`
4. `src/cli.ts` declares commands with `commander`; each command imports a pure function from `src/lib/`
5. `bin/<slug>.js` shebang `#!/usr/bin/env node` → imports `dist/cli.js`
6. `tsconfig.json` `target: ES2022`, `module: NodeNext`
7. `package.json` `bin` field, `files: ["bin","dist"]`, `engines.node: ">=20"`

## Scaffold (run order — Python variant)
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install typer rich pydantic`
3. `pyproject.toml` declares `[project.scripts] <slug> = "<pkg>.cli:app"`
4. `src/<pkg>/cli.py` `app = typer.Typer(rich_markup_mode="rich")`
5. `pip install -e .` for local dev; `pipx install .` for end-user smoke

## Packaging
- Node: `npm publish` (or `--registry <private>`); semver-locked
- Python: `python -m build && pipx install dist/<slug>-<ver>-py3-none-any.whl`
- Single binary (optional): `npx pkg` (Node) or `pyinstaller --onefile` (Python)

## Security baseline
- Validate every argument with zod / pydantic; reject unknown flags
- Never `child_process.exec(userInput)` / `subprocess.run(shell=True, userInput)`
- Tokens / API keys: read from env vars or OS keychain, never positional args
- File writes: refuse to write outside `cwd` unless `--out` is explicit
- Print a single-line summary on `SIGINT`; never leave half-written files

## IFQ ambient
- `--version` ends with `— shaped with ifq.ai/app-builder`
- Help footer (last line): `— shaped with ifq.ai/app-builder`
- Use color sparingly: rust for primary action, quiet teal for URLs, mono for paths

## Agent execution contract
- Print the three sentences back first
- Pick **one** runtime (Node or Python). Do not produce both unless user explicitly requests it.
- Never publish to npm/PyPI as part of scaffold; only document the publish command

— shaped with ifq.ai/app-builder · A-12 · T-cli-node-python
