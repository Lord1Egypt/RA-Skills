# Deep dive: eliminating the Google TV Streamer app-button handler and replacing it with a filtered key consumer

*Engineering write-up. Target: Google TV Streamer (Android TV, no root). Verified 2026-10-15.*
*All identifiers below are from the device under test; substitute your own where noted.*

---

## 0. Abstract

The physical Netflix/YouTube buttons on the Google TV reference remote are not handled by the
app layer and are not remappable through any documented interface. This document records the
full trace of the handler, three interception strategies that provably fail, and the one that
works: an `AccessibilityService` requesting `FLAG_REQUEST_FILTER_KEY_EVENTS`, which consumes
`KEYCODE_BUTTON_4` at the input-filter stage before the platform's own consumer runs.

It also records a reproduction hazard that produced several false negatives: **injected key
events (`InputManager.injectInputEvent` / `adb shell input keyevent`) do not reach an
accessibility `onKeyEvent`, while hardware key events do.** Any automated test that uses
injection will conclude, incorrectly, that interception is impossible.

---

## 1. Environment / inventory

| Item | Value |
|---|---|
| Device | Google TV Streamer, Android TV |
| Access | `adb connect <tv-host>:5555` (wireless debugging) |
| Remote | Google reference BT/IR remote, USB-HID `Vendor_18d1_Product_9451` |
| Launcher | `com.google.android.apps.tv.launcherx` (privileged, `UPDATED_SYSTEM_APP`) |
| Root | none (software); hardware glitch attack not attempted |
| Host toolchain | JDK 17.0.20.1, Android build-tools 34.0.0, platform android-34, `apksigner`, `zipalign`, `d8`, `aapt2` (all standalone, no Gradle) |

Key processes observed:

```
chromecastservice    pid 1251   uid 1000        # logs GlobalKeyReceiver: launchNetflix
launcherx:coreservices pid 3341 uid 10069       # logs GlobalButtonLaunch / GlobalAppLaunchManager
tv.remote.service    pid 1457                   # present, NOT the button consumer (verified)
```

---

## 2. Signal path

### 2.1 HID → keycode

The remote's key layout is `/system/usr/keylayout/Vendor_18d1_Product_9451.kl`:

```
key 116   POWER         WAKE
key 217   ASSIST
key 103   DPAD_UP
key 108   DPAD_DOWN
key 105   DPAD_LEFT
key 106   DPAD_RIGHT
key 353   DPAD_CENTER   WAKE
key 158   BACK          WAKE
key 172   HOME          WAKE
key 113   VOLUME_MUTE
key 114   VOLUME_DOWN
key 115   VOLUME_UP
key usage 0x000c0186    MACRO_1      WAKE
key usage 0x000c0077    BUTTON_3     WAKE #YouTube
key usage 0x000c0078    BUTTON_4     WAKE #Netflix
```

So: Netflix = HID usage `0x0C0078` → `KEYCODE_BUTTON_4` (`191`); YouTube = `0x0C0077` →
`KEYCODE_BUTTON_3` (`190`); ★ = `0x0C0186` → `MACRO_1`.

Raw event capture (kernel level) confirms the remote emits the button as an `EV_KEY` event on
its input node before any Android-level handling.

### 2.2 The privileged consumer

The key event does not go to an app. A privileged service resolves it to a package and drives
the launch. Tracing a single press:

```
W/GlobalKeyReceiver( 1251):  launchNetflix: fromNonInteractive: false
W/GlobalButtonLaunch( 3341): Received key press for package name com.netflix.ninja, key code -1.
W/GlobalAppLaunchManager(3341): Launching com.netflix.ninja in main user.
I/ActivityTaskManager(  684): START u0 {act=com.netflix.action.NETFLIX_KEY_START
      flg=0x10020000 pkg=com.netflix.ninja cmp=com.netflix.ninja/.MainActivity (has extras)}
      with LAUNCH_SINGLE_TASK from uid 10069 (BAL_ALLOW_ALLOWLISTED_COMPONENT) result code=2
```

Notes:
- `key code -1` at the launcher stage — by then the keycode has already been resolved to a
  package; the launch is package-driven, not keycode-driven.
- `fromNonInteractive: false` — there is an explicit interactive-state gate.
- The mapping is **data-driven**: no `Netflix`/`YouTube`→package table exists in the
  decompiled launcher Java; the target is resolved at runtime. That is how Google can retarget
  these buttons server-side without a firmware update.

### 2.3 The broadcast contract

The launcher's consumer is an exported manifest receiver running in a private process:

```xml
<receiver
    android:name="com.google.android.apps.tv.launcherx.remotecontrol.GlobalKeyListener_Receiver"
    android:exported="true"
    android:process=":coreservices"
    android:singleUser="true">
    <intent-filter>
        <action android:name="android.intent.action.GLOBAL_BUTTON"/>
        <action android:name="com.google.android.apps.tv.launcherx.CONFIGURE_GLOBAL_BUTTON"/>
    </intent-filter>
</receiver>
```

