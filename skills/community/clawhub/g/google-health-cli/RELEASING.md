# Releasing google-health-cli

Releases are cut by tagging a commit `vX.Y.Z`. A `v*` tag triggers the **Release**
workflow (`.github/workflows/release.yml`), which runs **GoReleaser**: it cross-compiles
the binary for linux/darwin/windows × amd64/arm64, stamps the version via ldflags,
generates `checksums.txt`, and publishes a GitHub Release with the archives attached.

Versioning is [semver](https://semver.org): bump **major** for a breaking change to the
CLI surface / JSON contract (see `AGENTS.md`), **minor** for new commands or data types,
**patch** for fixes. The version is *your* decision — there is intentionally no auto-tagging.

## Before you release

- The change is merged to `main` and **CI is green** on `main`.
- Locally: `make check` passes (tidy, fmt, vet, lint, race tests).
- You've decided the version bump (major/minor/patch).

## How to release

### A. From the GitHub UI (preferred)

**Actions → Release → "Run workflow"** → enter the version (e.g. `v1.2.3`) → Run.

The workflow validates the version, creates and pushes the tag at the current `main`
commit, and runs GoReleaser. (The tag is pushed with the built-in `GITHUB_TOKEN`, which
does not start a second workflow run, so there is no duplicate release.)

### B. From the terminal

```sh
git checkout main && git pull
git tag -a v1.2.3 -m "v1.2.3"
git push origin v1.2.3
```

The pushed tag triggers the same Release workflow.

## After it runs

- Confirm the **GitHub Release** appears with six archives + `checksums.txt`:
  `gh release view v1.2.3`
- Confirm a downloaded binary reports the right version: `google-health-cli version`.
- `go install github.com/stozo04/google-health-cli/cmd/google-health-cli@latest` picks up
  the new tag.

Pre-release tags (e.g. `v1.2.3-rc.1`) are auto-marked as prereleases by GoReleaser
(`prerelease: auto` in `.goreleaser.yaml`).

## ClawHub (separate)

The ClawHub skill is **not** tied to releases. It republishes whenever `SKILL.md` changes
on `main`, via `.github/workflows/publish-clawhub.yml` (needs the `CLAWHUB_TOKEN` repo
secret). Bumping the CLI version does not require a ClawHub republish.
