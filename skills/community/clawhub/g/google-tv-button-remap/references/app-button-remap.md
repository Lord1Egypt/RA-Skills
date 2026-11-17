# Remap a Google TV Streamer remote button (no root) — verified procedure

Scope: consume a physical remote app-button key event and launch a different app, without root.
Verified 2026-10-15 on a Google TV Streamer (Android 14, SDK 34): Netflix `BUTTON_4` (191) → Spotify.
Result: a single physical press opens the target; the stock app never launches.

## 1. The chain you are replacing (know it before you cut in)

- Remote → HID usage (`0x0C0078` = Netflix) → keycode `BUTTON_4` (191) via
  `/system/usr/keylayout/Vendor_18d1_Product_9451.kl`.
- A privileged service resolves the button to a package:
  `com.google.android.chromecast.chromecastservice` (uid 1000) logs `GlobalKeyReceiver … launchNetflix`,
  then the launcher `com.google.android.apps.tv.launcherx:coreservices` → `GlobalAppLaunchManager`
  runs `am start -a com.netflix.action.NETFLIX_KEY_START -n com.netflix.ninja/.MainActivity`.
- The trigger broadcast `android.intent.action.GLOBAL_BUTTON` is guarded by
  `com.google.android.permission.GLOBAL_BUTTON` (`system|signature`) — a normal app cannot send or receive it.

## 2. The interception (the part that works)

An `AccessibilityService` requesting the key-event filter receives hardware key events before the
launcher's consumer and can consume them.

`res/xml/accessibility_service_config.xml`:

```xml
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeWindowStateChanged"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagRequestFilterKeyEvents"
    android:canRequestFilterKeyEvents="true"
    android:description="@string/service_desc" />
```

Manifest (the service must declare the accessibility binding permission):

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

Service core — consume the target key, launch the replacement, pass everything else through:

```java
@Override
public boolean onKeyEvent(KeyEvent e) {
    if (e.getKeyCode() == 191 /* KEYCODE_BUTTON_4 */) {
        if (e.getAction() == KeyEvent.ACTION_UP) launch(targetPackage);
        return true;   // consume DOWN + UP — the launcher never sees it
    }
    return false;      // YouTube button, DPAD, etc. untouched
}
```

Because the event is consumed at the filter stage, the stock app does not launch at all (no flash).

## 3. The two traps (each one produced a false negative)

1. **`adb shell input keyevent 191` never reaches `onKeyEvent`.** Injected events trigger the launcher
   but bypass the accessibility key filter. Only a **physical** press is delivered. Any automated test
   will wrongly conclude the button cannot be intercepted.
2. **Install non-incrementally.** An incremental (fastdeploy) `adb install` left the service code
   unloaded and silent. Use `adb install --no-incremental`.

Do not mistake the `A11yInputFilter … Enabled features of Display [0] = [KeyboardInterceptor]` line for a
system component: it is **your own** service's filter and appears only while yours is enabled.

## 4. Build (no Gradle) and deploy

Build by hand: `aapt2 compile` → `aapt2 link` → `javac` → `d8` → `zipalign` → `apksigner`
(see `build-apk-without-gradle.md`), then:

```bash
adb install --no-incremental app-release.apk
adb shell settings put secure enabled_accessibility_services <pkg>/<pkg>.RemapService
adb shell settings put secure accessibility_enabled 1
```

Undo: `adb shell settings put secure enabled_accessibility_services ''`.

## 5. Verify (the success criteria)

```bash
adb shell input keyevent KEYCODE_HOME
# operator presses the PHYSICAL remapped button once, then:
adb shell getgs event -lt   # (optional) confirm the keycode
adb shell dumpsys activity activities | grep -m1 topResumedActivity
adb logcat -d | grep -E 'Launching com\.|GlobalKeyReceiver|NETFLIX_KEY_START'
```

Pass = `topResumedActivity` is the target app **and** there is **no** `Launching com.<stock>` line.
