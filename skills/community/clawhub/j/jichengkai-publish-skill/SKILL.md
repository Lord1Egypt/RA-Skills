---
name: publish-skill
description: Prepare, safety-review, version, commit, and publish local Codex skills through a GitHub-backed release flow and ClawHub CLI. Use when the user asks to host, publish, release, update, package, audit, or automate publication of a Codex skill, including GitHub repository setup, ClawHub `clawhub skill publish <path>`, patch updates, GitHub Actions with `CLAWHUB_TOKEN`, release notes, or pre-publish security checks.
---

# Publish Skill

## Overview

Use this skill to move a local Codex skill from a working folder to a published, versioned artifact. Keep GitHub as the source of truth, run a local safety review before publication, and use ClawHub only after authentication and command details are clear.

## Local Defaults

- Default GitHub account: `jichengkai`.
- Default GitHub profile: `https://github.com/jichengkai`.
- Prefer creating and pushing skill repositories under `jichengkai` unless the user explicitly names a different owner or organization.
- Treat this as a local identity preference only. It does not prove authentication and does not replace `gh auth login`, Git credentials, `clawhub login`, or `CLAWHUB_TOKEN`.

## Boundaries

- Never ask for or expose GitHub passwords, ClawHub tokens, API keys, SSH private keys, or recovery codes in chat.
- If authentication is missing, ask the user to complete `gh auth login`, `clawhub login`, or secret setup locally; do not invent credentials.
- Treat publishing commands as state-changing. Explain what will be published before running them, and stop if the target path is ambiguous.
- Verify current official ClawHub documentation before relying on exact CLI flags when network access is available or the user asks for a real publish.
- Do not publish a skill that reads sensitive directories, handles credentials, runs obfuscated code, or makes undisclosed network calls unless the user explicitly accepts the risk after review.

## Workflow

1. Locate the target skill.
   - Prefer an explicit path from the user.
   - Otherwise check the current workspace, then `${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>`.
   - Read the target `SKILL.md`, `agents/openai.yaml` if present, and a concise file listing before making decisions.

2. Validate the skill structure.
   - Use the local skill validator when available: `/Users/jichengkai/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-path>`.
   - Confirm the skill has only needed files: `SKILL.md`, optional `agents/`, and purposeful `scripts/`, `references/`, or `assets/`.
   - Do not add `README.md`, `CHANGELOG.md`, or other auxiliary docs inside the skill unless the publishing platform explicitly requires them.

3. Run a pre-publish safety review.
   - Run `python3 <this-skill>/scripts/review_skill.py <skill-path>`.
   - Read `references/security-review.md` when the scanner reports findings, the skill contains executable code, or the user asks for a security pass.
   - Inspect scripts manually for destructive commands, credential access, hidden network behavior, and obfuscation.

4. Prepare the GitHub source repo.
   - Read `references/publishing.md` for the detailed GitHub and ClawHub flow.
   - Use `jichengkai` as the default GitHub owner for local publishing unless the user overrides it.
   - Check repository status before editing or committing, and preserve unrelated user changes.
   - Keep the repository history as the durable version record. If version metadata exists, bump it intentionally; otherwise use clear commit messages and release notes.

5. Publish or update.
   - Use `clawhub skill publish <path> --slug <slug> --name "<display name>"` for a direct publish after auth is present; add `--owner <handle>` for an org owner.
   - For repeatable automation, add a GitHub Actions workflow only when the user asks, and use a GitHub secret named `CLAWHUB_TOKEN`.
   - After publish, report the repository, commit, command run, result, and any manual auth step the user still needs.

## Resource Guide

- `references/publishing.md`: detailed commands, versioning choices, and GitHub Actions pattern.
- `references/security-review.md`: manual safety checklist and blocker definitions.
- `scripts/review_skill.py`: local scanner for secrets, sensitive paths, network behavior, obfuscation hints, and unexpected binaries.

## Final Response Checklist

- Target skill path and repo path.
- Validation and safety-review result.
- Git commit or branch created, if any.
- Publish command run or exact manual command still needed.
- Remaining auth or secret setup, without exposing any secret values.
