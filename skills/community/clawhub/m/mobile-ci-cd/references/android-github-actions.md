# Android on GitHub Actions

Load this when the pipeline builds a native Android app (Kotlin or Java, Gradle Kotlin DSL). Adapt module
names, flavors, tasks and package names to the project.

Pinning convention used in every file below: `@<sha>` is a placeholder for the full 40-character commit
SHA of the release named in the comment. Resolve it before committing (see Rule 1 in SKILL.md). Versions
in comments were valid at the time of writing; use the latest release when pinning.

## Workflow: `.github/workflows/android.yml`

```yaml
name: Android

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
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@<sha> # v7
        with:
          persist-credentials: false

      - uses: gradle/actions/wrapper-validation@<sha> # v6

      - uses: actions/setup-java@<sha> # v6
        with:
          distribution: temurin
          java-version: '21'

      - uses: gradle/actions/setup-gradle@<sha> # v6

      - name: Static analysis
        run: ./gradlew ktlintCheck detekt lint --continue

      - name: Unit tests and coverage gate
        run: ./gradlew testDebugUnitTest koverVerify --continue

      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@<sha> # v7
        with:
          name: verify-reports
          path: |
            **/build/reports/
            **/build/test-results/
          retention-days: 14

  instrumented:
    needs: verify
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 45
    strategy:
      fail-fast: false
      matrix:
        api-level: [29, 35]
    steps:
      - uses: actions/checkout@<sha> # v7
        with:
          persist-credentials: false
      - uses: actions/setup-java@<sha> # v6
        with:
          distribution: temurin
          java-version: '21'
      - uses: gradle/actions/setup-gradle@<sha> # v6
      - name: Enable KVM
        run: |
          echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules
          sudo udevadm control --reload-rules
          sudo udevadm trigger --name-match=kvm
      - uses: reactivecircus/android-emulator-runner@<sha> # v2
        with:
          api-level: ${{ matrix.api-level }}
          arch: x86_64
          target: google_apis
          script: ./gradlew connectedDebugAndroidTest

  firebase-qa:
    needs: verify
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 30
    environment: firebase-qa
    permissions:
      contents: read
      id-token: write # OIDC to Google Cloud, no stored JSON key
    steps:
      - uses: actions/checkout@<sha> # v7
        with:
          persist-credentials: false
      - uses: actions/setup-java@<sha> # v6
        with:
          distribution: temurin
          java-version: '21'
      - uses: gradle/actions/setup-gradle@<sha> # v6
        with:
          cache-read-only: true

      - name: Compute versionCode
        env:
          VERSION_CODE_OFFSET: ${{ vars.VERSION_CODE_OFFSET }}
        run: echo "VERSION_CODE=$(( GITHUB_RUN_NUMBER + ${VERSION_CODE_OFFSET:-0} ))" >> "$GITHUB_ENV"

      - name: Build QA APK
        run: ./gradlew assembleQa -PversionCode="$VERSION_CODE"

      - uses: google-github-actions/auth@<sha> # v3
        with:
          workload_identity_provider: ${{ vars.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ vars.GCP_DISTRIBUTION_SERVICE_ACCOUNT }}

      - name: Distribute to testers
        env:
          FIREBASE_APP_ID: ${{ vars.FIREBASE_ANDROID_APP_ID }}
        run: |
          npx --yes firebase-tools@<x.y.z> appdistribution:distribute \
            app/build/outputs/apk/qa/app-qa.apk \
            --app "$FIREBASE_APP_ID" \
            --groups "qa" \
            --release-notes "main @ ${GITHUB_SHA::8}, build $VERSION_CODE"

  release:
    needs: verify
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    timeout-minutes: 45
    environment: play-production # required reviewers + tag rule v*
    steps:
      - uses: actions/checkout@<sha> # v7
        with:
          persist-credentials: false
      - uses: actions/setup-java@<sha> # v6
        with:
          distribution: temurin
          java-version: '21'
      - uses: gradle/actions/setup-gradle@<sha> # v6
        with:
          cache-read-only: true
      - uses: ruby/setup-ruby@<sha> # v1
        with:
          bundler-cache: true

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

      - name: Build signed AAB
        env:
          ANDROID_KEYSTORE_PASSWORD: ${{ secrets.ANDROID_KEYSTORE_PASSWORD }}
          ANDROID_KEY_ALIAS: ${{ secrets.ANDROID_KEY_ALIAS }}
          ANDROID_KEY_PASSWORD: ${{ secrets.ANDROID_KEY_PASSWORD }}
        run: ./gradlew bundleRelease -PversionCode="$VERSION_CODE" -PversionName="$VERSION_NAME"

      - name: Archive AAB and R8 mapping
        uses: actions/upload-artifact@<sha> # v7
        with:
          name: release-${{ env.VERSION_CODE }}
          path: |
            app/build/outputs/bundle/release/app-release.aab
            app/build/outputs/mapping/release/mapping.txt
          retention-days: 90

      - name: Upload to Play internal track
        env:
          PLAY_SERVICE_ACCOUNT_JSON: ${{ secrets.PLAY_SERVICE_ACCOUNT_JSON }}
        run: bundle exec fastlane android internal
```

