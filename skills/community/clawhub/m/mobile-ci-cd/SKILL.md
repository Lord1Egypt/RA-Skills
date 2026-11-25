---
name: mobile-ci-cd
description: "Writes and hardens CI/CD pipelines for Android, iOS and Flutter on GitHub Actions and GitLab CI: Gradle and xcodebuild builds, lint and tests, signing from secrets, fastlane, Play and TestFlight upload, Firebase App Distribution, caching and SHA-pinned actions. Use when setting up, fixing, speeding up or reviewing a mobile pipeline, workflow YAML, .gitlab-ci.yml or Fastfile."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile CI/CD

Build pipelines that a senior mobile engineer would trust with the signing keys: fast feedback on every
pull request, reproducible signed release builds from tags, and no path for untrusted code to reach a
secret or a store account.

## When to use

- The user asks to set up, fix, speed up or review CI for an Android, iOS, Flutter or KMP app.
- A workflow file (`.github/workflows/*.yml`), `.gitlab-ci.yml`, `Fastfile`, `Matchfile` or Gradle
  signing config is being added or changed.
- Release automation: Play Console upload, TestFlight, Firebase App Distribution, version numbering.
- A security review of an existing pipeline (secret exposure, unpinned actions, broad token permissions).

Not for: app-level security such as storage or network hardening (use `mobile-security`), or writing the
merge request that ships the pipeline (use `mobile-merge-request`).

## Workflow

1. Inventory the project before writing YAML.
   - Platforms, build system, flavors or schemes, module layout, existing lint and test tasks.
   - Existing CI files, `Gemfile` / `Fastfile`, `libs.versions.toml`, `Package.resolved`, `pubspec.lock`.
   - Where releases go today (Play track, TestFlight, Firebase App Distribution) and who approves them.
2. Agree the pipeline shape with the user (see table below). Ask before choosing store tracks,
   distribution groups or approval rules; do not guess them.
3. Load the matching reference and adapt its workflow instead of writing from memory:
   [Android on GitHub Actions](references/android-github-actions.md),
   [iOS on GitHub Actions](references/ios-github-actions.md),
   [Flutter on GitHub Actions](references/flutter-github-actions.md),
   [GitLab CI](references/gitlab-ci.md).
4. Write the verify job first (lint, static analysis, unit tests, coverage gate). It runs on every PR and
   never sees a secret.
5. Write the release job second: tag or manual trigger only, protected `environment:`, signing from
   secrets into the runner temp dir, upload to the store or distribution service.
6. Harden: top-level `permissions: contents: read`, SHA-pinned actions, concurrency group, timeouts,
   secrets passed through `env:` only, untrusted event data never interpolated into `run:`.
7. Validate locally where possible: `actionlint` for syntax and expression errors, `zizmor` for
   workflow security findings, and a dry run on a branch with the release job disabled.
8. Deliver the files plus the list of required secrets and the manual setup steps (see Output format).
   Never ask the user to paste secret values into the conversation.

## Pipeline shape

| Trigger | Jobs | Secrets |
|---|---|---|
| `pull_request` | verify (lint, detekt/ktlint/SwiftLint/analyze, unit tests, coverage gate), debug build | None |
| `push` to `main` | verify, QA build to Firebase App Distribution or TestFlight internal | Distribution only, via `environment:` |
| `push` tag `v*` or `workflow_dispatch` | verify, signed release build, store upload | Signing and store, via `environment:` with required reviewers |

Run iOS jobs only when iOS files change (`paths:` filters). macOS runner minutes cost several times more
than Linux minutes.

## Rules

### 1. Every action is pinned to a full commit SHA

Tags are mutable. A compromised tag runs attacker code with your secrets.

```yaml
# BAD: tag can be moved to a malicious commit
- uses: actions/checkout@v7
- uses: some-org/upload-thing@main

# GOOD: immutable commit, human-readable version in the comment
# (the SHA below is a placeholder, resolve the real one before use)
- uses: actions/checkout@<full-40-char-commit-sha> # vX.Y.Z
```

- Resolve a tag to its commit: `git ls-remote https://github.com/actions/checkout 'refs/tags/vX.Y.Z*'`
  (use the `^{}` line for annotated tags) or `gh api repos/actions/checkout/commits/vX.Y.Z --jq .sha`.
- Keep pins fresh with Dependabot, which updates the SHA and the comment together:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

- Container images are pinned by digest (`image@sha256:<digest>`), tools by exact version
  (`Gemfile.lock`, `firebase-tools@<x.y.z>`).

### 2. The token gets the least privilege, granted per job

