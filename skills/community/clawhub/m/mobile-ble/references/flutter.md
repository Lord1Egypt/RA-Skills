# Flutter BLE (flutter_blue_plus)

Load this for Dart BLE code. API details were checked against the flutter_blue_plus 2.3.x pages and API
reference on pub.dev, and permission_handler 13.x. Check `pubspec.lock` for the version the project uses;
names changed between 1.x and 2.x.

## Licensing and supply chain (read first)

- flutter_blue_plus 2.x uses its own FlutterBluePlus License, not BSD. Nonprofit, personal and educational
  use is free; for-profit use needs a paid commercial license.
- `connect` has a required `license:` argument: `License.nonprofit` or `License.commercial`
  (`License.free` is deprecated, renamed to `nonprofit`).
- The changelog (2.3.5) adds a license ping during the build that includes the package name and app name.
- The Android package moved from `com.lib.flutter_blue_plus` to `com.jmx.flutter_blue_plus` in 2.3.9.
  Update ProGuard or R8 keep rules that name the old package.
- Flag these to the owner: licence cost, a build-time network call to a third party, and an SBOM entry with
  a non-OSI licence. Do not pick the `license:` value on the owner's behalf.

## Setup

Android manifest (same rules as native, see [Android](android.md)):

```xml
<uses-feature android:name="android.hardware.bluetooth_le" android:required="false" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN" android:usesPermissionFlags="neverForLocation" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.BLUETOOTH" android:maxSdkVersion="30" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" android:maxSdkVersion="30" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" android:maxSdkVersion="30" />
```

If the app derives location from scans, drop `neverForLocation`, keep `ACCESS_FINE_LOCATION` uncapped and
pass `androidUsesFineLocation: true` to `startScan`.

iOS `Info.plist`: `NSBluetoothAlwaysUsageDescription`; `UIBackgroundModes` with `bluetooth-central` only if
needed, plus `FlutterBluePlus.setOptions(restoreState: true)` before any other call.

## Runtime permissions with permission_handler

```dart
Future<bool> ensureBlePermissions() async {
  if (Platform.isAndroid) {
    final sdk = (await DeviceInfoPlugin().androidInfo).version.sdkInt;
    final wanted = sdk >= 31
        ? [Permission.bluetoothScan, Permission.bluetoothConnect]
        : [Permission.locationWhenInUse];
    final result = await wanted.request();
    return result.values.every((s) => s.isGranted);
  }
  // iOS: the system prompt appears on first CoreBluetooth use; permission_handler reports the status.
  return (await Permission.bluetooth.request()).isGranted;
}
```

- On Android, `permanentlyDenied` is only reported by `request()`, not by `status`. Offer `openAppSettings()`.
- iOS with CocoaPods: permission_handler needs the `PERMISSION_BLUETOOTH=1` macro in the Podfile
  `post_install` block; with Swift Package Manager the `Info.plist` key is enough. Check the plugin README
  for the exact macro name for your version.
- `DeviceInfoPlugin` is from device_info_plus; any way of reading the SDK level works.

## Adapter state and scanning

```dart
if (await FlutterBluePlus.isSupported == false) return BleUnavailable();

await FlutterBluePlus.adapterState
    .where((s) => s == BluetoothAdapterState.on)
    .first
    .timeout(const Duration(seconds: 5));      // iOS starts in `unknown`

final sub = FlutterBluePlus.onScanResults.listen(
  (results) { if (results.isNotEmpty) _onFound(results.last); },
  onError: (Object e) => _onScanError(e),
);
FlutterBluePlus.cancelWhenScanComplete(sub);

await FlutterBluePlus.startScan(
  withServices: [Guid(serviceUuid)],
  timeout: const Duration(seconds: 10),
  androidScanMode: AndroidScanMode.balanced,  // default is lowLatency
);
await FlutterBluePlus.isScanning.where((s) => s == false).first;
```

