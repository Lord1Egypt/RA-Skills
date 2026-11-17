---
name: mobile-ble
description: "Designs, implements and reviews Bluetooth Low Energy code in Android, iOS and Flutter apps: Android 12+ permissions, filtered scans, GATT operation queues, MTU, bonding, status 133, CoreBluetooth threading and state restoration, flutter_blue_plus, framing, CRC, safe firmware updates (DFU) and connection state machines. Use when writing or reviewing BLE scan, connect, read, write or notify code, reconnect logic or device protocols."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile BLE

Build and review the app side of a Bluetooth Low Energy link the way a senior connected-device engineer
would: correct permissions per OS version, one GATT operation at a time, no assumptions about threads,
explicit connection states, framed and checked messages, firmware updates that cannot brick the device,
and logs that leak nothing. A good result works on real phones, recovers from drops, and survives
hostile or corrupt input.

## When to use

- Writing or changing scan, connect, discover, read, write, notify or disconnect code.
- Android BLE permissions, foreground services or background work for a connected device.
- CoreBluetooth central code, background mode, state restoration or reconnect logic.
- flutter_blue_plus code, or a Flutter plugin that talks to a peripheral.
- Designing or reviewing a packet protocol on top of GATT: framing, chunking, sequence numbers, CRC.
- Firmware update (DFU) flows driven by the app.
- "Status 133", "GATT error", "writes get lost", "notifications stop", "works on Pixel but not on X".

Not for: a full MASVS audit (use `mobile-security`), CRA or EN 18031 mapping (use `mobile-eu-compliance`),
general Kotlin or Swift style (use `mobile-kotlin`, `mobile-swift`).

## Workflow

1. **Read the device contract first.** Find the firmware protocol document: services, characteristics,
   opcodes, packet layout, CRC variant, timing, DFU procedure. The firmware document is authoritative.
   If a packet format, opcode or timing is not written down, ask; never guess it.
2. **Read the project setup.**
   - Android: `minSdk`, `targetSdk`, manifest permissions, foreground service declarations.
   - iOS: deployment target, `Info.plist` usage strings, `UIBackgroundModes`, restoration identifier.
   - Flutter: `pubspec.yaml` BLE and permission plugins and their versions.
3. **Load the platform reference** for the code being touched:
   [Android](references/android.md), [iOS](references/ios.md), [Flutter](references/flutter.md).
4. **Model the link** as a sealed connection state machine before writing callbacks (rule 9).
5. **Put every GATT operation behind one queue** with a timeout per operation (rule 3).
6. **Design or check the wire protocol**: framing above MTU, sequence numbers, CRC, bounds checks.
   Use [Protocol and DFU](references/protocol-and-dfu.md).
7. **Plan background behaviour** per platform: foreground service or Companion Device Manager on
   Android, `bluetooth-central` and state restoration on iOS.
8. **Test** with fakes behind an interface, then on real hardware. See [Testing](references/testing.md).
9. **Report** permissions, `Info.plist` keys, entitlements, foreground service types and background
   modes the change adds. These affect store review and signing and must be called out explicitly.

## Platform facts (verified)

| Area | Fact |
|---|---|
| Android 12+ (API 31) | `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`, `BLUETOOTH_ADVERTISE` are runtime permissions; legacy `BLUETOOTH` and `BLUETOOTH_ADMIN` get `maxSdkVersion="30"` |
| `neverForLocation` | Lets API 31+ scan without location; some beacons are filtered from results |
| Android 11 and lower | Scanning needs `ACCESS_FINE_LOCATION` |
| Android 13 (API 33) | `writeCharacteristic(c, value, writeType)` returns an `Int` status; byte-array callbacks; old forms deprecated |
| Android 14 (API 34) | Stack requests ATT MTU 517 on the first `requestMtu` and ignores later requests |
| Android 14 (API 34) | Every foreground service declares a type; `connectedDevice` needs `FOREGROUND_SERVICE_CONNECTED_DEVICE` |
| Android 16 (API 36) | Bond loss: system keeps the bond and shows a dialog; `ACTION_KEY_MISSING` and `ACTION_ENCRYPTION_CHANGE` intents (OEM behaviour varies) |
| Android 17 (API 37) | `connectGatt(BluetoothGattConnectionSettings, Executor, BluetoothGattCallback)` added; the `Context` overloads are deprecated; autonomous re-pairing after bond loss |
| iOS 13+ | `NSBluetoothAlwaysUsageDescription` is required to use Bluetooth |
| iOS | `connect(_:options:)` never times out; `queue: nil` delivers delegate calls on the main queue |
| iOS | Background scanning needs `bluetooth-central` and explicit service UUIDs |
| iOS 26 | Per TN3115, some relaunch cases are limited to apps that set up accessories with AccessorySetupKit |
| flutter_blue_plus 2.x | `connect` takes a required `license:` argument; commercial use needs a paid license |

