# Publishing Guide

This document is the standard update and release guide for `pipaclaw-skills-hub`.

## What Gets Published

Publish the repository root:

- `SKILL.md`
- `agents/`
- `references/`
- lightweight public helper scripts such as `scripts/*.sh`
- public skill folders such as `ppt-maker/`, `social-account-ops/`, and `promo-video-maker/`

Do not publish:

- backend services
- backend implementation code
- customer files
- generated artifacts
- local test harnesses
- `node_modules`

## Versioning Rule

Use semver:

- `0.1.x` for doc fixes, wording changes, and safe routing/reference updates
- `0.2.x` for new public skill behavior or significant workflow changes
- `1.0.0` when the hub contract is considered stable

## Preflight Checklist

Before publishing:

1. Confirm every referenced file in every `SKILL.md` actually exists.
2. Confirm no private customer names, reverse-engineered assets, or generated deliverables remain in the repo.
3. Confirm every published helper script is a thin public wrapper and does not contain backend-only business logic.
4. Confirm the root hub files are up to date:
   - `README.md`
   - `SKILL.md`
   - `agents/openai.yaml`
   - `references/routing-map.md`
5. Run:

```bash
cd /Users/xiexiongjie/code/skills-hub/skills
find . -type f | sort
git status --short
```

## Important Network Note

On this machine, ClawHub must be accessed through ClashX at `127.0.0.1:7890`.

The published `clawhub` CLI currently has a Node-path proxy issue:

- `clawhub ...` under Node may fail with `fetch failed`
- the Bun path works because it uses the curl-based request path

Use the Bun entry directly for login and publish.

## One Command Entry

Use the helper script in this repository:

```bash
cd /Users/xiexiongjie/code/skills-hub/skills
bin/clawhub-release doctor
```

That script handles:

- proxy validation
- local ClawHub CLI patch verification
- Bun-based execution
- auth check

## Login

```bash
cd /Users/xiexiongjie/code/skills-hub/skills

bin/clawhub-release login --token '<TOKEN>'
bin/clawhub-release whoami
```

Expected result:

- login succeeds
- `whoami` prints the authenticated handle

## First Publish

```bash
cd /Users/xiexiongjie/code/skills-hub/skills

bin/clawhub-release publish --version 0.1.0
```

## Update Publish

For the next release, only change the version:

```bash
cd /Users/xiexiongjie/code/skills-hub/skills

bin/clawhub-release publish \
  --version 0.1.1 \
  --changelog 'Refined public hub routing and skill package documentation.'
```

Change note wording can come from [RELEASE_NOTES_TEMPLATE.md](/Users/xiexiongjie/code/skills-hub/skills/RELEASE_NOTES_TEMPLATE.md).

## If Publish Fails

### `fetch failed`

Cause:
- the Node CLI path is not using the local proxy correctly

Fix:
- use the Bun command shown above
- make sure ClashX is running on `127.0.0.1:7890`

Quick check:

```bash
curl -I -x http://127.0.0.1:7890 https://clawhub.ai
```

### `ENOENT` for nested files during upload

Cause:
- the local `clawhub` install may still contain the nested-upload bug

The repository helper script auto-applies the required local patch when missing.

### `Not logged in`

Cause:
- token was not stored successfully

Fix:
- run the Bun-based `login`
- then run `whoami`
- only after that run `publish`

## Current Published Skill

- slug: `pipaclaw-skills-hub`
- first published version: `0.1.0`