The receiver's handler (`GlobalKeyListener` in the launcher's obfuscated `llh.java`) begins:

```java
if (!"android.intent.action.GLOBAL_BUTTON".equals(intent.getAction())) return wwu.a;
final KeyEvent keyEvent = (KeyEvent) intent.getParcelableExtra("android.intent.extra.KEY_EVENT");
if (keyEvent == null) return wwu.a;
if (keyEvent.getAction() == 1 && this.u.isInteractive()) { ... }
```

The launcher also declares the broadcast's guard permission:

```xml
<permission
    android:name="com.google.android.permission.GLOBAL_BUTTON"
    android:protectionLevel="system|signature"/>
```

A separate component monitors which remote is attached — `TvRemoteMonitor` (decompiled
`ies.java`) implements `InputManager.InputDeviceListener` and filters devices by
vendor/product, external keyboard type, and source caps. It observes device topology; it is
not the key consumer.

---

## 3. Interception strategies — negative results

### 3.1 Disabling the receiver: denied

```
$ adb shell pm disable-user --user 0 \
    com.google.android.apps.tv.launcherx/.remotecontrol.GlobalKeyListener_Receiver

Exception occurred while executing 'disable-user':
java.lang.SecurityException: Shell cannot change component state for
  ComponentInfo{com.google.android.apps.tv.launcherx/…GlobalKeyListener_Receiver} to 3
    at com.android.server.pm.PackageManagerService.setEnabledSettings(PackageManagerService.java:3958)
    …
```

`pm enable` fails identically (target state `1`). A non-root shell may not change enabled state
for a component of a **privileged system app**; the barrier is a permission check, not the
signing key. (`PackageManagerShellCommand.runSetEnabledSetting` → `PackageManagerService`.)

### 3.2 Spoofing the broadcast: impossible

`GLOBAL_BUTTON` is guarded by `com.google.android.permission.GLOBAL_BUTTON`
(`system|signature`). An ordinary app cannot hold that permission, so it can neither send the
broadcast nor (in practice) be a recipient. An instrumented manifest receiver for
`android.intent.action.GLOBAL_BUTTON` never fired.

### 3.3 RRO / overlay: unavailable

The launcher is a signed Play APK under `/data/app/...`, `UPDATED_SYSTEM_APP`, and exposes no
`<overlayable>` (overlayable count = 0). There is no static-resource override path.

---

## 4. The interception point that works

Android routes hardware key events through the accessibility input filter, which forwards them
to any `AccessibilityService` that requests it via `FLAG_REQUEST_FILTER_KEY_EVENTS`
(`AccessibilityServiceInfo` capability bit `0x8`). A service that returns `true` from
`onKeyEvent()` **consumes** the event before window dispatch, so the platform consumer never
sees it.

Observed device evidence:

- `dumpsys accessibility`: `A11yInputFilter Info : Enabled features of Display [0] = [KeyboardInterceptor]`
  — this feature exists *only* while the service is enabled (empty otherwise), confirming the
  service holds the filter.
- `Bound services: {Service[... capabilities=8, eventTypes=TYPE_WINDOW_STATE_CHANGED ...]}`
  — `capabilities=8` = `CAPABILITY_CAN_REQUEST_FILTER_KEY_EVENTS`.
- Only **one** accessibility service may hold the key-event filter at a time.

### 4.1 The reproduction hazard

With the service bound and enabled:

- `adb shell input keyevent 191` → the launcher still launches Netflix; **`onKeyEvent` is never
  called** (verified: zero breadcrumb lines for keycodes 23, 19, and 191).
- A **physical** press of the Netflix button → `onKeyEvent code=191 action=0` then `action=1`
  immediately, and the consume fires.

Conclusion: injected events and hardware events diverge at the accessibility filter. Do not use
`input keyevent` to evaluate an accessibility key filter.

---

## 5. Implementation

### 5.1 Service config (`res/xml/accessibility_service_config.xml`)

```xml
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeWindowStateChanged"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagRequestFilterKeyEvents"
    android:canRequestFilterKeyEvents="true"
    android:notificationTimeout="100"
    android:description="@string/service_desc" />
```

### 5.2 Service (`RemapService.java`)

```java
package com.sam.streamer.remap;

import android.accessibilityservice.AccessibilityService;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.view.KeyEvent;
import android.view.accessibility.AccessibilityEvent;

public class RemapService extends AccessibilityService {
    public static final String PREFS = "remap";
    public static final String KEY_ENABLED = "enabled";
    public static final String KEY_TARGET = "target";

    private static final int BTN_NETFLIX = 191;             // KEYCODE_BUTTON_4
    private static final String DEFAULT_TARGET = "com.spotify.tv.android";

    private SharedPreferences prefs;

    private SharedPreferences prefs() {
        if (prefs == null) prefs = getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        return prefs;
    }

    @Override protected void onServiceConnected() {
        prefs = getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }

    @Override public boolean onKeyEvent(KeyEvent event) {
        if (!prefs().getBoolean(KEY_ENABLED, true)) return false;   // disabled: stock
        if (event.getKeyCode() == BTN_NETFLIX) {
            if (event.getAction() == KeyEvent.ACTION_UP) launchTarget();
            return true;                                            // consume DOWN + UP
        }
        return false;                                               // pass everything else
    }

    private void launchTarget() {
        String pkg = prefs().getString(KEY_TARGET, DEFAULT_TARGET);
        Intent i = getPackageManager().getLaunchIntentForPackage(pkg);
        if (i == null) return;
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED);
        try { startActivity(i); } catch (Exception ignored) {}
    }

    @Override public void onAccessibilityEvent(AccessibilityEvent event) {}
    @Override public void onInterrupt() {}
}
```

