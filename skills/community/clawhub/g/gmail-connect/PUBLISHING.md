# Publish and update Gmail Connect from GitHub

## Exact folder to import

Repository: `svetlyoh/web-wallet`

Branch: `master`

Skill path: `openclaw/skills/gmail-connect/gmail-connect`

[Open the GitHub skill folder](https://github.com/svetlyoh/web-wallet/tree/master/openclaw/skills/gmail-connect/gmail-connect). It contains `SKILL.md`, all scripts and browser assets, and the listing documents. Its parent is the archive distribution folder.

Keep this nested folder as the maintained source. A generated local `ClawHub/gmail-connect` folder is an upload snapshot; make future edits in GitHub source and re-export.

`CARD.md` is the editable listing brief. Hosted publication reserves `skill-card.md` for ClawHub's generated card; do not upload a manually authored file with that reserved name. The public summary comes from the `description` in `SKILL.md`, while categories/topics and release tags are supplied at publication.

## First GitHub import

1. Push the reviewed skill changes to `master`.
2. Open [ClawHub Import from GitHub](https://clawhub.ai/import), signed in with your `svetlyoh` GitHub account.
3. Find the `gmail-connect` candidate from `svetlyoh/web-wallet` and verify its exact nested path above. The current picker detects `SKILL.md` in owned public repositories.
4. Review the file selection. Include every runtime file under `scripts/`, `assets/`, and `references/`, along with `SKILL.md` and the listing documents. Use **Select all** for this skill folder; referenced-file selection alone can omit Python modules or browser assets.
5. Set display name **Gmail Connect**, slug `gmail-connect`, version `0.1.3`, release tags `latest,preview`, categories `integrations,productivity,communication`, and topics `gmail,email,oauth,ubuntu,local-first`. These last fields are catalog settings, not fields automatically read from this Markdown card.
6. Review ClawHub's MIT-0 publication terms, submit, and inspect the resulting security audit. Keep the preview designation while live acceptance is incomplete. Check slug ownership before choosing a different slug; update the workflow consistently if you change it.

A normal GitHub import publishes a snapshot and stores source provenance. It does not establish automatic future updates. ClawHub also has GitHub-backed source synchronization for enabled publishers; availability depends on its rollout and your dashboard. Do not assume that a source link enrolls your repository.

## Updates using GitHub Actions

The repository workflow `.github/workflows/gmail-connect-clawhub.yml` processes only this skill. Pull requests run Ubuntu offline tests and a publishing dry run. A release tag `gmail-connect-v0.1.3` publishes version `0.1.3` from that exact commit. Manual runs default to a dry run.

One-time setup after merging the workflow:

1. Use `clawhub login` and `clawhub whoami` to verify the publisher account. A signed-in browser does not automatically authenticate the CLI. If the publisher handle differs from `svetlyoh`, change `CLAWHUB_OWNER` in the workflow before publication.
2. Add your ClawHub API token as the GitHub Actions repository secret `CLAWHUB_TOKEN` at [repository Actions secrets](https://github.com/svetlyoh/web-wallet/settings/secrets/actions). Never paste the token into source, Markdown, an issue, or chat.
3. Open [GitHub Actions](https://github.com/svetlyoh/web-wallet/actions) → **Gmail Connect - ClawHub** → **Run workflow** and leave `publish` false to preview. A real manual publish requires selecting `publish` true and running the workflow on `master`.

For each later release:

1. Edit the canonical skill on a feature branch. Update its version consistently in `SKILL.md`, `scripts/gmail_connect/core.py`, `assets/ui/index.html`, `references/operations.md`, the release README, and the card/changelog. The exporter copies the source version without a hard-coded override.
2. Review tests, source, clean export, and preview status. Merge to `master`.
3. Create and push a matching version tag from the intended merged commit, for example:

```bash
git tag gmail-connect-v0.1.4
git push origin gmail-connect-v0.1.4
```

The workflow validates tag/version agreement, exports a clean bundle, and submits it with the repository, source path, ref, and exact GitHub commit. Tags must be new release versions: an existing ClawHub version cannot be overwritten. If you already imported `0.1.3` through the website, publish the next changed release as `0.1.4`; do not submit `0.1.3` again through Actions.

Preview labeling does not prevent `latest` from being installable. If you want a preview available only by a dedicated tag, change the publish tags consistently before submission. After an allowed version is available, users can update a ClawHub-managed installation with `clawhub update @YOUR_CLAWHUB_HANDLE/gmail-connect` in their configured workspace. Check the handle displayed by `whoami` and the resulting listing.

## Publish an exported folder manually

Install ClawHub CLI with Node.js 22+ (`npm install -g clawhub@0.23.3`), then run from the parent of your clean `gmail-connect` export:

```bash
clawhub login
clawhub whoami
clawhub skill publish ./gmail-connect --slug gmail-connect --name "Gmail Connect" --version 0.1.3 --tags latest,preview --categories integrations,productivity,communication --topics gmail,email,oauth,ubuntu,local-first --dry-run
```

After reviewing the preview, repeat without `--dry-run` to submit. The GitHub importer and workflow add source provenance automatically; a standalone local upload should also provide `--source-repo`, `--source-commit`, `--source-ref`, and `--source-path` only when its bytes correspond to that committed source. Do not claim provenance for uncommitted edits.

## References

- [ClawHub publishing and catalog metadata](https://github.com/openclaw/clawhub/blob/main/docs/publishing.md)
- [ClawHub CLI, Actions, and source flags](https://github.com/openclaw/clawhub/blob/main/docs/cli.md)
- [GitHub import behavior](https://github.com/openclaw/clawhub/blob/main/specs/github-import.md)
- [GitHub-backed source synchronization and rollout limits](https://github.com/openclaw/clawhub/blob/main/specs/github-backed-skills.md)
