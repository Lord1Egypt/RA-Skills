# Remapping the Google TV Streamer's Netflix button — without root

*Interoperability research on hardware we own. Verified 2026-10-15.*

## TL;DR

On the Google TV Streamer (Android TV, no root), the physical **Netflix** button can be
remapped by a **150-line accessibility service that holds the key-event filter**. It
consumes the remote's `BUTTON_4` key event *before* Google's own handler ever sees it, so
the stock app never launches — no flash, no root, no third-party remapper app.

The interesting part isn't the trick; it's the chain, and a trap that will fool anyone who
tests this with `adb`.

## The device

- Google TV Streamer, Android TV, **no software root available** (root would require a
  hardware glitch attack — out of scope for a working device).
- ADB shell access only: `adb connect <host>:5555`.
- Works with the stock BLE/IR remote (`Vendor_18d1_Product_9451`).

## What actually happens when you press the button

The signal chain, end to end:

1. **Remote → HID.** The Netflix key emits HID usage `0x0C0078`.
2. **Key layout.** The remote's own layout file maps it:
   `key usage 0x000c0078 BUTTON_4 WAKE #Netflix`
   (YouTube is `0x0C0077 → BUTTON_3`; the ★/magic key is `0x0C0186 → MACRO_1`.)
   So the press arrives in Android as `KEYCODE_BUTTON_4` (keycode `191`).
3. **A privileged consumer picks it up.** On the Streamer the mapping is handled by system
   components, not the app layer:
   - `com.google.android.chromecast.chromecastservice` (system uid 1000) logs
     `GlobalKeyReceiver: launchNetflix`,
   - handing to the launcher's private process
     `com.google.android.apps.tv.launcherx:coreservices`,
   - which calls `GlobalAppLaunchManager: Launching com.netflix.ninja in main user`.
4. **The launch is a broadcast.** The trigger is
   `android.intent.action.GLOBAL_BUTTON`, carrying
   `android.intent.extra.KEY_EVENT`, handled by the launcher's exported receiver
   `…launcherx.remotecontrol.GlobalKeyListener_Receiver`.
5. **Netflix opts in.** The launch action is
   `com.netflix.action.NETFLIX_KEY_START` → `com.netflix.ninja/.MainActivity`. The mapping
   is data-driven, which is how Google can retarget these buttons server-side without a
   firmware update.

## Why the obvious approaches fail

- **Disable the launcher's receiver** (`pm disable-user <component>`): denied with
  `SecurityException: Shell cannot change component state for …GlobalKeyListener_Receiver`.
  A non-root shell may not toggle a component of a **privileged system app**. The wall is
  *permissions*, not signatures.
- **Spoof the broadcast ourselves:** impossible. `GLOBAL_BUTTON` is guarded by
  `com.google.android.permission.GLOBAL_BUTTON`, declared
  `android:protectionLevel="system|signature"`. A normal app can neither send it nor (in
  practice) receive it — our test receiver never fired.
- **Resources/overlays:** the launcher is a signed Play APK in `/data/app`, not overlayable
  (`overlayable` count = 0). No clean RRO path.

## The trap that will fool you (read this twice)

**`adb shell input keyevent 191` is not a valid test of an accessibility key filter.**

Injected events (`input keyevent …`) *do* travel far enough to trigger the launcher's
handler — so an automated test looks like the button path runs — but they **do not reach an
accessibility service's `onKeyEvent`**. Only **real hardware events** do.

We spent several rounds concluding "no app can intercept this" because every scripted test
showed an empty `onKeyEvent`. The moment a human pressed the physical button, the service
logged `onKeyEvent code=191 action=0/1` immediately. If you replicate this work, test with
your finger, not with `input`.

## The working method

An `AccessibilityService` that requests the key-event filter:

**`res/xml/accessibility_service_config.xml`**
```xml
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeWindowStateChanged"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagRequestFilterKeyEvents"
    android:canRequestFilterKeyEvents="true"
    android:description="@string/service_desc" />
```

**The service consumes the target key and launches the replacement:**
```java
@Override
public boolean onKeyEvent(KeyEvent event) {
    if (event.getKeyCode() == 191 /* KEYCODE_BUTTON_4 */) {
        if (event.getAction() == KeyEvent.ACTION_UP) {
            launch("com.spotify.tv.android");
        }
        return true; // consume DOWN + UP — the launcher never sees it
    }
    return false;    // everything else passes through, YouTube included
}
```

Because the event is consumed at the filter stage, Google's `GlobalKeyListener` never fires
and the stock app does **not** launch — there is no "Netflix flashes then Spotify opens"
behaviour. It is a true replacement of the button's behaviour.

## Building it without Gradle

The whole app builds by hand — no Android Studio, no SDK manager:

```
aapt2 compile --dir app/res -o res.zip
aapt2 link -o app.unsigned.apk -I android.jar --manifest app/AndroidManifest.xml res.zip \
      --java gen --min-sdk-version 30 --target-sdk-version 34
javac -cp android.jar -d classes $(find app/src gen -name '*.java')
d8 --lib android.jar --min-api 30 --output . $(find classes -name '*.class')
zip -j app.apk classes.dex        # add dex to the linked APK
zipalign -f -p 4 app.apk app.aligned.apk
apksigner sign --ks release.keystore --out app-release.apk app.aligned.apk
```

## Install and enable

```
adb install app-release.apk
adb shell settings put secure enabled_accessibility_services \
    <pkg>/<pkg>.RemapService
adb shell settings put secure accessibility_enabled 1
```

## Honest caveats

- **Needs the accessibility service enabled** — a normal, user-visible grant; one toggle to
  undo. Not a silent modification.
- **Only one service can hold the key-event filter at a time**; a competing service could
  displace it.
- **Screen-off / non-interactive presses are untested** — behaviour there may fall back to
  stock.
- **Per-device:** keycodes and the target package are hardcoded as written.
- **Google can change it.** The mapping is data-driven and updatable; this is a snapshot,
  not a permanent patch.
- **Only this button, on this remote path.** Voice, the phone app, and casting are
  unaffected.
- Contributing an app that filters key events is the classic malware shape; treat the
  accessibility grant as powerful and keep the code clean and auditable (no input logging).

## Ethics / scope

Performed on hardware we own, to change a button's behaviour on our own TV. No DRM or
protected content is involved. Frame it as interoperability and device-modding research;
redact your own network identifiers before publishing.
