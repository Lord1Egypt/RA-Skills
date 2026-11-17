# Publishing Flow

Use this reference when preparing a target skill for GitHub and ClawHub publication.

## Local Account Defaults

For this local installation, assume the default GitHub owner is `jichengkai` with profile `https://github.com/jichengkai`.

Use this owner for repository creation, remote URLs, release notes, and GitHub Actions examples unless the user explicitly names a different owner or organization. This default is only an identity preference; still verify that local GitHub and ClawHub authentication are configured before pushing or publishing.

## GitHub Source Of Truth

1. Confirm the target skill path and the repository root.
2. Use `jichengkai/<repo-name>` as the default GitHub repository target unless the user overrides it.
3. Run a repository status check before editing, committing, or publishing.
4. Keep unrelated user changes intact. Stage only the skill files and release automation files that belong to the current task.
5. Use clear commits such as:
   - `Add <skill-name> skill`
   - `Update <skill-name> publishing workflow`
   - `Release <skill-name> vX.Y.Z`
6. Push through the user's configured GitHub auth. If auth is missing, ask the user to complete login locally.

Preferred remote examples:

```bash
git remote add origin git@github.com:jichengkai/<repo-name>.git
git remote add origin https://github.com/jichengkai/<repo-name>.git
```

## Versioning

If the repo already has version metadata for the skill, update it intentionally:

- Patch: fixes, wording improvements, security-review refinements, or backward-compatible behavior changes.
- Minor: new workflow, new script, new supported publication target, or new automation.
- Major: changed skill interface, renamed skill, removed workflows, or incompatible behavior.

If no version metadata exists, use Git history and release notes as the version record. Do not create extra documentation inside the skill folder solely for version history.

## Direct ClawHub Publish

Before first real publish, verify the current official ClawHub documentation when possible. The current expected flow is:

```bash
clawhub login
clawhub skill publish <path-to-skill> \
  --slug <skill-slug> \
  --name "<display name>"
```

Use `--owner <handle>` when publishing under an org owner. For the local default user account `jichengkai`, omit `--owner` unless current ClawHub documentation requires a personal owner flag. Use the explicit target skill path; do not publish from a parent directory unless the platform documentation requires it.

If `clawhub login` opens a browser or prompts for a token, let the user complete that step. Never request the token in chat, and never store it in the repository.

ClawHub starts a new skill at `1.0.0`, skips unchanged content, and automatically publishes later changed content as the next patch version. Pass `--version` only when an explicit version is needed.

## GitHub Actions Publish

Only add automation when the user asks for it. Use a GitHub secret named `CLAWHUB_TOKEN`, set in repository settings, not in source files.

Prefer the official reusable workflow from ClawHub documentation if it is available and current. The documented reusable workflow accepts an `owner`, `dry_run`, and secret `clawhub_token: ${{ secrets.CLAWHUB_TOKEN }}`. Use `dry_run: true` to preview changed skills without publishing.

If writing a workflow manually, keep it narrow:

- Trigger on tags or manual dispatch unless the user wants every main-branch merge to publish.
- Check out source.
- Install the ClawHub CLI using the official installation method.
- Publish the explicit skill path.
- Read `CLAWHUB_TOKEN` from secrets only.

## Release Notes

Give the user a short release note for each publish:

- What changed.
- What was reviewed.
- Which command or workflow published it.
- Any manual follow-up.
