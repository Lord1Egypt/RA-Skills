# Flutter on GitHub Actions

Load this when the pipeline builds a Flutter app for Android and iOS. Platform-specific signing and store
upload follow the [Android](android-github-actions.md) and [iOS](ios-github-actions.md) references; this
file covers what changes for Flutter.

Pinning convention: `@<sha>` is a placeholder for the full 40-character commit SHA of the release named
in the comment. Resolve it before committing. Versions in comments were valid at the time of writing.

## Assumptions

- Flavors `staging` and `prod`, with entry points `lib/main_staging.dart` and `lib/main_prod.dart`, and
  matching Android product flavors and iOS schemes. Ask the owner if the project differs.
- The Flutter version is pinned in `pubspec.yaml` (`environment: flutter:`) or in the workflow, and
  `pubspec.lock` is committed.
- Android Gradle reads signing from environment variables exactly as in the Android reference. Do not set
  `versionCode` in Gradle; Flutter passes `--build-number` through.

## Workflow: `.github/workflows/flutter.yml`

```yaml
name: Flutter

on:
  pull_request:
  push:
    branches: [main]
    tags: ['v*']
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  verify:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@<sha> # v7
        with:
          persist-credentials: false

      - uses: subosito/flutter-action@<sha> # v2
        with:
          channel: stable
          flutter-version-file: pubspec.yaml
          cache: true

      - run: flutter pub get --enforce-lockfile
      - run: dart format --output=none --set-exit-if-changed .
      - run: flutter analyze --fatal-infos
      - run: flutter test --coverage

      - name: Coverage gate
        env:
          MIN_COVERAGE: '70'
        run: |
          awk -F: -v min="$MIN_COVERAGE" '
            /^LF:/ { found += $2 }
            /^LH:/ { hit += $2 }
            END {
              pct = found ? hit * 100 / found : 0
              printf "Line coverage: %.1f%%\n", pct
              exit (pct < min)
            }' coverage/lcov.info

  android:
    needs: verify
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    timeout-minutes: 40
    environment: android-release # required reviewers + tag rule v*
    permissions:
      contents: read
      id-token: write # OIDC for Firebase App Distribution
    strategy:
      fail-fast: false
      matrix:
        include:
          - flavor: staging
            target: apk
          - flavor: prod
            target: appbundle
    steps:
      - uses: actions/checkout@<sha> # v7
        with:
          persist-credentials: false
      - uses: actions/setup-java@<sha> # v6
        with:
          distribution: temurin
          java-version: '21'
      - uses: subosito/flutter-action@<sha> # v2
        with:
          channel: stable
          flutter-version-file: pubspec.yaml
          cache: true

      - name: Compute versions
        env:
          VERSION_CODE_OFFSET: ${{ vars.VERSION_CODE_OFFSET }}
        run: |
          echo "VERSION_CODE=$(( GITHUB_RUN_NUMBER + ${VERSION_CODE_OFFSET:-0} ))" >> "$GITHUB_ENV"
          echo "VERSION_NAME=${GITHUB_REF_NAME#v}" >> "$GITHUB_ENV"

      - name: Decode upload keystore
        env:
          KEYSTORE_BASE64: ${{ secrets.ANDROID_UPLOAD_KEYSTORE_BASE64 }}
        run: |
          echo "$KEYSTORE_BASE64" | base64 --decode > "$RUNNER_TEMP/upload.jks"
          echo "ANDROID_KEYSTORE_PATH=$RUNNER_TEMP/upload.jks" >> "$GITHUB_ENV"

      - name: Build
        env:
          ANDROID_KEYSTORE_PASSWORD: ${{ secrets.ANDROID_KEYSTORE_PASSWORD }}
          ANDROID_KEY_ALIAS: ${{ secrets.ANDROID_KEY_ALIAS }}
          ANDROID_KEY_PASSWORD: ${{ secrets.ANDROID_KEY_PASSWORD }}
          FLAVOR: ${{ matrix.flavor }}
          TARGET: ${{ matrix.target }}
        run: |
          flutter build "$TARGET" --release \
            --flavor "$FLAVOR" \
            -t "lib/main_${FLAVOR}.dart" \
            --dart-define-from-file="config/${FLAVOR}.json" \
            --obfuscate \
            --split-debug-info="build/symbols/android-${FLAVOR}" \
            --build-number="$VERSION_CODE" \
            --build-name="$VERSION_NAME"

      - name: Keep binaries, symbols and mapping
        uses: actions/upload-artifact@<sha> # v7
        with:
          name: android-${{ matrix.flavor }}-${{ env.VERSION_CODE }}
          path: |
            build/app/outputs/flutter-apk/*.apk
            build/app/outputs/bundle/${{ matrix.flavor }}Release/*.aab
            build/app/outputs/mapping/${{ matrix.flavor }}Release/mapping.txt
            build/symbols/android-${{ matrix.flavor }}
          retention-days: 90

      # staging: testers via Firebase App Distribution
      - if: matrix.flavor == 'staging'
        uses: google-github-actions/auth@<sha> # v3
        with:
          workload_identity_provider: ${{ vars.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ vars.GCP_DISTRIBUTION_SERVICE_ACCOUNT }}
      - if: matrix.flavor == 'staging'
        env:
          FIREBASE_APP_ID: ${{ vars.FIREBASE_ANDROID_STAGING_APP_ID }}
        run: |
          npx --yes firebase-tools@<x.y.z> appdistribution:distribute \
            build/app/outputs/flutter-apk/app-staging-release.apk \
            --app "$FIREBASE_APP_ID" --groups "qa"

      # prod: Play internal track, lane as in the Android reference with the Flutter AAB path
      - if: matrix.flavor == 'prod'
        uses: ruby/setup-ruby@<sha> # v1
        with:
          bundler-cache: true
          working-directory: android
      - if: matrix.flavor == 'prod'
        working-directory: android
        env:
          PLAY_SERVICE_ACCOUNT_JSON: ${{ secrets.PLAY_SERVICE_ACCOUNT_JSON }}
          AAB_PATH: ${{ github.workspace }}/build/app/outputs/bundle/prodRelease/app-prod-release.aab
        run: bundle exec fastlane android internal
```

