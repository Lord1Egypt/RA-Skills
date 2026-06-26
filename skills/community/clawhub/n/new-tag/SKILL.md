---
name: new-tag
description: Prepare and publish a git release tag by inspecting the repo's release convention, bumping affected package versions, validating release builds, committing the release prep, pushing the branch, and pushing a new tag. Use when asked to bump project versions, cut a release, push a tag, or trigger tag-based GitHub Actions or npm publishing.
---

# New Tag

## Workflow

### Inspect the release convention

- Check `git status --short`, the current branch, and recent tags before changing versions.
- Inspect `.github/workflows/` for tag patterns such as `v*`, package filters, build jobs, and publish jobs.
- Inspect package manifests and release scripts to determine which package version should drive the new tag.

### Choose the version plan

- Follow the repository's existing tag pattern unless the user explicitly wants to change it.
- Bump only the packages affected by the release.
- Bump shared packages when their changed code is consumed by a package that will be published from this tag.
- Keep compatibility gates unchanged unless the new release actually requires a higher minimum version.
- If the worktree contains unrelated changes, stop and ask before including them in the release.

### Apply the version changes

- Update package versions in manifest files.
- Update release workflows, workspace filters, and package references when package names or published artifacts have changed.
- Fix any packaging or TypeScript resolution issues discovered while preparing the release.

### Validate before tagging

- Run the builds required by the release workflow, not just a subset that happens to pass locally.
- At minimum, build every package that the tag-triggered workflow will build or publish.
- Do not create or push a tag while any required build is failing.

### Commit and push the release prep

- Stage only the files that belong in the release prep.
- Use a clear release-oriented commit message such as `Prepare vX.Y.Z release`.
- Push the branch before creating the tag so the tag points at a commit already on the remote.

### Create and push the tag

- Create an annotated tag that matches the workflow trigger, usually `vX.Y.Z`.
- Push the tag explicitly.
- Report the commit SHA, tag name, and any workflows that should now trigger.

## Command Pattern

Use this sequence as the default pattern and adapt it to the repo:

```bash
git status --short
git tag --sort=-creatordate | head
rg -n "tags:|push:|workflow_dispatch|publish|--filter" .github/workflows -g '*.yml' -g '*.yaml'

# edit package versions and release metadata

pnpm --filter <package-a> build
pnpm --filter <package-b> build
pnpm run <release-build-if-defined>

git add <release-files>
git commit -m "Prepare vX.Y.Z release"
git push origin <branch>
git tag -a vX.Y.Z -m "vX.Y.Z"
git push origin vX.Y.Z
```

## Heuristics

- Prefer the version of the primary published package as the tag version.
- If the repo already uses mixed version streams, keep using the stream implied by recent tags.
- If a tag-triggered workflow still references old package names, fix that before tagging.
- If a package publish job can skip already-published versions, still ensure the build jobs succeed so the GitHub release is not red.
- If the release includes a browser extension and a native host, verify that packaging or ID compatibility changes do not break the published extension.

## Output

Return:

- the packages that were bumped and their new versions
- the validation commands that were run
- the commit SHA
- the pushed tag name
- any residual release risk, if something was intentionally left unchanged
