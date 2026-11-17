# Skeleton

Starting point for a new `CHANGELOG.md`. The header prose is part of the format — it tells the reader which rules the file follows.

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

[Unreleased]: https://github.com/OWNER/REPO/commits/HEAD
```

# Worked example

Shows all six categories, a yanked release, and the link-reference block.

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Dry-run flag (`--dry-run`) that prints planned actions without executing them.

## [1.1.0] - 2026-07-28

### Added

- Windows arm64 builds are published with each release.

### Changed

- Config file paths may now be relative to the project root instead of the
  current working directory.

### Deprecated

- `--format json` — use `--output json` instead; `--format` will be removed
  in 2.0.0.

### Fixed

- Crash when the config file contained a byte-order mark.

### Security

- Updated `libyaml` to 0.2.6 to address CVE-2026-1234 (code execution when
  parsing untrusted YAML).

## [1.0.1] - 2026-06-14 [YANKED]

- Yanked: the published macOS binary was built from the wrong commit.

### Fixed

- Progress bar flickering on narrow terminals.

## [1.0.0] - 2026-06-01

### Added

- First stable release: `init`, `build`, and `deploy` commands.

### Removed

- The experimental `sync` command from the 0.x series; `deploy --watch`
  covers its use case.

[Unreleased]: https://github.com/OWNER/REPO/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/OWNER/REPO/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/OWNER/REPO/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/OWNER/REPO/releases/tag/v1.0.0
```

# Adaptations

- **Non-GitHub hosting** — point the references at the host's compare URLs
  (GitLab: `/-/compare/v1.0.0...v1.1.0`); a host with no compare view links
  each version to its release tag instead.
- **No Semantic Versioning** — replace the SemVer sentence in the header with
  the scheme actually used; the MAJOR/MINOR/PATCH inference in "Cut a release"
  then no longer applies.
- **First tagged release** — the oldest version has no predecessor to compare
  against; link it to its release tag, as `[1.0.0]` does above.