Re-check these against the official pages before quoting them in a design document. Versions move.

## Rules

### 1. Declare permissions per API level and check them before every call

```xml
<!-- BAD: location requested on Android 12+ for no reason, no legacy caps -->
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />

<!-- GOOD: app never derives location from scans -->
<uses-permission android:name="android.permission.BLUETOOTH" android:maxSdkVersion="30" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" android:maxSdkVersion="30" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" android:maxSdkVersion="30" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN"
    android:usesPermissionFlags="neverForLocation" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-feature android:name="android.hardware.bluetooth_le" android:required="true" />
```

```swift
// BAD: CBCentralManager created at launch, before the user knows why; no usage string
let central = CBCentralManager(delegate: self, queue: nil)

// GOOD: Info.plist has NSBluetoothAlwaysUsageDescription; create the manager when the feature starts
if CBManager.authorization == .denied { state = .bluetoothDenied; return }
central = CBCentralManager(delegate: self, queue: bleQueue)
```

- If the app uses scan results for location, drop `neverForLocation` and keep `ACCESS_FINE_LOCATION`.
- Request runtime permissions from a screen that explains the feature. Handle "denied" with a path to settings.

### 2. Scan with filters, a time limit and the cheapest mode that works

```kotlin
// BAD: unfiltered, low latency, never stopped
scanner.startScan(callback)

// GOOD
val filters = listOf(ScanFilter.Builder().setServiceUuid(ParcelUuid(SERVICE_UUID)).build())
val settings = ScanSettings.Builder().setScanMode(ScanSettings.SCAN_MODE_BALANCED).build()
scanner.startScan(filters, settings, callback)
scanTimeout = scope.launch { delay(10.seconds); scanner.stopScan(callback) }
```

- Stop as soon as the device is found. Never scan in a loop.
- Unfiltered scans stop on screen off. Apps not in the foreground get `SCAN_MODE_LOW_POWER`.
- Starting scans too often gets throttled: `SCAN_FAILED_SCANNING_TOO_FREQUENTLY`, or silently no
  results on some devices. The exact limit is not documented; do not restart scans in a tight loop.
- iOS: pass service UUIDs to `scanForPeripherals(withServices:options:)`; `nil` does not work in background.

### 3. One GATT operation at a time, each with a timeout

Android and iOS both drop or reject overlapping requests. Android returns `false` or
`ERROR_GATT_WRITE_REQUEST_BUSY`; the callback for the first request may never come.

```kotlin
// BAD: second call fails while the first is in flight
gatt.writeCharacteristic(cmd, bytes, WRITE_TYPE_DEFAULT)
gatt.readCharacteristic(status)

// GOOD: serialized queue, completes on the callback, times out if the callback never comes
suspend fun write(c: BluetoothGattCharacteristic, value: ByteArray) =
    queue.run(timeout = 5.seconds) { gatt.writeCharacteristic(c, value, WRITE_TYPE_DEFAULT) == BluetoothStatusCodes.SUCCESS }
```

- Service discovery, MTU request, enabling notifications (CCCD write), reads and writes all go through the queue.
- A timeout fails the operation and usually the connection: disconnect, close, reconnect.
- Full queue implementation: [Android](references/android.md).

### 4. Never assume the main thread in BLE callbacks

Android GATT callbacks arrive on a binder thread unless you pass a `Handler` or `Executor`.
iOS delegate calls arrive on the queue passed to `CBCentralManager`, or main when `nil`.

```kotlin
// BAD: mutates UI-facing state and a plain list from a binder thread
override fun onCharacteristicChanged(g: BluetoothGatt, c: BluetoothGattCharacteristic, value: ByteArray) {
    buffer.add(value); uiState.items += parse(value)
}

// GOOD: hand off to one serial context; StateFlow exposes the result
override fun onCharacteristicChanged(g: BluetoothGatt, c: BluetoothGattCharacteristic, value: ByteArray) {
    inbound.trySend(value.copyOf())   // Channel consumed on a limitedParallelism(1) dispatcher
}
```

