# Building & deploying a minimal APK without Gradle

No Android Studio needed: `aapt2` / `d8` / `apksigner` from SDK build-tools do the whole job. Verified building and installing a signed APK for a Google TV Streamer (SDK 34) over `adb`.

## One-time toolchain

```bash
sudo apt-get install -y openjdk-17-jdk-headless unzip zip curl
# Unpack Android command-line tools to $SDK/cmdline-tools/latest, then:
export SDK=$HOME/android-sdk
yes | "$SDK/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$SDK" --licenses
yes | "$SDK/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$SDK" "build-tools;34.0.0" "platforms;android-34"
```

## Debug keystore (once per project)

```bash
keytool -genkeypair -keystore debug.keystore -alias androiddebugkey \
  -storepass android -keypass android -dname "CN=Android Debug,O=Android,C=US" \
  -keyalg RSA -keysize 2048 -validity 10000
```

## Build script

```bash
BT=$SDK/build-tools/34.0.0
PLAT=$SDK/platforms/android-34/android.jar

aapt2 compile --dir app/res -o build/res.zip
aapt2 link -o build/app.unsigned.apk -I "$PLAT" \
  --manifest app/AndroidManifest.xml build/res.zip \
  --java gen --min-sdk-version 30 --target-sdk-version 34
javac -cp "$PLAT" -d build/classes $(find app/src gen -name '*.java')
d8 --lib "$PLAT" --min-api 30 --output build $(find build/classes -name '*.class')
cp build/app.unsigned.apk build/app.apk
( cd build && zip -q app.apk classes.dex )     # classes.dex must sit at the APK root
zipalign -f -p 4 build/app.apk build/app.aligned.apk
apksigner sign --ks debug.keystore --ks-pass pass:android --key-pass pass:android \
  --out build/app.signed.apk build/app.aligned.apk
```

**Pitfall (cost a full round trip):** pass the compiled resources as a **positional** argument, as above. Passing them via `-R build/res.zip` marks them an **overlay** and `aapt2 link` fails with `error: resource string/app_name does not override an existing resource` → `failed parsing overlays`; `--auto-add-overlay` only masks the mistake.

Also: `aapt2` wants its own `--min-sdk-version`; keep it ≥ that of the platform you linked against, and pass the same number to `d8 --min-api`.

## Accessibility-service glue

- Manifest: service with `android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"`, an `<intent-filter>` for `android.accessibilityservice.AccessibilityService`, and `<meta-data android:name="android.accessibilityservice" android:resource="@xml/...">`.
- Service config XML: `android:canRequestFilterKeyEvents="true"` **and** `android:accessibilityFlags="flagRequestFilterKeyEvents"` — both are required to receive key events.
- Enable it from the shell: `settings put secure enabled_accessibility_services <pkg>/<cls>` then `settings put secure accessibility_enabled 1`; confirm the service appears under `Bound services` in `dumpsys accessibility`.

## Debugging rule

Log **every** key event at the top of `onKeyEvent`. If nothing logs, the service is not being fed events at all — the config is fine and the interception point is wrong (on the Streamer another component holds the box's single key-event filter). Do not write interception logic before you have seen one log line.