```yaml
# BAD: default token may have write access to the whole repo
on: pull_request
jobs:
  test: ...

# GOOD: read-only by default, escalate only where needed
permissions:
  contents: read

jobs:
  distribute:
    permissions:
      contents: read
      id-token: write   # OIDC to a cloud provider, nothing else
```

- Set `persist-credentials: false` on `actions/checkout` unless a later step pushes with the token.

### 3. Secrets never reach untrusted code

Secrets are not passed to `pull_request` runs from forks. Do not "fix" that by switching triggers.

```yaml
# BAD: runs fork code with secrets and a write token
on: pull_request_target
jobs:
  build:
    steps:
      - uses: actions/checkout@<sha> # vX.Y.Z
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: ./gradlew bundleRelease

# GOOD: PRs build unsigned; signing happens only on trusted refs
on:
  pull_request:
  push:
    tags: ['v*']
jobs:
  release:
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production
```

- `workflow_run` and `issue_comment` triggers carry the same risk: secrets plus someone else's input.

### 4. Release jobs run behind a protected environment

- Store and signing secrets are environment secrets, not repository secrets.
- The environment has required reviewers and a deployment branch or tag rule (`v*` tags, `main`).

```yaml
# BAD: any workflow on any branch can read the Play key
env:
  PLAY_JSON: ${{ secrets.PLAY_SERVICE_ACCOUNT_JSON }}   # repository secret, workflow level

# GOOD: only this job, only after approval, only on allowed refs
jobs:
  release:
    environment: play-production
    steps:
      - run: bundle exec fastlane android release
        env:
          PLAY_SERVICE_ACCOUNT_JSON: ${{ secrets.PLAY_SERVICE_ACCOUNT_JSON }}
```

### 5. Signing material is decoded into the runner temp dir, never committed

```yaml
# BAD: keystore committed as app/release.jks, password in gradle.properties,
# both visible to every fork and every past clone forever
- run: ./gradlew bundleRelease

# GOOD: decoded at build time, outside the workspace
- name: Decode upload keystore
  env:
    KEYSTORE_BASE64: ${{ secrets.ANDROID_UPLOAD_KEYSTORE_BASE64 }}
  run: |
    echo "$KEYSTORE_BASE64" | base64 --decode > "$RUNNER_TEMP/upload.jks"
    echo "ANDROID_KEYSTORE_PATH=$RUNNER_TEMP/upload.jks" >> "$GITHUB_ENV"
```

- Gradle reads path and passwords from environment variables (see the Android reference).
- With Play App Signing, CI holds only the upload key. A leaked upload key can be reset in Play Console;
  a leaked app signing key cannot.
- iOS: certificates and profiles come from `fastlane match` in `readonly` mode into a temporary keychain
  created by `setup_ci`. Never export a `.p12` into the repo.
- `.gitignore` covers `*.jks`, `*.keystore`, `*.p12`, `*.p8`, `*.mobileprovision`, `google-services.json`
  if it is environment specific, and any `*-service-account.json`.

### 6. Secrets and untrusted input go through `env:`, never inline

```yaml
# BAD: secret ends up in the process list and possibly the log; PR title is a script injection
- run: |
    set -x
    curl -H "Authorization: Bearer ${{ secrets.API_TOKEN }}" ...
    echo "Building ${{ github.event.pull_request.title }}"

# GOOD
- env:
    API_TOKEN: ${{ secrets.API_TOKEN }}
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    curl -H "Authorization: Bearer $API_TOKEN" ...
    echo "Building $PR_TITLE"
```

- No `set -x`, `env`, `printenv` or `--debug` flags in steps that hold secrets.
- Mask values derived from a secret: `echo "::add-mask::$DERIVED"`.
- `--dart-define` values and `BuildConfig` fields are compiled into the app. They are configuration,
  never secrets.

### 7. One run per ref; cancel PR runs, never cancel releases

```yaml
# BAD: every push queues another full run, and a new tag can kill an upload half way
concurrency:
  group: ci
  cancel-in-progress: true

# GOOD
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

- Every job has `timeout-minutes`. A hung simulator should not burn six hours of macOS minutes.

### 8. Caches are keyed on lockfiles and written only from trusted branches

```yaml
# BAD: hand-rolled Gradle cache, keyed on nothing useful, written by every PR
- uses: actions/cache@<sha> # vX.Y.Z
  with:
    path: ~/.gradle
    key: gradle

# GOOD: setup-gradle caches and only writes from the default branch by default
- uses: gradle/actions/setup-gradle@<sha> # vX.Y.Z
```

- iOS: cache `SourcePackages` (passed via `-clonedSourcePackagesDirPath`) keyed on
  `hashFiles('**/Package.resolved')`, and resolve with `-disableAutomaticPackageResolution` so CI uses
  the committed versions.
- Flutter: `subosito/flutter-action` with `cache: true`. Release jobs restore caches read-only.

### 9. Version numbers come from CI and only go up

```yaml
# BAD: versionCode hand-edited in build.gradle.kts, forgotten, rejected by Play
versionCode = 42

