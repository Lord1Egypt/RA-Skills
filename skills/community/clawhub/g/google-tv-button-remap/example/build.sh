#!/bin/bash
# Build a signed APK by hand (no gradle): aapt2 -> javac -> d8 -> zipalign -> apksigner
# Signs with release.keystore when keystore.properties is present, else debug.keystore.
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
BT=/home/mrstone/android-sdk/build-tools/34.0.0
PLAT=/home/mrstone/android-sdk/platforms/android-34/android.jar
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"
cd "$ROOT"
rm -rf build gen && mkdir -p build gen

echo "[1/6] aapt2 compile resources"
"$BT/aapt2" compile --dir app/res -o build/res.zip

echo "[2/6] aapt2 link (manifest + resources)"
"$BT/aapt2" link -o build/app.unsigned.apk -I "$PLAT" \
  --manifest app/AndroidManifest.xml build/res.zip \
  --java gen --min-sdk-version 30 --target-sdk-version 34

echo "[3/6] javac"
javac -cp "$PLAT" -d build/classes $(find app/src gen -name '*.java')

echo "[4/6] d8 -> classes.dex"
"$BT/d8" --lib "$PLAT" --min-api 30 --output build $(find build/classes -name '*.class')

echo "[5/6] package + zipalign"
cp build/app.unsigned.apk build/app.apk
( cd build && zip -q app.apk classes.dex )
"$BT/zipalign" -f -p 4 build/app.apk build/app.aligned.apk

echo "[6/6] apksigner"
if [ -f keystore.properties ] && [ -f release.keystore ]; then
  . ./keystore.properties
  "$BT/apksigner" sign --ks release.keystore \
    --ks-pass "pass:$STORE_PASS" --key-pass "pass:$KEY_PASS" --ks-key-alias "$KEY_ALIAS" \
    --out build/app-release.apk build/app.aligned.apk
  echo "OK (RELEASE) -> $ROOT/build/app-release.apk"
  "$BT/apksigner" verify --print-certs build/app-release.apk | head -2
else
  "$BT/apksigner" sign --ks debug.keystore --ks-pass pass:android --key-pass pass:android \
    --out build/app-debug.apk build/app.aligned.apk
  echo "OK (DEBUG) -> $ROOT/build/app-debug.apk"
fi