- `onScanResults` clears between scans; `scanResults` keeps previous results.
- Filters combine with OR (`withServices`, `withNames`, `withRemoteIds`, `withMsd`, `withServiceData`).
- `FlutterBluePlus.turnOn()` is Android only.

## Connecting

```dart
final device = result.device;

final stateSub = device.connectionState.listen((s) {
  if (s == BluetoothConnectionState.disconnected) {
    _link.add(LinkEvent.dropped(device.disconnectReason?.code));
  }
});
device.cancelWhenDisconnected(stateSub, delayed: true, next: true);

await device.connect(
  license: License.commercial,                  // chosen by the owner, see Licensing
  timeout: const Duration(seconds: 15),
  mtu: 512,                                     // Android only; ignored on iOS
);
final services = await device.discoverServices();   // after every connection
```

- `connect(autoConnect: true, mtu: null)` reconnects whenever the device is found and returns immediately;
  `autoConnect` cannot be combined with `mtu`, so call `requestMtu` after connecting. Listen to
  `connectionState` to know when it actually connects. Calling `disconnect()` turns auto connect off.
- `remoteId` is the MAC address on Android and a system UUID on iOS. Never use it as a cross-platform key.
- `FlutterBluePlus.events.onConnectionStateChanged` observes every device; useful for a single link manager.

## MTU, writes and notifications

```dart
// Android: request explicitly if not done in connect(); iOS negotiates on its own
if (Platform.isAndroid) await device.requestMtu(512);
final maxPayload = device.mtuNow - 3;

for (final chunk in frames(bytes, maxPayload)) {
  await rx.write(chunk, withoutResponse: false, timeout: 5);
}

await tx.setNotifyValue(true);
final notifySub = tx.onValueReceived.listen(_onBytes);
device.cancelWhenDisconnected(notifySub);
```

- `requestMtu(desiredMtu, {predelay, timeout})` is Android only. `device.mtu` is a stream; `mtuNow` the value.
- `write(value, {withoutResponse = false, allowLongWrite = false, timeout = 15})`. `withoutResponse: true`
  always returns success immediately; delivery is not guaranteed. `allowLongWrite` allows up to 512 bytes
  with response but can leave partial data if interrupted; prefer your own framing.
- `onValueReceived` fires for reads and notifications only. `lastValueStream` also fires on writes and
  re-emits the last value on listen, which makes it easy to process a stale packet twice.
- `createBond`, `removeBond`, `bondState`, `requestConnectionPriority` and `clearGattCache` are Android only.
- `FlutterBluePlus.setOperationQueueMode` (2.3.0) controls how operations are queued across devices. The
  plugin serialises calls per device, but your protocol still needs one outstanding command at a time.

## Structure

- Wrap flutter_blue_plus in a `BleClient` interface in the data layer. Widgets and view models never import
  the plugin. This is also the seam for fakes; see [Testing](testing.md).
- Cancel every `StreamSubscription` (use `cancelWhenDisconnected` and `cancelWhenScanComplete`), and dispose
  the link manager with its owner.
- Platform channels deliver results on the main isolate. Heavy parsing of large transfers (DFU images,
  logs) goes to `Isolate.run`.

```dart
abstract interface class BleClient {
  Stream<LinkState> get state;
  Future<void> connect(String deviceId);
  Future<Uint8List> request(Uint8List command, {Duration timeout});
  Stream<Uint8List> get notifications;
  Future<void> disconnect();
}
```

## Platform differences to design for

| Topic | Android | iOS |
|---|---|---|
| Device id | MAC address, stable | System UUID per phone, can change |
| MTU | Requested by the app | Negotiated by the system |
| Bonding API | `createBond`, `removeBond` | None; triggered by encrypted characteristics |
| Turn adapter on | `turnOn()` | Not possible; ask the user |
| Background | Foreground service or CDM (native code) | `bluetooth-central` + `restoreState` |
| Location permission | API 30 and lower, or if not `neverForLocation` | Never needed for BLE |

Background work on Android (foreground service type `connectedDevice`, Companion Device Manager) is native
code; add it in the Android host project and follow [Android](android.md).