# BAD: GitHub expressions have no arithmetic, this is not a number
run: ./gradlew bundleRelease -PversionCode=${{ github.run_number + 1000 }}

# GOOD: offset computed in the shell, passed as a Gradle property
- run: echo "VERSION_CODE=$(( GITHUB_RUN_NUMBER + ${VERSION_CODE_OFFSET:-0} ))" >> "$GITHUB_ENV"
  env:
    VERSION_CODE_OFFSET: ${{ vars.VERSION_CODE_OFFSET }}
- run: ./gradlew bundleRelease -PversionCode="$VERSION_CODE"
```

- iOS: pass `CURRENT_PROJECT_VERSION=$BUILD_NUMBER` to the build so `CFBundleVersion` follows the run.
- Flutter: `--build-number="$VERSION_CODE"` sets both Android `versionCode` and iOS `CFBundleVersion`.
- `run_number` is per workflow and does not change on re-run. Set an offset above the highest number
  already uploaded when migrating, and never rename the release workflow file without bumping the offset.
- Marketing version (`versionName`, `CFBundleShortVersionString`, `--build-name`) comes from the tag.

### 10. Quality gates fail the build before anything is signed

```yaml
# BAD: lint runs but never fails; release job does not depend on tests
- run: ./gradlew lint || true
release:
  runs-on: ubuntu-latest

# GOOD
verify:
  steps:
    - run: ./gradlew ktlintCheck detekt lint testDebugUnitTest koverVerify --continue
release:
  needs: verify
```

- Coverage thresholds live in the build (`koverVerify` rules) or a short script over `xccov` / `lcov`
  output, and the threshold is a number in the repo, not in someone's head.
- Lint baselines are fine for legacy debt; new issues fail the build. `verify` is a required check on `main`.
- Upload test reports with `if: always()` so failures can be diagnosed.

### 11. Obfuscation symbols and mapping files are kept per build

```yaml
# BAD: obfuscated release with nothing to symbolicate crashes
- run: flutter build appbundle --obfuscate --split-debug-info=build/symbols
# (build/symbols discarded with the runner)

# GOOD: symbols archived and sent to the crash reporter
- run: flutter build appbundle --release --obfuscate --split-debug-info=build/symbols --build-number="$VERSION_CODE"
- uses: actions/upload-artifact@<sha> # vX.Y.Z
  with:
    name: symbols-${{ env.VERSION_CODE }}
    path: build/symbols
    retention-days: 90
```

- Android R8 `mapping.txt`, iOS `dSYM`s and Flutter `--split-debug-info` output are archived with the
  build number in the name, and uploaded to Crashlytics or the crash reporter in use.
- Retention for crash symbols matches how long the release is supported.

### 12. Apple authentication uses an App Store Connect API key

```ruby
# BAD: Apple ID password and 2FA session cookies in CI
ENV["FASTLANE_PASSWORD"] = "..."
ENV["FASTLANE_SESSION"] = "..."