```swift
// BAD: BLE work on the main queue blocks UI during bursts of notifications
central = CBCentralManager(delegate: self, queue: nil)

// GOOD: dedicated serial queue; hop to the main actor only for UI state
central = CBCentralManager(delegate: self, queue: DispatchQueue(label: "ble.central"))
Task { @MainActor in model.apply(event) }
```

### 5. Use the value-carrying Android 13+ APIs; never read `characteristic.value` on 33+

```kotlin
// BAD: deprecated in API 33, not memory safe, value can change under you
characteristic.value = bytes
gatt.writeCharacteristic(characteristic)

// GOOD
val status = if (Build.VERSION.SDK_INT >= 33) {
    gatt.writeCharacteristic(characteristic, bytes, BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT)
} else {
    legacyWrite(gatt, characteristic, bytes)   // @Suppress("DEPRECATION") helper: sets value, calls old API
}
```

- Override both `onCharacteristicChanged` overloads when `minSdk < 33`; use the `value` parameter on 33+.
- API 37: prefer `connectGatt(BluetoothGattConnectionSettings, Executor, callback)` behind a version check.

### 6. Always close the GATT, and treat status 133 as "close, back off, retry"

Status 133 (0x85) is a generic stack error with no public constant. It shows up on connect failures,
stale caches and too many open clients.

```kotlin
// BAD: reconnect on the same object, never closed, leaks a client interface per attempt
if (status != BluetoothGatt.GATT_SUCCESS) gatt.connect()

// GOOD
override fun onConnectionStateChange(gatt: BluetoothGatt, status: Int, newState: Int) {
    if (status != BluetoothGatt.GATT_SUCCESS || newState == BluetoothProfile.STATE_DISCONNECTED) {
        gatt.close()
        events.trySend(LinkEvent.Dropped(status))   // state machine schedules retry with backoff
        return
    }
    if (newState == BluetoothProfile.STATE_CONNECTED) events.trySend(LinkEvent.Connected)
}
```

- Backoff: for example 1 s, 2 s, 4 s, capped, with a maximum attempt count, then surface an error.
- `disconnect()` is asynchronous. Call `close()` once you no longer need the object, including after timeouts.

### 7. Size every write from the negotiated MTU

```kotlin
// BAD: assumes 512-byte packets because MTU was "requested"
gatt.requestMtu(517); send(chunk512)

// GOOD: payload per ATT write is MTU - 3, taken from onMtuChanged
override fun onMtuChanged(gatt: BluetoothGatt, mtu: Int, status: Int) {
    maxPayload = if (status == BluetoothGatt.GATT_SUCCESS) mtu - 3 else 20
}
```

```swift
// GOOD: iOS negotiates MTU itself; ask per write type
let maxPayload = peripheral.maximumWriteValueLength(for: .withoutResponse)
```

- Default ATT MTU is 23 bytes (20 bytes of payload). A single attribute value is at most 512 bytes.
- Request a high connection priority only for bulk transfer, then go back to `CONNECTION_PRIORITY_BALANCED`.

### 8. Respect flow control on writes without response

```swift
// BAD: loop floods the stack; packets are dropped with no error
for chunk in chunks { peripheral.writeValue(chunk, for: tx, type: .withoutResponse) }

// GOOD
func pump() {
    while peripheral.canSendWriteWithoutResponse, let chunk = outbox.popFirst() {
        peripheral.writeValue(chunk, for: tx, type: .withoutResponse)
    }
}
func peripheralIsReady(toSendWriteWithoutResponse peripheral: CBPeripheral) { pump() }
```

- Android: keep no-response writes in the queue too; treat `ERROR_GATT_WRITE_REQUEST_BUSY` as back-pressure.
- Use writes with response, or an application-level ACK, for anything that must not be lost.

### 9. Model the connection as a sealed state machine

```kotlin
// BAD: booleans that drift apart
var isConnected = false; var isConnecting = false; var servicesReady = false

// GOOD
sealed interface Link {
    data object Idle : Link
    data class Connecting(val attempt: Int) : Link
    data object Discovering : Link
    data class Ready(val maxPayload: Int) : Link
    data class Backoff(val attempt: Int, val reason: Int) : Link
    data class Failed(val reason: FailReason) : Link
}
```

```swift
enum Link: Sendable { case idle, connecting(attempt: Int), discovering, ready(maxPayload: Int), backoff(attempt: Int), failed(FailReason) }
```

- One function computes the next state from (state, event). Illegal transitions are logged and ignored.
- Commands are only accepted in `Ready`. UI observes the state; it never drives callbacks directly.

