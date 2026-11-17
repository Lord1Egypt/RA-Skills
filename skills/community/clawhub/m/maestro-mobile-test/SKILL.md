---
name: maestro-mobile-test
description: >-
    Write and run E2E tests for React Native / Expo apps using Maestro CLI — the open-source tool that drives the **real native app** on an Android emulator or iOS simulator, not a web build. Covers what browser-based e2e (Playwright, Expect, e2e-verify) cannot reach: native components, biometrics, secure storage, push notifications, platform-specific modules. Write YAML flows, run headed for authoring or headless for CI. Scripts currently automate the Android workflow end-to-end (Java + SDK detection, emulator boot, adb reverse); iOS simulator setup requires Xcode + `xcrun simctl` and is documented but not automated by the setup script. Use this skill whenever the user says "test my react native app", "e2e test the mobile app", "write maestro tests", "test the expo app", "automate emulator testing", or "/maestro-mobile-test" — even if they don't name the skill. Not for web apps (e2e-verify), unit/component tests (write-tests with RNTL + Jest), or API contract tests.
---

# Maestro Mobile Test

The browser is the wrong tool for a React Native app — it renders to native components (UIView / android.view), not a DOM. Maestro drives the **actual native binary** on a real emulator/simulator: real taps, real native assertions, real platform behavior. It's the open-source (Apache-2.0) standard for RN E2E, and it writes tests as YAML flows — no test framework setup, no instrumentation in your app code.

The discipline is identical to `e2e-verify`'s Route B (durable tests): ration by journey risk, selectors a user would recognize, prove red-capable, quote the run summary. What changes is the surface — native instead of browser — and the harness-specific pitfalls that will eat your time if you don't know them.

## When to use this skill

- The user says "test my react native app", "e2e the mobile app", "write maestro tests", "test the expo app", "automate emulator testing", "/maestro-mobile-test".
- A React Native / Expo feature just shipped and needs runtime proof beyond Jest component tests.
- A flow involves native modules (`expo-local-authentication`, `expo-secure-store`, `expo-notifications`) that no browser-based tool can reach.

Do **not** auto-trigger for web app e2e (`e2e-verify` — Playwright/Expect), unit/component authoring (`write-tests` — RNTL + Jest), or API contract tests.

## Prerequisites

| Requirement | How to check | Install |
|---|---|---|
| Java 17+ | `java -version` | `brew install --cask temurin@17` (macOS), `sudo apt install openjdk-17-jdk` (Linux), `winget install Microsoft.OpenJDK.17` (Windows) — or run `scripts/setup.sh` which auto-installs |
| Android SDK | `echo $ANDROID_HOME` | Android Studio |
| AVD (emulator image) | `emulator -list-avds` | Android Studio → AVD Manager |
| Maestro CLI | `maestro --version` | `curl -Ls https://get.maestro.mobile.dev \| bash` — or run `scripts/setup.sh` |
| Built APK (Android) | Check `android/app/build/outputs/apk/` | `cd android && ./gradlew assembleDebug` |

### Environment setup

The `scripts/setup.sh` handles everything — it detects your OS (macOS, Linux, Windows/git-bash) and installs the prerequisites in the right locations:

- **Java JDK 17+** — auto-installed via Homebrew (macOS), apt/dnf (Linux), or winget (Windows)
- **Android SDK** — detected from standard locations (`ANDROID_HOME`, or `~/Library/Android/sdk`, `~/AppData/Local/Android/Sdk`, `/opt/android-sdk`)
- **Maestro CLI** — installed to `~/.maestro/bin`

```bash
bash skills/maestro-mobile-test/scripts/setup.sh
```

After setup, activate before running tests:

```bash
source ~/.maestro/activate.sh
```

## The pitfalls that will cost you hours

These are not theoretical. Each one was learned by hitting it in a real Expo app.

### ⚠️ Pitfall 1: Dev builds are fragile under Maestro — use a debug APK

An Expo **dev build** (the kind you get from `npx expo start`) needs a live Metro bundler connection. Maestro's `launchApp` cold-starts the app, which **drops the Metro connection**. The app then shows the Expo Dev Launcher instead of your screens.

**Strategy A — Dev build (local authoring only):**
1. Start `npx expo start`, connect the app to Metro *before* running Maestro
2. Never use `launchApp` with `clearState: true`
3. Use `extendedWaitUntil` to give the app time to reconnect
4. **WARNING:** Even connected, dev builds break: `back` exits to the launcher, `hideKeyboard` backgrounds the app, rapid hot reloads crash native modules. Fine for authoring. Not fine for reliable runs.

**Strategy B — Debug APK (recommended for reliable runs and CI):**
```bash
cd android && ./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```
Now Maestro can `launchApp` freely — the JS bundle is compiled into the APK. No Metro, no fragility.

### ⚠️ Pitfall 2: The emulator cannot reach your localhost

The Android emulator runs in its own network namespace. `localhost:8888` inside the emulator means the emulator itself — not your machine's backend.

