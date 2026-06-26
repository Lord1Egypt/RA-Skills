# Publishing Guide

This directory lives inside a larger workspace repository, so publish it as its own standalone GitHub repository rather than pushing the parent workspace.

## Current Local Paths

If you are working in this machine, keep the local folder names aligned with the skill slug:

- repo dir: `/home/living/.openclaw/workspace/skills/one-person-company-os`
- private release dir: `/home/living/.openclaw/workspace/one-person-company-os-release`

Do not keep local names like `one-person-company` while the actual skill slug is `one-person-company-os`. That mismatch is easy to forget and makes ClawHub publish and follow-up verification more error-prone.

## Recommended Flow

1. Create a new empty GitHub repository, for example `one-person-company-os`
2. In this directory, initialize a nested repository
3. Commit the skill package
4. Add the GitHub remote
5. Push the first release

## Commands

Run these commands from this directory:

```bash
cd <repo-dir>
python3 scripts/preflight_check.py --mode 创建公司
python3 scripts/ensure_python_runtime.py
python3 scripts/validate_release.py
git init
git checkout -b main
git add .
git commit -m "release: publish one-person-company-os v1.0.0"
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

If `main` already exists locally, skip the branch creation step.

Before pushing, make sure `python3 scripts/validate_release.py` passes locally so the helper scripts, agent-brief generation, and release SVG assets are all verified together.

## Ongoing Update Flow

For later updates on this machine, the practical flow is:

```bash
cd /home/living/.openclaw/workspace/skills/one-person-company-os
python3 scripts/preflight_check.py --mode 创建公司
python3 scripts/ensure_python_runtime.py
python3 scripts/validate_release.py
git status --short
git add .
git commit -m "release: polish one-person-company-os public surface"
git push origin main
clawhub publish /home/living/.openclaw/workspace/skills/one-person-company-os \
  --slug one-person-company-os \
  --name "One Person Company OS" \
  --version 1.0.3 \
  --changelog "Complete the mainstream platform push list with canonical status, MCP registry submissions, agentskills.io listing material, and current Copilot/OpenAI/Microsoft marketplace requirements."
```

Replace the staged files, commit message, version, and changelog as needed.

When splitting the `clawhub publish` command across lines in bash, keep every continued line except the last ending with `\`. Without the backslashes, the shell runs `clawhub publish <path>` first and then treats `--slug`, `--version`, and `--changelog` as separate commands.

Single-line equivalent:

```bash
clawhub publish /home/living/.openclaw/workspace/skills/one-person-company-os --slug one-person-company-os --name "One Person Company OS" --version 1.0.3 --changelog "Complete the mainstream platform push list with canonical status, MCP registry submissions, agentskills.io listing material, and current Copilot/OpenAI/Microsoft marketplace requirements."
```

## Suggested First Repository Settings

- repository name: `one-person-company-os`
- visibility: public
- description: `Set up and run a solo SaaS like a real company`
- homepage: optional, add the ClawHub listing later if desired
- topics: `ai-agents`, `solo-founder`, `saas`, `indie-hacker`, `workflow`, `openclaw`, `product-ops`

## Suggested Current Release

- tag: `v1.0.3`
- title: `v1.0.3: mainstream platform push list`
- notes source: `CHANGELOG.md`, `RELEASE-NOTES.md`, and `release/v1.0.3-github-release.md`

## ClawHub Submission Prep

Use the materials in `release/`:

- `clawhub-listing.md`
- `sample-outputs.md`
- `media-kit.md`
- `social-posts.md`
- the SVG assets under `release/assets/`

## ClawHub Publish Notes

- Use the absolute skill folder path in `clawhub publish`. Avoid publishing `.` from an ambiguous working directory.
- Keep the local folder basename aligned with the slug: `one-person-company-os`.
- Current CLI `clawhub v0.4.0` has a client-side timeout tendency around publish. A timeout does not reliably mean the server-side publish failed.
- If the CLI reports `Version already exists`, treat that as a strong sign the server already accepted the version.
- After any timeout, verify with the download endpoint before retrying:

```bash
curl -L "https://clawhub.ai/api/v1/download?slug=one-person-company-os&version=1.0.3" -o /tmp/one-person-company-os-1.0.3.zip
unzip -p /tmp/one-person-company-os-1.0.3.zip README.zh-CN.md | sed -n '1,80p'
unzip -p /tmp/one-person-company-os-1.0.3.zip agents/openai.yaml
unzip -p /tmp/one-person-company-os-1.0.3.zip release/v1.0.3-github-release.md | sed -n '1,120p'
```

- The public listing page may lag behind the downloadable package version. Trust the download endpoint first.

## Language Behavior To Mention Publicly

- Chinese prompt in, Chinese materials out by default
- English prompt in, English materials out by default
- bilingual output only when explicitly requested
- founder-visible workspace files and directories localize to the founder language
- hidden machine-state storage stays stable at `.opcos/state/current-state.json`
- marketplace build does not auto-install system packages
