---
name: "google-tv-button-remap"
description: "Remap a Google TV Streamer remote button without root: capture the app-button key with an accessibility filter and launch another app."
---

# Google TV Streamer button remap (no root)

Triggers: "remap the Netflix button", "make the Netflix button open <app>", "change what a Google TV remote button does", "swap the Netflix / YouTube buttons on the streamer", "the <app> button opens the wrong thing". Verified on a **Google TV Streamer** (Android 14, SDK 34), no root.

**Goal:** a physical remote app-button opens a different app, without root, with **no visible flash** of the stock app.

The whole job is: identify the keycode → build a tiny AccessibilityService that **consumes** that key → install and enable it → verify with a **physical** press.

## 1. Identify the button's keycode

`adb shell getevent -lt`, have the operator press the button once; the `MSC_SCAN 000c00XX` line is the HID usage (page `0x0C`). Resolve it from the remote's keylayout (`dumpsys input` names it): the Google reference remote uses `/system/usr/keylayout/Vendor_18d1_Product_9451.kl`:

- YouTube = `0x0C0077` → `BUTTON_3` (190)
- Netflix = `0x0C0078` → `BUTTON_4` (191)
- ★ = `0x0C0186` → `MACRO_1`

**Completion:** you have the integer keycode (e.g. `191`).

## 2. Know what you're replacing

The button is not handled by an app. A privileged service resolves it to a package and launches it. Confirm on your device:

```bash
adb shell input keyevent 191
adb logcat -d | grep -E 'ActivityTaskManager: START|from uid'
```

On the Streamer: `com.google.android.chromecast.chromecastservice` (uid 1000) → launcher `…launcherx:coreservices` → `GlobalAppLaunchManager` → `am start -a com.netflix.action.NETFLIX_KEY_START`. The trigger broadcast `android.intent.action.GLOBAL_BUTTON` is guarded by `com.google.android.permission.GLOBAL_BUTTON` (`system|signature`) — **not spoofable**, and `pm disable` of the launcher receiver throws `SecurityException`. So the only place to cut in is the raw key event.

**Completion:** you can name the uid/package that handles the button.

## 3. Build the key-consuming accessibility service

Request the key-event filter, then consume the target key in `onKeyEvent` and launch your app.

`res/xml/accessibility_service_config.xml`:
```xml
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeWindowStateChanged"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagRequestFilterKeyEvents"
    android:canRequestFilterKeyEvents="true"
    android:description="@string/service_desc" />
```

Manifest — the service must declare the accessibility binding permission:
```xml
<service android:name=".RemapService" android:exported="true"
    android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE">
    <intent-filter>
        <action android:name="android.accessibilityservice.AccessibilityService" />
    </intent-filter>
    <meta-data android:name="android.accessibilityservice"
               android:resource="@xml/accessibility_service_config" />
</service>
```

Service core (consume DOWN+UP; pass every other button through):
```java
@Override
public boolean onKeyEvent(KeyEvent e) {
    if (e.getKeyCode() == 191 /* KEYCODE_BUTTON_4 */) {
        if (e.getAction() == KeyEvent.ACTION_UP) launch(targetPackage);
        return true;   // the launcher never sees it — no flash
    }
    return false;
}
```

**Why no flash:** the consume happens at the input-filter stage, upstream of Google's handler, so the stock app is never started.

**Completion:** the app builds and its service is declared.

## 4. Install non-incrementally and enable

```bash
adb install --no-incremental app-release.apk
adb shell settings put secure enabled_accessibility_services <pkg>/<pkg>.RemapService
adb shell settings put secure accessibility_enabled 1
```

Undo any time: `adb shell settings put secure enabled_accessibility_services ''`.

See `references/build-apk-without-gradle.md` (in this repo) for building/signing the APK with no Gradle/SDK.

**Completion:** `dumpsys accessibility` lists the service under `Bound services`.

## 5. Verify — with a PHYSICAL press

```bash
adb shell input keyevent KEYCODE_HOME
# operator presses the PHYSICAL button once, then:
adb shell dumpsys activity activities | grep -m1 topResumedActivity
adb logcat -d | grep -E 'Launching com\.|GlobalKeyReceiver|NETFLIX_KEY_START'
```

**Pass:** `topResumedActivity` is your target app **and** there is **no** `Launching com.<stock>` line.

## Traps (each one caused a false negative — clear both before concluding anything)

1. **`adb shell input keyevent` never reaches `onKeyEvent`.** Injected events trigger the launcher but bypass the accessibility key filter. **Only a physical press is delivered.** Any scripted test will wrongly conclude the button cannot be intercepted.
2. **Install non-incrementally** (`--no-incremental`). An incremental (fastdeploy) install left the service's code unloaded and silent.

Also: `A11yInputFilter … Enabled features of Display [0] = [KeyboardInterceptor]` is **your own** service's filter (it appears only while yours is enabled) — not a system component holding it. Only one service can hold the key-event filter at a time.

## Notes

- Keycode, target package and (if used) device specifics are per-device — read them, don't assume.
- Google's mapping is data-driven; a platform update can change the button or tighten filter-key-events.
- An app that filters key events is the classic malware shape — keep the code auditable and never log input.
- Deeper context (the full handler chain, decompiled components, negative results): `docs/rcu-app-button-remap.md` and `docs/rcu-app-button-remap-engineering.md`.

## Completion checks

- The service is enabled and bound (`dumpsys accessibility` → `Bound services`)
- A **physical** press opens the target app
- The stock app's launch line is **absent** from logcat