**Symptom:** App shows "Connection error" / "Couldn't load" even though your backend runs fine on `localhost:8888`.

**Fix — `adb reverse` (standard pattern, run before launching the app):**
```bash
adb reverse tcp:8888 tcp:8888   # map emulator localhost:8888 → host localhost:8888
adb reverse tcp:8081 tcp:8081   # Metro, if using a dev build
```
This resets on emulator reboot — re-run it each session.

### ⚠️ Pitfall 3: `timeout` is NOT a property of `assertVisible`

```yaml
# WRONG — "Unknown Property: timeout"
- assertVisible:
    text: "Welcome"
    timeout: 10000

# CORRECT — use extendedWaitUntil for timed waits
- extendedWaitUntil:
    visible: "Welcome"
    timeout: 10000
```

### ⚠️ Pitfall 4: Icon-only buttons need accessibility labels

MaterialIcons buttons have no text for Maestro to match. Add `testID` and `accessibilityLabel` to the source:

```tsx
// Before — Maestro cannot tap this reliably (no text to match)
<TouchableOpacity onPress={...}>
  <MaterialIcons name="add" size={28} color="..." />
</TouchableOpacity>

// After — Maestro taps by accessibility label
<TouchableOpacity
  onPress={...}
  testID="add-item-button"
  accessible={true}
  accessibilityLabel="Add Item"
>
  <MaterialIcons name="add" size={28} color="..." />
</TouchableOpacity>
```
Then: `- tapOn: "Add Item"`

### ⚠️ Pitfall 5: `hideKeyboard` and `back` exit dev builds

On dev builds, both can send the app to the home screen. Dismiss the keyboard by tapping a non-interactive element instead:

```yaml
# WRONG — can exit the app on dev builds
- hideKeyboard
- back

# CORRECT — tap a header to blur the input
- tapOn: "Screen Title"
- waitForAnimationToEnd
```

## Maestro YAML command reference

```yaml
appId: com.example.app
---
# Assertions
- assertVisible: "Text"
- extendedWaitUntil:
    visible: "Text"
    timeout: 20000

# Taps and input
- tapOn: "Button Label"
- tapOn:
    id: "add-button"
- doubleTapOn: "Text"
- longPressOn: "Text"
- inputText: "Hello"

# Navigation
- back
- swipe:
    direction: UP
- scrollUntilVisible:
    element: "Target Text"

# Waits
- waitForAnimationToEnd

# App control
- launchApp:
    appId: com.example.app
    clearState: false
- killApp: com.example.app

# Conditionals / branching (runFlow with when condition)
- runFlow:
    when:
      visible: "Welcome"
    commands:
      - tapOn: "Get Started"

# Repeat a sequence
- repeat:
    times: 3
    commands:
      - tapOn: "Next"

# Screenshots
- captureScreenshot: "step-name"

# Deep links
- openLink: myapp://screen/path

# Sub-flow inclusion (essential for suite patterns)
- runFlow: ../setup.yaml          # run another flow file
- runFlow: ../config.yaml         # shared config

# Visibility negation
- assertNotVisible: "Loading..."

# Text extraction (store for later assertions)
- copyTextFrom:
    id: "total-amount"
- assertTrue: ${output.total-amount} == "$54.20"

# Input helpers
- inputRandomEmail                # generates and types a random email
- pasteText                       # paste from clipboard

# Location mocking (travel)
- travel:
    points: "37.7749,-122.4194"

# Media injection (camera roll)
- addMedia:
    - "./test-assets/photo.jpg"
```

## Directory convention

```
project-root/
├── .maestro/
│   ├── navigation/
│   │   ├── tab-nav.yaml
│   │   └── dashboard-elements.yaml
│   ├── features/
│   │   ├── create-item.yaml
│   │   └── view-list.yaml
│   └── suites/
│       ├── smoke.yaml            # fast: navigation + visibility (pre-merge)
│       └── regression.yaml       # full: all flows (pre-release)
```

**Suite levels:**
- **Smoke** (~30s): structural checks — tabs work, screens load, elements visible. Every PR.
- **Regression** (~3-5 min): full lifecycle tests — create/edit/delete. Before release.

## Running tests

### Headed (authoring/debugging — you watch the taps)

```bash
# Boot emulator
$ANDROID_HOME/emulator/emulator.exe -avd my-phone -no-snapshot-load &
adb wait-for-device
adb shell 'while [[ -z $(getprop sys.boot_completed) ]]; do sleep 1; done;'

# Run a flow
maestro test .maestro/navigation/tab-nav.yaml

# Run a suite
maestro test .maestro/suites/regression.yaml
```

### Headless (CI)

```bash
# Android: boot emulator headless
$ANDROID_HOME/emulator/emulator.exe -avd my-phone -no-window -no-audio -no-snapshot-load &
# Then run the same flows
maestro test .maestro/suites/regression.yaml
```

**GitHub Actions CI** (uses `reactivecircus/android-emulator-runner` to boot the emulator):

