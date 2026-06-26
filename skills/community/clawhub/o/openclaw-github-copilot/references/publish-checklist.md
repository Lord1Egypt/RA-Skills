# Publish Checklist

Use this checklist before uploading a new version to ClawHub.

## Content

- `SKILL.md` uses valid YAML frontmatter
- metadata is a single-line JSON object
- every referenced file actually exists
- helper scripts use `{baseDir}` in docs where appropriate
- instructions prefer native `openclaw` commands over speculative config edits

## Validation

- run `openclaw skills info openclaw-github-copilot`
- run `openclaw skills check`
- run `bash scripts/copilot-status.sh`
- run `bash scripts/copilot-status.sh --probe` if a live auth check is safe
- run `bash scripts/copilot-quickstart.sh --probe` for the guided flow

## Packaging

To create a local bundle for inspection:

```bash
cd ..
zip -r ../downloads/openclaw-github-copilot.skill openclaw-github-copilot
```

## Publish

If `clawhub whoami` shows a logged-in account:

```bash
clawhub publish ./skills/openclaw-github-copilot \
  --slug openclaw-github-copilot \
  --name "OpenClaw GitHub Copilot" \
  --version 1.0.0 \
  --tags latest \
  --changelog "Initial public release with setup guide, troubleshooting notes, and guided helper scripts."
```

## Post-publish smoke check

- run `clawhub inspect openclaw-github-copilot`
- install into a clean workspace if possible
- verify the skill still loads via `openclaw skills info openclaw-github-copilot`