Matrix notes:
- A job-level `if:` is evaluated before the matrix expands and cannot read `matrix`. Filter per entry
  with step-level `if: matrix.flavor == '...'`, or split into separate jobs.
- `fail-fast: false` so a staging failure does not cancel an in-flight prod upload.
- `upload-artifact` warns, not fails, on path patterns that match nothing, so one path list can serve
  both targets.
- For a staging build on every push to `main`, add a second job with the same steps and only the
  staging entry; keep prod on tags.

## iOS job

```yaml
  ios:
    needs: verify
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: macos-15
    timeout-minutes: 60
    environment: testflight
    steps:
      - uses: actions/checkout@<sha> # v7
        with:
          persist-credentials: false
      - uses: subosito/flutter-action@<sha> # v2
        with:
          channel: stable
          flutter-version-file: pubspec.yaml
          cache: true
      - uses: ruby/setup-ruby@<sha> # v1
        with:
          bundler-cache: true
          working-directory: ios

      - name: Compute build number
        env:
          BUILD_NUMBER_OFFSET: ${{ vars.BUILD_NUMBER_OFFSET }}
        run: echo "BUILD_NUMBER=$(( GITHUB_RUN_NUMBER + ${BUILD_NUMBER_OFFSET:-0} ))" >> "$GITHUB_ENV"

      - name: Signing, build and upload
        working-directory: ios
        env:
          ASC_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          ASC_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          ASC_KEY_P8_BASE64: ${{ secrets.ASC_KEY_P8_BASE64 }}
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_BASIC_AUTHORIZATION }}
        run: bundle exec fastlane ios beta

      - name: Keep symbols
        uses: actions/upload-artifact@<sha> # v7
        with:
          name: ios-prod-${{ env.BUILD_NUMBER }}
          path: |
            build/symbols/ios-prod
            build/ios/archive/*.xcarchive/dSYMs
          retention-days: 90
```

`ios/fastlane/Fastfile`:

```ruby
default_platform(:ios)

platform :ios do
  lane :beta do
    setup_ci
    api_key = app_store_connect_api_key(
      key_id: ENV.fetch("ASC_KEY_ID"),
      issuer_id: ENV.fetch("ASC_ISSUER_ID"),
      key_content: ENV.fetch("ASC_KEY_P8_BASE64"),
      is_key_content_base64: true
    )
    match(type: "appstore", readonly: true, api_key: api_key)

    Dir.chdir("../..") do
      sh(
        "flutter", "build", "ipa", "--release",
        "--flavor", "prod",
        "-t", "lib/main_prod.dart",
        "--dart-define-from-file=config/prod.json",
        "--obfuscate",
        "--split-debug-info=build/symbols/ios-prod",
        "--build-number=#{ENV.fetch('BUILD_NUMBER')}",
        "--export-options-plist=ios/ExportOptions.plist"
      )
    end

    ipa = Dir[File.join(File.expand_path("../.."), "build/ios/ipa/*.ipa")].first
    UI.user_error!("No IPA produced") if ipa.nil?
    upload_to_testflight(api_key: api_key, ipa: ipa, skip_waiting_for_build_processing: true)
  end
end
```

- Plain Ruby in a Fastfile runs with `ios/fastlane` as the working directory, while actions resolve
  paths from `ios/`. Absolute paths (as above) avoid mixing the two up.
- `ios/ExportOptions.plist` sets `method` to App Store distribution, manual signing, and maps the bundle
  id to the `match AppStore <bundle id>` profile.
- The Xcode project's Release configuration for the `prod` scheme uses manual signing with that profile.

## Obfuscation symbols

- `--obfuscate` requires `--split-debug-info`. The directory holds the symbol files needed to read Dart
  stack traces; without them, production crashes are unreadable.
- Archive them per flavor and build number, and upload them to the crash reporter. For Crashlytics:
  `firebase crashlytics:symbols:upload --app=<firebase-app-id> build/symbols/<dir>`.
- Symbolicate a stored trace manually with
  `flutter symbolize -i <stack-trace-file> -d <symbols-dir>/<file>.symbols`.
- Never ship the symbols directory inside the app or commit it.

## Configuration and secrets

- `--dart-define` and `--dart-define-from-file` values are compiled into the binary and are readable by
  anyone with the APK or IPA. Use them for environment URLs and feature flags, never for API secrets.
- `config/<flavor>.json` files hold non-secret configuration and can be committed. Anything secret stays
  server side.
- Secrets and variables are the union of the Android and iOS tables, scoped to the same environments.