### 10. Frame, number and check every message; never trust device input

```kotlin
// BAD: length byte from the device used as-is
val len = data[1].toInt()
val payload = data.copyOfRange(2, 2 + len)

// GOOD: bounds-check every length, verify CRC, reject and count bad frames
fun parse(frame: ByteArray): Frame? {
    if (frame.size < HEADER + CRC_SIZE) return null
    val len = frame[2].toInt() and 0xFF
    if (len > MAX_PAYLOAD || HEADER + len + CRC_SIZE != frame.size) return null
    if (crc16(frame, 0, HEADER + len) != frame.readU16(HEADER + len)) return null
    return Frame(seq = frame[1].toInt() and 0xFF, payload = frame.copyOfRange(HEADER, HEADER + len))
}
```

- CRC16 or CRC32 detects corruption, not tampering. Authenticity needs a signature or MAC (rule 13).
- Sequence numbers detect loss, duplicates and reordering across chunked transfers.
- Layout, CRC variant and limits come from the firmware document. See [Protocol and DFU](references/protocol-and-dfu.md).

### 11. Reconnect the platform way

```kotlin
// BAD: background scan loop to find a known device again
while (true) { scanner.startScan(cb); delay(5_000); scanner.stopScan(cb) }

// GOOD: autoConnect for a known device; the stack waits for it to come back in range (API 37: settings overload)
gatt = device.connectGatt(context, /* autoConnect = */ true, callback, BluetoothDevice.TRANSPORT_LE)
```

```swift
// GOOD: retrieve by stored identifier and connect; the request does not time out
if let p = central.retrievePeripherals(withIdentifiers: [savedID]).first {
    p.delegate = self
    central.connect(p)
}
```

- Use direct connect (`autoConnect = false`) for the first, user-initiated connection; it is faster.
- iOS identifiers are per-app UUIDs, not MAC addresses. Store them, do not try to derive them.

### 12. Keep long-lived links alive with the supported mechanism

```kotlin
// BAD: start a service from a BLE callback while in the background (throws on Android 12+)
override fun onCharacteristicChanged(...) { context.startForegroundService(intent) }

// GOOD: start the connectedDevice service while the app is visible, or use Companion Device Manager
startForeground(id, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_CONNECTED_DEVICE)
```

```xml
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_CONNECTED_DEVICE" />
<service android:name=".DeviceLinkService" android:exported="false"
    android:foregroundServiceType="connectedDevice" />
```

- For devices that stay paired for months, prefer Companion Device Manager presence over a permanent service.
- iOS: `UIBackgroundModes` with `bluetooth-central` plus `CBCentralManagerOptionRestoreIdentifierKey`.
  A user force quit stops relaunch. Details: [Android](references/android.md), [iOS](references/ios.md).

### 13. Firmware updates must never brick the device

```kotlin
// BAD: blind stream, no checks, phone at 5 %, image trusted because the CRC matched
dfu.send(image)

// GOOD: preconditions, signed image verified by the bootloader, resumable, verified after reboot
require(battery.phone >= 30 && deviceInfo.battery >= 50) { "battery too low" }   // thresholds from firmware team
require(sha256(image).contentEquals(release.sha256))     // download integrity
dfu.send(image, resumeFrom = device.confirmedOffset())   // device verifies the vendor signature
check(device.reportedVersion() == release.version)
```

- Dual-bank or swap with rollback on the device; the old image stays bootable until the new one is confirmed.
- Never downgrade unless the firmware explicitly allows it (anti-rollback).

### 14. Pair securely and keep keys and personal data out of logs

```kotlin
// BAD
Log.d("BLE", "connected ${device.address} key=${sessionKey.toHex()} payload=${value.toHex()}")

// GOOD: redacted identifiers, no keys, payload sizes not contents
log.debug { "connected dev=${device.address.redact()} mtu=$mtu len=${value.size}" }
```

- Require LE Secure Connections with Numeric Comparison, Passkey Entry or OOB. "Just Works" has no
  protection against man-in-the-middle during pairing.
- Encrypt and authenticate application data end to end when the link alone is not trusted.
- MAC addresses, serial numbers and device names can be personal data (GDPR). Do not ship them in analytics.

## Anti-patterns