```yaml
# .github/workflows/maestro-e2e.yml
jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          script: |
            # Install Maestro + app, then run flows
            curl -Ls "https://get.maestro.mobile.dev" | bash
            adb install -r android/app/build/outputs/apk/debug/app-debug.apk
            $HOME/.maestro/bin/maestro test .maestro/suites/smoke.yaml
```

> **iOS CI:** Maestro supports iOS simulator in CI but requires a macOS runner with Xcode. Use `xcrun simctl boot <udid>` to boot the simulator instead of the Android emulator runner.

## Writing durable flows (same discipline as e2e-verify Route B)

*("Ration by journey risk" means: test only the user-facing flows that matter — login, checkout, CRUD — not every internal code path; push business logic to unit tests. "Prove red-capable" means: break the behavior, run, confirm the test fails; revert, run, confirm it passes. A test that's never been seen failing is unproven.)*

1. **Ration flows by journey risk.** Each flow is slow and has flake surface. Test through the UI only what is *about* the flow: the user journey, navigation, the wiring. Business-logic variations belong in unit tests.
2. **Selectors a user would recognize.** `accessibilityLabel` > `testID` > text > coordinates. Never raw coordinates — they break on any layout change.
   - ❌ `tapOn: { point: 93%,9% }` — breaks on any layout change, catches nothing a user cares about.
   - ✅ `tapOn: "Add Item"` (backed by `accessibilityLabel`) — breaks only when the user's world breaks.
3. **No blind sleeps.** `waitForAnimationToEnd` and `extendedWaitUntil` auto-wait.
4. **Prove red-capable** (non-negotiable): break the behavior or the assertion target, run, quote the red; revert, quote the green. A flow never seen red is a decoration.
5. **Quote the run summary.** A result you didn't observe is `not run`, never "passed."

## Examples

### Example 1: post-feature smoke → durable suite

**User:** "I just finished the item creation flow — test it on the emulator."

**Claude:** Builds a debug APK (not dev build — "dev builds are fragile under Maestro"), installs it, boots the emulator headed. Writes `.maestro/features/create-item.yaml`: navigate to Items → tap "Add Item" (via `accessibilityLabel`) → fill title + description → save → verify on list. Proves it red by running with a wrong assertion target, quotes both runs. Adds it to the smoke suite.

### Example 2: "test my expo app"

**User:** "Test my expo app."

**Claude:** Checks for `.maestro/` — none exists. Checks the app ID from `app.json`. Scaffolds the directory structure, writes a `tab-nav.yaml` smoke flow first (fastest signal), runs it headed so the user sees the taps. Then writes feature flows for the core journeys identified from the navigation structure.

## Anti-patterns

- ❌ Testing a dev build for reliable runs — Metro drops on cold launch, `back` exits the app. Use a debug APK.
- ❌ Raw coordinate taps (`point: 93%,9%`) — weld the test to today's layout. Use `accessibilityLabel`.
- ❌ `assertVisible` with a `timeout` — use `extendedWaitUntil`.
- ❌ Writing a flow for every case a unit test could cover — ration by journey, push logic to Jest.
- ❌ Shipping a flow never seen red — break it, quote the red, revert, quote the green.
- ❌ Forgetting `adb reverse` — the app can't reach your backend and every flow reports "connection error."
- ✅ Debug APK → `adb reverse` → headed authoring → accessibility-label selectors → prove red-capable → quote the run.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `java not found` | Java not installed | Install JDK 17+ |
| App shows "Connection error" | Emulator can't reach backend | `adb reverse tcp:<port> tcp:<port>` |
| `launchApp` breaks dev build | Cold start drops Metro | Use debug APK, or don't use `clearState: true` |
| `Unknown Property: timeout` | `assertVisible` doesn't accept it | Use `extendedWaitUntil: { visible: ..., timeout: ... }` |
| Flaky tap failures | Element not loaded yet | Add `waitForAnimationToEnd` or `extendedWaitUntil` before tapping |
| `hideKeyboard` exits the app | Dev build treats it as back | Tap a non-interactive element to blur |

## Scripts

This skill ships with reusable scripts in `scripts/`:

| Script | Purpose |
|---|---|
| `scripts/setup.sh` | One-time install: Java 17, Maestro CLI, verifies Android SDK + AVDs |
| `scripts/run_flow.sh` | Boots emulator (if needed), sets up adb reverse, runs a flow |
| `scripts/flow_template.yaml` | Copy-and-edit template for new Maestro flows |

### Quick start with scripts

```bash
# 1. One-time setup
bash skills/maestro-mobile-test/scripts/setup.sh

# 2. Run a flow (boots emulator if needed, sets up adb reverse)
source ~/.maestro/activate.sh
bash skills/maestro-mobile-test/scripts/run_flow.sh my-avd .maestro/navigation/tab-nav.yaml 8888
```

## Links

- Maestro docs: https://maestro.mobile.dev
- Command reference: https://maestro.mobile.dev/cli/test-suites-and-reports
- Flow schema: https://maestro.mobile.dev/reference/api
- Repo: https://github.com/mobile-dev-inc/maestro
