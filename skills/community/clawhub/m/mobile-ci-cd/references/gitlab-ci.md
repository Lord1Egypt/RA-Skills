# GitLab CI

Load this when the project uses GitLab CI instead of GitHub Actions. The rules in SKILL.md apply
unchanged; this file maps them to GitLab keywords and shows a short Android pipeline. iOS and Flutter
jobs follow the same shape on a macOS runner and reuse the fastlane lanes from the
[iOS](ios-github-actions.md) and [Flutter](flutter-github-actions.md) references.

## Concept mapping

| GitHub Actions | GitLab CI |
|---|---|
| `uses: owner/action@<sha>` | `image: <image>@sha256:<digest>`, `include: project: ... ref: <commit-sha>` |
| `permissions:` | `CI_JOB_TOKEN` allowlist and project token access settings |
| Environment secrets with required reviewers | Protected and masked CI/CD variables, protected environments with deployment approvals |
| Secrets withheld from fork PRs | Protected variables are exposed only to pipelines on protected branches and tags |
| `concurrency` + `cancel-in-progress` | `interruptible: true` + auto-cancel redundant pipelines; `resource_group` for deploys |
| `github.run_number` | `CI_PIPELINE_IID` (per project, increasing) |
| OIDC `id-token: write` | `id_tokens:` keyword |
| `actions/upload-artifact` | `artifacts:` with `expire_in` |
| `paths:` filter | `rules: - changes:` |

## Variables

- Signing and store credentials are CI/CD variables that are protected (only on protected refs) and
  masked (or masked and hidden). Mark `v*` tags as protected tags so release pipelines receive them.
- Binary files (keystore, `.p8`) are stored base64-encoded and decoded at runtime. A File-type variable
  can hold text files such as the Play service account JSON; the variable then contains a path.
- Merge request pipelines from forks run in the fork project by default. A parent-project member can
  choose to run them in the parent project, which exposes its non-protected variables; review the fork's
  code, including `.gitlab-ci.yml`, before doing that.

## Pipeline: `.gitlab-ci.yml` (Android)

```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG =~ /^v/

stages: [verify, build, deploy]

default:
  image: <android-sdk-image>@sha256:<digest> # placeholder: JDK + Android SDK image, pinned by digest
  interruptible: true

variables:
  GRADLE_USER_HOME: $CI_PROJECT_DIR/.gradle

.gradle-cache: &gradle-cache
  key:
    files:
      - gradle/wrapper/gradle-wrapper.properties
      - gradle/libs.versions.toml
  paths:
    - .gradle/caches/
    - .gradle/wrapper/
  policy: pull

verify:
  stage: verify
  timeout: 30m
  cache:
    - <<: *gradle-cache   # read-only for MRs and tags
  rules:
    - if: $CI_COMMIT_BRANCH != $CI_DEFAULT_BRANCH
  script:
    - ./gradlew ktlintCheck detekt lint testDebugUnitTest koverVerify --continue
  artifacts:
    when: always
    expire_in: 14 days
    reports:
      junit: "**/build/test-results/**/TEST-*.xml"
    paths:
      - "**/build/reports/"

verify-main:
  extends: verify
  cache:
    - <<: *gradle-cache
      policy: pull-push   # only the default branch writes the cache
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

release:
  stage: build
  timeout: 45m
  interruptible: false
  needs: [verify]
  rules:
    - if: $CI_COMMIT_TAG =~ /^v/
  environment:
    name: play-production   # protected environment with deployment approval
  resource_group: play-store
  cache:
    - <<: *gradle-cache
  script:
    - export VERSION_CODE=$(( CI_PIPELINE_IID + ${VERSION_CODE_OFFSET:-0} ))
    - export ANDROID_KEYSTORE_PATH="$(mktemp -d)/upload.jks"
    - echo "$ANDROID_UPLOAD_KEYSTORE_BASE64" | base64 -d > "$ANDROID_KEYSTORE_PATH"
    - ./gradlew bundleRelease -PversionCode="$VERSION_CODE" -PversionName="${CI_COMMIT_TAG#v}"
    - bundle install
    - bundle exec fastlane android internal
  artifacts:
    expire_in: 90 days
    paths:
      - app/build/outputs/bundle/release/app-release.aab
      - app/build/outputs/mapping/release/mapping.txt
```

Notes:
- Only `verify-main` writes the Gradle cache, so merge request code cannot poison what release jobs
  restore. `cache:key:files` accepts at most two files.
- The release job assumes Ruby and Bundler are available in the image; otherwise use a separate,
  digest-pinned image for the upload step.
- Enable "Auto-cancel redundant pipelines" in the project CI/CD settings so `interruptible: true` jobs are
  cancelled by newer pipelines on the same ref. The release job sets `interruptible: false`.
- `resource_group` serialises store uploads so two tags never upload at the same time.
- Shell expansion works in `script:` lines, so arithmetic for `VERSION_CODE` is done there.
- `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD` and
  `PLAY_SERVICE_ACCOUNT_JSON` are protected, masked variables scoped to the `play-production` environment.
- Never enable `CI_DEBUG_TRACE` on jobs with protected variables; it prints every variable.

## iOS and Flutter on GitLab

```yaml
ios-testflight:
  stage: deploy
  tags: [macos]   # placeholder: tag of a GitLab-hosted or self-hosted macOS runner
  timeout: 60m
  interruptible: false
  needs: [verify]
  rules:
    - if: $CI_COMMIT_TAG =~ /^v/
  environment:
    name: testflight
  resource_group: testflight
  script:
    - export BUILD_NUMBER=$(( CI_PIPELINE_IID + ${BUILD_NUMBER_OFFSET:-0} ))
    - export MARKETING_VERSION="${CI_COMMIT_TAG#v}"
    - bundle install
    - bundle exec fastlane ios beta
  artifacts:
    expire_in: 90 days
    paths:
      - build/*.dSYM.zip
```

- Self-hosted macOS runners keep state between jobs. `setup_ci` uses a temporary keychain, but also clean
  derived data and never leave decoded keys on disk.
- Use `rules: - changes:` to run macOS jobs only when iOS or shared code changed.