Notes:
- `instrumented` and `firebase-qa` run on `main` only; the PR path stays fast and secret-free.
- The `qa` build type is assumed to exist and to be signed with a non-production key (or the debug key).
  Firebase App Distribution accepts AABs only when the Firebase project is linked to Play, so APK is the
  simpler default for QA.
- `environment:` on `firebase-qa` and `release` holds the secrets and variables those jobs need.
- If the Play account cannot use OIDC with the upload tool, the JSON key is an environment secret, not a
  repository secret.

## Gradle: signing and version from CI (`app/build.gradle.kts`)

```kotlin
android {
    defaultConfig {
        versionCode = providers.gradleProperty("versionCode").orNull?.toInt() ?: 1
        versionName = providers.gradleProperty("versionName").orNull ?: "0.0.0-dev"
    }

    signingConfigs {
        create("release") {
            val keystorePath = providers.environmentVariable("ANDROID_KEYSTORE_PATH").orNull
            if (keystorePath != null) {
                storeFile = file(keystorePath)
                storePassword = providers.environmentVariable("ANDROID_KEYSTORE_PASSWORD").get()
                keyAlias = providers.environmentVariable("ANDROID_KEY_ALIAS").get()
                keyPassword = providers.environmentVariable("ANDROID_KEY_PASSWORD").get()
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

- No passwords in `gradle.properties`, `local.properties` or the build file.
- A local `bundleRelease` without the environment variables fails at signing. That is intended: release
  builds come from CI.
- `versionCode` must stay below 2100000000. Keep the offset small.

## Coverage threshold (Kover)

```kotlin
// build.gradle.kts of the module (or the root, if Kover merges modules)
kover {
    reports {
        verify {
            rule {
                minBound(80)
            }
        }
    }
}
```

- Exclude generated code (Hilt, Room, Compose previews, DI modules) through Kover filters so the number
  measures real logic.
- Raise the threshold over time; never lower it to make a PR pass without a recorded decision.
- JaCoCo with a `JacocoCoverageVerification` task is an equivalent alternative if the project already uses it.

## Fastlane: Play upload (`fastlane/Fastfile`)

```ruby
default_platform(:android)

platform :android do
  lane :internal do
    upload_to_play_store(
      package_name: "com.example.app",
      track: "internal",
      aab: ENV.fetch("AAB_PATH", "app/build/outputs/bundle/release/app-release.aab"),
      json_key_data: ENV.fetch("PLAY_SERVICE_ACCOUNT_JSON"),
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true,
      release_status: "completed"
    )
  end

  lane :promote_production do
    upload_to_play_store(
      package_name: "com.example.app",
      track: "internal",
      track_promote_to: "production",
      rollout: "0.1",
      json_key_data: ENV.fetch("PLAY_SERVICE_ACCOUNT_JSON"),
      skip_upload_changelogs: true,
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end
end
```

- `upload_to_play_store` is the action behind `fastlane supply`.
- Use `release_status: "draft"` while the app has never been published; Play rejects completed releases
  for draft apps.
- Commit `Gemfile` and `Gemfile.lock` so the fastlane version is pinned.
- The Play service account is invited in Play Console with release permissions for this app only, not
  admin on the developer account.
- Production promotion is a separate, manually triggered lane with a staged rollout, not part of the tag job.

## Secrets and variables

| Name | Kind | Scope |
|---|---|---|
| `ANDROID_UPLOAD_KEYSTORE_BASE64` | secret | env `play-production` |
| `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD` | secret | env `play-production` |
| `PLAY_SERVICE_ACCOUNT_JSON` | secret | env `play-production` |
| `VERSION_CODE_OFFSET` | variable | repository |
| `GCP_WORKLOAD_IDENTITY_PROVIDER`, `GCP_DISTRIBUTION_SERVICE_ACCOUNT`, `FIREBASE_ANDROID_APP_ID` | variable | env `firebase-qa` |

Create the keystore secret with `base64 -i upload.jks | pbcopy` (macOS) or `base64 -w0 upload.jks` (Linux)
and paste it into the environment secret form. Delete any local plaintext copies of passwords afterwards.
