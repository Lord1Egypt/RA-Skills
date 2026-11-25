# iOS on GitHub Actions

Load this when the pipeline builds a native iOS app (Swift, Xcode project or workspace, SPM dependencies).
Adapt workspace, scheme, bundle id and simulator names to the project.

Pinning convention: `@<sha>` is a placeholder for the full 40-character commit SHA of the release named
in the comment. Resolve it before committing. Versions in comments were valid at the time of writing.

## Before writing the workflow

- Check the runner image's installed Xcode versions and simulators in the `actions/runner-images`
  documentation for the chosen macOS label. Do not assume a path or device name exists.
- App Store uploads must be built with the minimum Xcode and SDK Apple currently requires. Pick the
  runner label and Xcode version from that, not from what is cheapest.
- Release signing uses manual signing in the Release configuration with the `match` profile names, or
  `match` updates the project with `update_code_signing_settings`. Decide which before writing lanes.
- Any `Info.plist`, entitlement or capability change needed for CI (for example a new app group) is
  called out to the owner, because the provisioning profiles must be regenerated.

## Workflow: `.github/workflows/ios.yml`

```yaml
name: iOS

on:
  pull_request:
    paths:
      - 'ios/**'
      - 'fastlane/**'
      - 'Gemfile.lock'
      - '.github/workflows/ios.yml'
  push:
    tags: ['v*']
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

env:
  XCODE_VERSION: '<xcode-version-on-runner>' # placeholder, for example the value listed in the image README
  WORKSPACE: ios/App.xcworkspace
  SCHEME: App

jobs:
  test:
    runs-on: macos-15 # choose the image that ships the required Xcode
    timeout-minutes: 40
    steps:
      - uses: actions/checkout@<sha> # v7
        with:
          persist-credentials: false

      - name: Select Xcode
        run: sudo xcode-select -s "/Applications/Xcode_${XCODE_VERSION}.app"

      - uses: actions/cache@<sha> # v6
        with:
          path: SourcePackages
          key: spm-${{ runner.os }}-${{ env.XCODE_VERSION }}-${{ hashFiles('**/Package.resolved') }}
          restore-keys: spm-${{ runner.os }}-${{ env.XCODE_VERSION }}-

      - name: Lint
        run: swiftlint lint --strict # assumes SwiftLint is provided (SPM plugin, Mint or Homebrew)

      - name: Unit tests
        run: |
          set -o pipefail
          xcodebuild test \
            -workspace "$WORKSPACE" \
            -scheme "$SCHEME" \
            -destination 'platform=iOS Simulator,name=<simulator-on-runner>,OS=latest' \
            -clonedSourcePackagesDirPath SourcePackages \
            -disableAutomaticPackageResolution \
            -enableCodeCoverage YES \
            -resultBundlePath "$RUNNER_TEMP/Tests.xcresult" \
            CODE_SIGNING_ALLOWED=NO

      - name: Coverage gate
        env:
          MIN_COVERAGE: '0.70'
        run: |
          COVERAGE=$(xcrun xccov view --report --json "$RUNNER_TEMP/Tests.xcresult" | jq '.lineCoverage')
          echo "Line coverage: $COVERAGE"
          awk -v c="$COVERAGE" -v min="$MIN_COVERAGE" 'BEGIN { exit (c + 0 < min + 0) }'

      - name: Upload result bundle
        if: failure()
        uses: actions/upload-artifact@<sha> # v7
        with:
          name: test-results
          path: ${{ runner.temp }}/Tests.xcresult
          retention-days: 7

  testflight:
    needs: test
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: macos-15
    timeout-minutes: 60
    environment: testflight # required reviewers + tag rule v*
    steps:
      - uses: actions/checkout@<sha> # v7
        with:
          persist-credentials: false

      - name: Select Xcode
        run: sudo xcode-select -s "/Applications/Xcode_${XCODE_VERSION}.app"

      - uses: actions/cache/restore@<sha> # v6
        with:
          path: SourcePackages
          key: spm-${{ runner.os }}-${{ env.XCODE_VERSION }}-${{ hashFiles('**/Package.resolved') }}

      - uses: ruby/setup-ruby@<sha> # v1
        with:
          bundler-cache: true

      - name: Compute build number
        env:
          BUILD_NUMBER_OFFSET: ${{ vars.BUILD_NUMBER_OFFSET }}
        run: |
          echo "BUILD_NUMBER=$(( GITHUB_RUN_NUMBER + ${BUILD_NUMBER_OFFSET:-0} ))" >> "$GITHUB_ENV"
          echo "MARKETING_VERSION=${GITHUB_REF_NAME#v}" >> "$GITHUB_ENV"

      - name: Build and upload to TestFlight
        env:
          ASC_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          ASC_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          ASC_KEY_P8_BASE64: ${{ secrets.ASC_KEY_P8_BASE64 }}
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_BASIC_AUTHORIZATION }}
        run: bundle exec fastlane ios beta

      - name: Archive dSYMs
        uses: actions/upload-artifact@<sha> # v7
        with:
          name: dsyms-${{ env.BUILD_NUMBER }}
          path: build/*.dSYM.zip
          retention-days: 90
```

