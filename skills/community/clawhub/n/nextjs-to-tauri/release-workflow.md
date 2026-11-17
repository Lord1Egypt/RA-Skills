# Build and release templates

Install all rows together in the application repository. Review the resulting project diff. The installed skill remains read-only; all runtime writes belong to the application checkout, CI runner or GitHub draft release.

| Bundled source | Application destination |
| --- | --- |
| [desktop-build.yml](desktop-build.yml) | `.github/workflows/desktop-build.yml` |
| [tauri-build.yml](tauri-build.yml) | `.github/workflows/tauri-build.yml` |
| [release-assets.js](release-assets.js) | `.github/scripts/release-assets.mjs` |
| `release-assets/` (all files, including package.json) | `.github/scripts/release-assets/` |
| `ci/` (all shell scripts) | `.github/scripts/ci/` |

The entry script keeps the `.mjs` destination. The module directory includes its own `type: module` declaration, so both CommonJS and ESM application packages work. There are no npm dependencies for these helpers. Do not copy just the entry script: its imports require the complete module directory.

Replace `<App Title>` and `<AppName>` in the build workflow and `ci/prepare-portable.sh`. Match the application's product title and `mainBinaryName`. Review action versions and the pinned Node major using the verification step in SKILL.md. The commands assume Yarn Classic; adapt installation and caching together for npm or pnpm.

## Workflow responsibilities

- `desktop-build.yml` handles tag/manual triggers, serialization, draft creation, the four-target matrix and final verification. A tag creates or reuses an unpublished draft. An existing public release fails the preflight. Manual dispatch skips release creation, uploads and final release verification, but still builds workflow artifacts.
- `tauri-build.yml` is a same-repository reusable workflow, called once per matrix target. The caller passes runner, target, build arguments, draft ID, source commit and the publish flag explicitly. Only the two updater signing secrets are forwarded; GITHUB_TOKEN is provided by Actions. Keep the local workflow reference so the called workflow comes from the caller's commit. See [GitHub reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).
- The matrix stays serial (`max-parallel: 1`) because latest.json is a shared read-modify-write asset. A separate verifier waits for every target before computing checksums and attestation. The release remains a draft for manual publication; the updater's `releases/latest` endpoint ignores drafts.

## Operations and safety checks

- `ci/prepare-draft.sh` validates the tag, rejects duplicate/public releases, creates or reuses the draft and exports its ID plus the checkout commit.
- The build workflow injects the tag version into package.json before `yarn update-version` copies it into Tauri config. Installer names, the embedded version and portable upload tag all use the built version. Manual runs retain the committed version. Keep frontend installation and version propagation as separate steps.
- Linux dependency installation uses sudo on an ephemeral Ubuntu runner. It writes outside the checkout on that runner; it is not a local setup command. Rust and frontend caches also live on the runner.
- Set TAURI_SIGNING_PRIVATE_KEY and, when needed, TAURI_SIGNING_PRIVATE_KEY_PASSWORD as repository secrets before a signed updater build. Never commit the private key. Updater signatures are separate from Windows/macOS code signing and notarization; configure those for the actual distribution.
- `ci/prepare-portable.sh` first requires the action's built appVersion, then copies the Windows binary and exports that version for uploads. The portable exe still requires WebView2 and has no guaranteed update path. It is a separate artifact from the installer.
- Keep releaseAssetNamePattern consistent with mainBinaryName and latest.json. The `_setup` suffix distinguishes NSIS from the portable exe. Omitting the pattern restores Tauri CLI naming. uploadPlainBinary is intended for no-bundle builds and does not replace portable copying here. updaterJsonPreferNsis changes the generic Windows feed target from MSI to NSIS and needs a separate distribution decision.
- `ci/record-build.sh` downloads draft metadata and the updater feed, then records evidence from the actual local build bytes. It binds files to target, version, repository, tag, source commit and workflow run. Evidence is uploaded separately for each target.
- `ci/verify-draft.sh` requires an unpublished draft, downloads its full contents, invokes the verifier and rejects a moved tag. The verifier requires exactly the supported target evidence and asset inventory, rejects stale/missing/duplicate files, checks local hashes, feed ownership, architecture, bundle type and signature-file consistency. Only the previous generated SHA256SUMS is cleared for regeneration.
- `ci/write-checksums.sh` runs after verification and uploads SHA256SUMS from the verified payloads. Attestation consumes those sums only after that step succeeds. `ci/write-summary.sh` links the draft and reminds the operator to publish it manually.

## Verifier modules

The entry script preserves the `record`, `verify`, `ready`, `verify-release` and `verify-draft` commands and the exported API. All module sources are bundled for inspection:

| Module | Responsibility |
| --- | --- |
| `release-assets/common.js` | JSON loading, names, assertions, target mapping, SHA-256 |
| `release-assets/feed.js` | Asset URL ownership, architecture, bundle and signature consistency |
| `release-assets/record.js` | Evidence from local build outputs |
| `release-assets/verify.js` | Exact inventory, source identity, local digests and merged feed checks |
| `release-assets/release.js` | Public/draft release readiness and full release verification |
| `release-assets/cli.js` | Command dispatch and explicit file inputs/outputs |

The entry script re-exports the existing functions. These checks establish build/feed consistency; they do not replace platform signature verification or the updater's cryptographic signature verification.