### 5.3 Manifest essentials

```xml
<service
    android:name="com.sam.streamer.remap.RemapService"
    android:exported="true"
    android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE">
    <intent-filter>
        <action android:name="android.accessibilityservice.AccessibilityService" />
    </intent-filter>
    <meta-data android:name="android.accessibilityservice"
               android:resource="@xml/accessibility_service_config" />
</service>
```

### 5.4 Why there is no flash

The consume happens at the filter stage, upstream of `GlobalKeyListener_Receiver`. The
platform's consumer never receives the event, so the stock app is never started — this is a
replacement of behaviour, not a launch-then-switch.

---

## 6. Build (no Gradle)

```
BT=$ANDROID_SDK/build-tools/34.0.0 ; PLAT=$ANDROID_SDK/platforms/android-34/android.jar

$BT/aapt2 compile --dir app/res -o build/res.zip
$BT/aapt2 link -o build/app.unsigned.apk -I "$PLAT" \
      --manifest app/AndroidManifest.xml build/res.zip \
      --java gen --min-sdk-version 30 --target-sdk-version 34
javac -cp "$PLAT" -d build/classes $(find app/src gen -name '*.java')
$BT/d8 --lib "$PLAT" --min-api 30 --output build $(find build/classes -name '*.class')
cp build/app.unsigned.apk build/app.apk ; (cd build && zip -q app.apk classes.dex)
$BT/zipalign -f -p 4 build/app.apk build/app.aligned.apk
$BT/apksigner sign --ks release.keystore --out build/app-release.apk build/app.aligned.apk
```

### 6.1 Deployment / enablement

```
adb install --no-incremental build/app-release.apk
adb shell settings put secure enabled_accessibility_services com.sam.streamer.remap/com.sam.streamer.remap.RemapService
adb shell settings put secure accessibility_enabled 1
```

Install the APK **non-incrementally** (`--no-incremental`): an incremental (fastdeploy)
install left the app's code unloaded and the service silent — another false-negative source.

---

## 7. Verification methodology

```
# before press
adb shell input keyevent KEYCODE_HOME
adb shell dumpsys activity activities | grep -m1 topResumedActivity

# press the physical button, then:
adb shell dumpsys activity activities | grep -m1 topResumedActivity
adb logcat -d | grep -E 'GlobalKeyReceiver|GlobalAppLaunchManager|Launching com\.'
```

Success criteria for a Netflix→Spotify remap:

- `topResumedActivity` = `com.spotify.tv.android/com.spotify.app.androidtv.MainActivity`
- **no** `Launching com.netflix` / `NETFLIX_KEY_START` in the log (proves the consume held)
- a `WindowManager` OPEN transition with the Spotify task `TO_FRONT` and the home task
  `TO_BACK`

Observed on the reference device: all three held for a single physical press.

---

## 8. Caveats and risk notes

- Requires the accessibility grant (user-visible, one toggle to disable).
- Single-filter invariant: a competing accessibility service requesting the filter can displace
  this one.
- Screen-off / non-interactive behaviour is **untested**; the platform consumer has an explicit
  interactive gate, so behaviour there may differ.
- Keycode (`191`), the input device, and the target package are hardcoded; portability is nil as
  written.
- The mapping is server-driven; a platform update can change the button or tighten
  filter-key-events.
- Scope is limited to this button on this remote path — voice, the phone app, and casting are
  unaffected.
- An app that filters key events is the classic malware shape. Keep the code auditable, do not
  log input, and treat the grant as sensitive.

---

## 9. Appendix — raw evidence

- `pm` component-state denial: `SecurityException` from `PackageManagerService.setEnabledSettings`
  (target state `3` for disable, `1` for enable).
- `dumpsys accessibility`: `A11yInputFilter Info : Enabled features of Display [0] = [KeyboardInterceptor]`
  (present only with the service enabled).
- `dumpsys package …launcherx`: `GlobalKeyListener_Receiver` filter present;
  `flags=[SYSTEM HAS_CODE ALLOW_CLEAR_USER_DATA UPDATED_SYSTEM_APP]`,
  `PRIVILEGED PRODUCT`.
- Decompiled launcher sources referenced: `llh.java` (GlobalKeyListener),
  `ien.java` (GlobalAppLaunchManager), `ies.java` (TvRemoteMonitor).
- Key layout: `/system/usr/keylayout/Vendor_18d1_Product_9451.kl`.