Notes:
- The release job uses `actions/cache/restore` only, so a PR cannot poison what the release build links.
- `-disableAutomaticPackageResolution` makes the build fail if `Package.resolved` is out of date instead
  of silently resolving new versions.
- `paths:` keeps Android-only PRs off macOS runners. If the iOS check is required on `main`, add a
  lightweight always-running job with the same name or the PR will wait for a check that never starts.

## Fastlane (`fastlane/Fastfile`)

```ruby
default_platform(:ios)

platform :ios do
  lane :beta do
    setup_ci # temporary keychain on CI, no changes to the login keychain

    api_key = app_store_connect_api_key(
      key_id: ENV.fetch("ASC_KEY_ID"),
      issuer_id: ENV.fetch("ASC_ISSUER_ID"),
      key_content: ENV.fetch("ASC_KEY_P8_BASE64"),
      is_key_content_base64: true
    )

    match(type: "appstore", readonly: true, api_key: api_key)

    build_app(
      workspace: "ios/App.xcworkspace",
      scheme: "App",
      configuration: "Release",
      export_method: "app-store",
      cloned_source_packages_path: "SourcePackages",
      output_directory: "build",
      xcargs: "CURRENT_PROJECT_VERSION=#{ENV.fetch('BUILD_NUMBER')} MARKETING_VERSION=#{ENV.fetch('MARKETING_VERSION')}"
    )

    upload_to_testflight(
      api_key: api_key,
      skip_waiting_for_build_processing: true
    )
  end
end
```

`fastlane/Matchfile`:

```ruby
git_url("https://github.com/<org>/<certificates-repo>.git")
storage_mode("git")
type("appstore")
app_identifier(["com.example.app"])
```

- `MATCH_GIT_BASIC_AUTHORIZATION` is base64 of `user:token` for a token that can only read the
  certificates repository. A deploy key or a cloud storage backend for `match` is equally fine.
- `MATCH_PASSWORD` decrypts the repository. Losing it means regenerating certificates; store it in a
  password manager as well as in CI.
- `CURRENT_PROJECT_VERSION` and `MARKETING_VERSION` overrides work when `Info.plist` uses
  `$(CURRENT_PROJECT_VERSION)` and `$(MARKETING_VERSION)`, which is the default for current Xcode templates.
  Older projects with hardcoded values need that change first.
- Build numbers must increase for each upload of the same marketing version. Set `BUILD_NUMBER_OFFSET`
  above the highest build already in App Store Connect when migrating.
- Upload dSYMs to the crash reporter in the same lane (for example `upload_symbols_to_crashlytics`) when
  the project uses one.

## App Store Connect API key

- Created in App Store Connect under Users and Access, Integrations. The `.p8` file can be downloaded only once.
- Store as `ASC_KEY_P8_BASE64` (`base64 -i AuthKey_XXXX.p8`), with `ASC_KEY_ID` and `ASC_ISSUER_ID`, as
  environment secrets of `testflight`.
- Use a team key with the lowest role that can upload and manage TestFlight for the lanes in use. Revoke
  it when the pipeline is retired or the key may have leaked.
- Never use `FASTLANE_USER` / `FASTLANE_PASSWORD`, app-specific passwords or `FASTLANE_SESSION` in CI.

## Firebase App Distribution (ad hoc builds)

- Needs an `adhoc` (or enterprise) profile from `match(type: "adhoc", readonly: true)` and tester devices
  registered in the profile. TestFlight internal testing is usually simpler for iOS QA.
- Upload with the Firebase CLI (`firebase appdistribution:distribute <ipa> --app <id> --groups <group>`)
  after authenticating with OIDC via `google-github-actions/auth`, as in the Android reference.

## Secrets and variables

| Name | Kind | Scope |
|---|---|---|
| `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_P8_BASE64` | secret | env `testflight` |
| `MATCH_PASSWORD`, `MATCH_GIT_BASIC_AUTHORIZATION` | secret | env `testflight` |
| `BUILD_NUMBER_OFFSET` | variable | repository |