- Calling `gatt.connect()` again after an error instead of `close()` and a fresh `connectGatt`.
- `Thread.sleep` or fixed delays between GATT calls instead of a queue that waits for callbacks.
- Assuming the MTU you requested is the MTU you got.
- Catching every failure as "device not found" so status codes never reach logs or the state machine.
- Scanning without filters, without a timeout, or restarting scans every few seconds.
- Reading characteristic values from shared objects on Android 13+ instead of the callback parameter.
- Treating CRC as security, or a device's length field as trusted.
- A DFU flow that can start on low battery, cannot resume, or accepts unsigned images.
- Storing the Android MAC address as the cross-platform device ID; iOS never exposes it.
- Building a protocol from sniffed traffic and guesses instead of the firmware document.
- Declaring `ACCESS_BACKGROUND_LOCATION`, `BLUETOOTH_PRIVILEGED` or extra permissions "just in case".

## Checklist

- [ ] Firmware protocol document located; every opcode, length and CRC variant traced to it
- [ ] Manifest: API 31+ permissions, legacy ones capped at `maxSdkVersion="30"`, location only if needed
- [ ] Runtime permission and Bluetooth-off states handled with a user-visible path
- [ ] `Info.plist`: `NSBluetoothAlwaysUsageDescription`; `bluetooth-central` only if background is required
- [ ] Scans use filters, a time limit and stop on match
- [ ] Every GATT operation goes through one queue with a timeout
- [ ] No callback touches UI or unsynchronised state; one serial context owns the link
- [ ] Android 13+ value-carrying APIs used, with fallbacks below API 33
- [ ] `close()` on every disconnect, failure and timeout; status 133 retried with capped backoff
- [ ] Payload size taken from the negotiated MTU or `maximumWriteValueLength(for:)`
- [ ] Write-without-response respects flow control
- [ ] Connection modelled as sealed states; commands only in `Ready`
- [ ] Every inbound length bounds-checked; CRC verified; sequence numbers checked
- [ ] Reconnect uses `autoConnect`, CDM or `retrievePeripherals(withIdentifiers:)`, not scan loops
- [ ] Foreground service type `connectedDevice` declared with its permission, or CDM used
- [ ] DFU: battery check, signed image verified on device, resume, rollback, version check after reboot
- [ ] Pairing uses LE Secure Connections with an authenticated method where the device supports it
- [ ] Logs and analytics contain no keys, tokens, raw payloads or unredacted device identifiers
- [ ] BLE layer behind an interface with fakes; tested on real phones from more than one vendor

## Output format

For a review or design check:

~~~markdown
## BLE review: <app / module / branch>

Scope: <files>. Platforms: <Android | iOS | Flutter>. Firmware doc: <name and version, or "missing">.

### Findings

1. [Blocker] Android -- ble/GattClient.kt:88 -- reconnect calls gatt.connect() after status 133, gatt never closed
   Why: leaks a GATT client per attempt; after a few failures every connect returns 133 until Bluetooth restarts
   Fix:
   ```kotlin
   gatt.close(); stateMachine.on(LinkEvent.Dropped(status))
   ```

2. [Major] iOS -- BLE/Central.swift:41 -- writes without response in a loop, no canSendWriteWithoutResponse check
   Why: chunks are dropped silently during DFU
   Fix: pump from peripheralIsReady(toSendWriteWithoutResponse:)

### Protocol
| Check | Status | Evidence |
|---|---|---|
| Length fields bounds-checked | Missing | `FrameParser.kt:22` trusts `data[1]` |
| CRC verified on every frame | Met | `Crc16.kt`, CRC-16/CCITT-FALSE per firmware doc 2.3 |

### Manifest, Info.plist and background changes
- <permission / key / service type added or required, with store-review impact>

### Questions
- <anything the firmware document does not define>

### Verdict
Request changes -- 1 Blocker, 1 Major.
~~~

Severity: Blocker (bricked device, data corruption, security or privacy breach, crash), Major (lost data,
stuck connection, battery drain, wrong behaviour on common phones), Minor, Nit. For a new protocol, the
agent fills the protocol checklist from [Protocol and DFU](references/protocol-and-dfu.md) instead.

## Related skills

- `mobile-security` -- MASVS checks for pairing, key storage, logging and exported components
- `mobile-eu-compliance` -- CRA and EN 18031 duties for companion apps, secure update evidence
- `mobile-kotlin`, `mobile-swift`, `mobile-flutter` -- language rules for the BLE layer code
- `mobile-testing` -- fakes, virtual time and device-lab strategy
- `mobile-performance` -- battery cost of scans, connection priority and background work
- `mobile-code-review` -- general review dimensions alongside the BLE-specific findings