# GOOD: .p8 API key from secrets, scoped by role, revocable
api_key = app_store_connect_api_key(
  key_id: ENV.fetch("ASC_KEY_ID"),
  issuer_id: ENV.fetch("ASC_ISSUER_ID"),
  key_content: ENV.fetch("ASC_KEY_P8_BASE64"),
  is_key_content_base64: true
)
upload_to_testflight(api_key: api_key, skip_waiting_for_build_processing: true)
```

- Lowest role that covers the lane; a dedicated CI key, never a personal one.
- `match(readonly: true)` in CI. Creating or renewing certificates is a manual, reviewed operation.

### 13. Prefer short-lived credentials over stored keys

- Where the target supports it (Google Cloud and Firebase, AWS, Azure), use OIDC from the workflow
  (`id-token: write` plus the provider's auth action) instead of a long-lived JSON key.
- Where a stored key is unavoidable (Play service account JSON, App Store Connect `.p8`), scope it to one
  app, grant the minimum console role, and record a rotation date.

## Anti-patterns

- `pull_request_target` or `workflow_run` that checks out and builds PR code with secrets available.
- Third-party actions referenced by tag or branch, or `curl ... | bash` installers in release jobs.
- Workflow-level `permissions: write-all` or no `permissions:` block at all.
- Keystores, `.p12`, `.p8`, `google-services.json` with production keys, or passwords committed "temporarily".
- Signing release builds on every PR "to make sure signing works".
- `continue-on-error: true` or `|| true` on lint and test steps.
- Release jobs that re-run the whole verify pipeline in parallel instead of `needs:` on it.
- Uploading to the production track directly from CI without a staged rollout or a human approval.
- Caches shared between PR and release jobs without lockfile keys.
- Debug output (`set -x`, `--verbose`, `--debug`) left on in jobs that handle secrets.
- Hand-maintained version numbers that drift between Android, iOS and the tag.
- One giant job doing lint, tests, build and upload, so a flaky test blocks diagnosis of everything else.

## Checklist

Secure pipeline:
- [ ] Top-level `permissions: contents: read`; any extra scope granted per job with a comment
- [ ] Every third-party action pinned to a full commit SHA with a version comment; Dependabot enabled
- [ ] Container images pinned by digest; CLI tools pinned by exact version or lockfile
- [ ] No `pull_request_target`, `workflow_run` or comment-triggered job builds untrusted code with secrets
- [ ] Signing and store secrets are environment secrets behind required reviewers and ref rules
- [ ] Keystore and keys decoded into `$RUNNER_TEMP`, never written into the workspace or committed
- [ ] Secrets and event data reach scripts only through `env:`; no `set -x` or debug flags near them
- [ ] `persist-credentials: false` on checkout unless the job pushes
- [ ] App Store Connect API key used; no Apple ID password or session; `match` is `readonly`
- [ ] OIDC used where the provider supports it; remaining stored keys scoped and rotation-dated

Pipeline quality:
- [ ] Verify job runs lint, static analysis, unit tests and a coverage threshold, and fails on violations
- [ ] Release job `needs:` the verify job and runs only on tags, `main` or manual dispatch
- [ ] Concurrency group per workflow and ref; `cancel-in-progress` only for PRs
- [ ] `timeout-minutes` on every job; `paths:` filters on expensive macOS jobs
- [ ] Caches keyed on lockfiles; release jobs do not write caches from PR content
- [ ] versionCode and build number derived from the run number with a documented offset
- [ ] R8 mapping, dSYMs and Flutter split debug info archived per build and uploaded to the crash reporter
- [ ] Test and lint reports uploaded with `if: always()`
- [ ] `actionlint` and `zizmor` pass on the workflow files

## Output format

Deliver files, then a setup sheet. Do not invent secret values; name them and say how to create them.

~~~markdown
## CI/CD: <project> -- <platforms>

### Files
- `.github/workflows/android.yml` -- verify on PR, Firebase QA build on main, Play internal on tag
- `fastlane/Fastfile` -- lanes `android release`, `ios beta`
- `app/build.gradle.kts` -- signing config and versionCode from Gradle properties (diff below)

```yaml
<full workflow file>
```

### Required secrets
| Name | Scope | What it is | How to create |
|---|---|---|---|
| ANDROID_UPLOAD_KEYSTORE_BASE64 | env `play-production` | Upload keystore, base64 | `base64 -i upload.jks` (macOS) or `base64 -w0 upload.jks` (Linux) |
| PLAY_SERVICE_ACCOUNT_JSON | env `play-production` | Play Console service account key | Google Cloud service account, invited in Play Console with release permission for this app only |
| ASC_KEY_ID / ASC_ISSUER_ID / ASC_KEY_P8_BASE64 | env `testflight` | App Store Connect API key | Users and Access > Integrations, lowest role that can upload |

### Repository variables
| Name | Example | Purpose |
|---|---|---|
| VERSION_CODE_OFFSET | 1000 | Keeps versionCode above previously uploaded builds |

### Manual setup
1. Create environments `play-production`, `testflight` with required reviewers and tag rule `v*`.
2. Add the secrets above as environment secrets.
3. Branch protection on `main`: require the `verify` check.
4. Enable Dependabot for `github-actions`.
5. <store-side steps: Play App Signing enrolled, first AAB uploaded manually, TestFlight groups created>

### Verification
- `actionlint` and `zizmor` output
- Which jobs were run on a branch, and which were not run because they need secrets

### Open questions
- <tracks, groups, approvers or thresholds that need the owner's decision>
~~~

## Related skills

- `mobile-security` -- secret storage, MASVS and supply-chain review beyond the pipeline
- `mobile-merge-request` -- describing pipeline changes and required manual steps in the MR
- `mobile-code-review` -- reviewing Gradle, Fastfile and workflow changes alongside app code
- `mobile-kotlin`, `mobile-swift`, `mobile-flutter` -- build configuration conventions per platform
- `mobile-release` -- store readiness, tracks, phased rollout and rollback
- `mobile-testing` -- which test layers the pipeline runs and how to shard them
