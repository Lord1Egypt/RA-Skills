# iterate-skill-installer

<p align="center">
  <a href="README.md"><strong>English</strong></a> ·
  <a href="README.zh-CN.md"><strong>简体中文</strong></a>
</p>

One-command installer for [iterate-skill](https://github.com/jingzhao-l/iterate-skill) across AI coding assistants.

[![GitHub stars](https://img.shields.io/github/stars/jingzhao-l/iterate-skill?style=social&label=Star)](https://github.com/jingzhao-l/iterate-skill)

> ⭐ If this project helps you, please consider giving a GitHub star — it means a lot to open-source maintenance!

## Usage

```bash
# Interactive install — detects your AI assistants and lets you choose
npx iterate-skill-installer

# Install to a specific assistant only
npx iterate-skill-installer --ai trae
npx iterate-skill-installer --ai claude

# Install into a project directory instead of globally
npx iterate-skill-installer --target ./my-project

# Force overwrite existing skill files
npx iterate-skill-installer --force

# Skill-only install — skip installing the iterate CLI
npx iterate-skill-installer --no-cli

# Show help / version
npx iterate-skill-installer --help
npx iterate-skill-installer --version
```

## What it does

1. Checks for Python 3 on your system.
2. Fetches the latest iterate-skill release from GitHub.
3. Downloads the release tarball, `SHA256SUMS.txt` and its detached GPG
   signature (`iterate-skill.tar.gz.asc`).
4. Verifies BOTH the tarball checksum (integrity) and the signature against the
   pinned iterate signing key (authenticity). **Signing is mandatory**: a
   release without a valid signature is refused, because `SHA256SUMS.txt`
   travels in the same release as the tarball and therefore cannot be the only
   anchor. Install GnuPG (`gpg`) if you do not have it; hosts that cannot run
   gpg may opt out explicitly with `ITERATE_ALLOW_UNSIGNED=1` (a bad signature
   is never bypassed).
5. Extracts the release into a temporary directory.
6. Runs the bundled Python install script (`scripts/install.py`) which:
   - Detects installed AI coding assistants on your machine.
   - Prompts you to select targets (default: all detected assistants).
   - Copies the skill files into the correct skills directories.
7. Installs the `iterate` CLI onto your PATH (prefers `pipx`, otherwise
   `pip install --user`) so you can run `iterate onboard` directly.

> **Note:** the installer normally puts the `iterate` CLI on your PATH so a single
> command gives you both the skill and the CLI. If you **don't** want the CLI
> auto-installed, pass `--no-cli` to install the skill only — you can install the
> CLI later with `pipx install .` or `pip install .` from a checkout. If the CLI
> install fails, you can still install it later the same way.

## Supported AI assistants

Trae, Claude / Claude Code, Cursor, Windsurf, GitHub Copilot, Codex, Gemini CLI, OpenCode, Aider, AiderDesk, Zed, Warp, Continue, Cline, Roo Code, Qoder, Augment, OpenClaw, Autohand Code CLI, IBM Bob, CodeArts Agent, Antigravity, Amp, Deep Agents, Kimi Code CLI, Astral.

## Requirements

- Node.js 18+
- Python 3.10+
- `tar` command available on PATH (available by default on macOS, Linux, Windows 10+)

## Release tarball structure

The GitHub release asset `iterate-skill.tar.gz` must contain **exactly one
top-level directory** (e.g. `iterate-skill/`). The installer extracts it with
`tar --strip-components=1`, so a tarball with multiple top-level directories,
or with entries whose path disappears after stripping the top level, is
rejected instead of being silently mis-extracted.

## License

MIT
