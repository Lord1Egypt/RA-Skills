# Repository Guidelines

## Project Structure & Module Organization

- `SKILL.md` defines the Agent Skill metadata, triggering rules, workflows, and troubleshooting contract.
- `scripts/gh_accel.sh` is the self-contained Bash entry point; keep the core implementation here.
- `README.md` provides the public overview, installation instructions, and mirror-maintenance notes.
- `templates/proxies.conf.example` documents the optional private-proxy configuration format.

## Build, Test, and Development Commands

There is no build step. Use these commands from the repository root:

```bash
bash -n scripts/gh_accel.sh     # Check Bash syntax
bash scripts/gh_accel.sh check  # Probe direct GitHub access and all configured proxies
bash scripts/gh_accel.sh dl <github-url>          # Download with automatic fallback
bash scripts/gh_accel.sh clone <owner/repo> [dir] # Clone with automatic fallback
``+

If `shellcheck` is installed, run `shellcheck scripts/gh_accel.sh` before submitting shell changes.

## Coding Style & Naming Conventions

Use Bash with `#!/usr/bin/env bash`, two-space indentation, lowercase snake-case function and variable names, and meaningful prefixes such as `cmd_` for command handlers. Prefer defensive constructs already present in the script, including quoted expansions and non-empty array expansion. Keep user-facing text consistent with the existing Chinese/English style. Documentation uses GitHub-flavored Markdown with numbered skill sections.

## Testing Guidelines

No automated test framework is currently configured. At minimum, run the syntax and help checks above. For network-facing changes, run `check`, then exercise `dl --no-direct` and `clone --no-direct` against a small public GitHub artifact or repository. Verify downloads by size or SHA-256. Avoid committing downloaded fixtures or machine-local proxy configuration.

## Commit & Pull Request Guidelines

Recent history uses short imperative subjects with type or release prefixes, for example `docs: ...` and `v1.2.0: ...`. Keep subjects specific and add a body for behavior changes, compatibility impacts, or mirror-list updates.

Pull requests should include a concise problem statement, implementation summary, validation performed, and links to related issues. Documentation-only changes should show before/after excerpts or rendered screenshots where structure is affected.

## Security & Configuration Tips

Never commit local proxy configuration, credentials, or generated `~/.config/gh-accelerator/proxies.conf` files. Private repositories must not use third-party mirrors. Preserve the direct-first behavior and never introduce global Git URL rewrites.
