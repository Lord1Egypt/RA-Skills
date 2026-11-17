# iOS BLE (CoreBluetooth central)

Load this for Swift code that uses `CBCentralManager` and `CBPeripheral`. Facts were checked against
developer.apple.com (CoreBluetooth reference, `Info.plist` keys, TN3115).

## Info.plist, capabilities and review

| Key or setting | When | Notes |
|---|---|---|
| `NSBluetoothAlwaysUsageDescription` | Always, iOS 13+ | Required if the app uses Bluetooth. A deployment target below 13 also needs `NSBluetoothPeripheralUsageDescription` |
| `UIBackgroundModes` = `bluetooth-central` | Only if BLE work continues in the background | Added via Background Modes capability. App Review asks why; explain the user-visible feature |
| `UIBackgroundModes` = `bluetooth-peripheral` | Only if the phone advertises or serves GATT in the background | Rare for companion apps |

- Write the usage string around the user benefit ("Connect to your thermostat to change settings"),
  not "This app uses Bluetooth".
- Every new key or background mode is an `Info.plist` change with App Review impact. Call it out in the MR.
- iOS 18+: AccessorySetupKit offers a system picker for accessories with app-provided names and images.
  Consider it for new products; per TN3115, iOS 26 limits some background relaunch cases to apps that
  set up their accessories with AccessorySetupKit.

## Authorization and power state

```swift
switch CBManager.authorization {          // iOS 13.1+, class property
case .notDetermined: break                // creating a CBCentralManager triggers the prompt
case .denied, .restricted: state = .bluetoothDenied
case .allowedAlways: break
@unknown default: break
}
```

- `centralManagerDidUpdateState(_:)` is the gate. Issue no scans or connects until `.poweredOn`.
- On `.poweredOff`, `.resetting` or `.unauthorized` every peripheral is invalid. Move the state machine to
  `Idle` and rebuild from stored identifiers when power returns.

## Threading

- `CBCentralManager(delegate:queue:options:)`: `queue` is where all central and peripheral delegate calls
  arrive. `nil` means the main queue.
- Use one serial `DispatchQueue` for the manager and every peripheral it owns. Confine all BLE state to it.
- Swift 6: the delegate is an `NSObject` subclass. Either keep it a `final class` whose mutable state is only
  touched on the BLE queue (and say so in a comment where you mark it `@unchecked Sendable`), or forward
  events into an `AsyncStream` consumed by an actor. Hop to `@MainActor` only for UI state.

```swift
final class BleCentral: NSObject, @unchecked Sendable {   // all mutable state confined to `queue`
    private let queue = DispatchQueue(label: "com.example.ble")
    private lazy var central = CBCentralManager(
        delegate: self, queue: queue,
        options: [CBCentralManagerOptionRestoreIdentifierKey: "com.example.ble.central"]
    )
    private let continuation: AsyncStream<LinkEvent>.Continuation
    let events: AsyncStream<LinkEvent>

    override init() {
        let (stream, cont) = AsyncStream.makeStream(of: LinkEvent.self)
        events = stream
        continuation = cont
        super.init()
    }
}
```

## Scanning

```swift
central.scanForPeripherals(withServices: [serviceUUID],
                           options: [CBCentralManagerScanOptionAllowDuplicatesKey: false])
```

- Pass service UUIDs. `nil` returns everything in the foreground and does not work in the background.
- In the background, scan options have no effect; duplicates are coalesced.
- Allowing duplicates costs battery; use it only for live RSSI or advertisement payload updates.
- Stop with `stopScan()` once found and on a timer you own.

## Connecting and reconnecting

- `connect(_:options:)` never times out. Keep a strong reference to the `CBPeripheral`; deallocating it
  cancels the connection. Add your own timeout for user-initiated connects and cancel with
  `cancelPeripheralConnection(_:)`.
- A pending `connect` to a known peripheral is the iOS way to reconnect when it comes back in range. It also
  survives suspension and, with restoration, termination by the system.
- Known devices: `retrievePeripherals(withIdentifiers:)` with the stored `UUID`. Devices connected by the
  system or other apps: `retrieveConnectedPeripherals(withServices:)`, then `connect` locally.
- `peripheral.identifier` is assigned by the system the first time this device sees the peer. It is not the
  MAC address and differs between phones. Store it per phone; map it to a device serial read over GATT.
- iOS 17+: `CBConnectPeripheralOptionEnableAutoReconnect` asks the system to reconnect after a drop;
  disconnects then arrive in `centralManager(_:didDisconnectPeripheral:timestamp:isReconnecting:error:)`.

```swift
func reconnectKnown() {
    guard central.state == .poweredOn else { return }
    for p in central.retrievePeripherals(withIdentifiers: store.knownIDs) {
        p.delegate = self
        peripherals[p.identifier] = p          // strong reference
        central.connect(p)
    }
}

func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
    continuation.yield(.connected(peripheral.identifier))
    peripheral.discoverServices([serviceUUID])
}

func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: Error?) {
    continuation.yield(.dropped(peripheral.identifier, error.map(String.init(describing:))))
    central.connect(peripheral)                // pending reconnect, no timeout
}
```

## Discovery, notifications and serialization

- Discover only the services and characteristics you need: `discoverServices([uuid])`,
  `discoverCharacteristics([uuids], for:)`. After a reconnect, discover again unless restoration provided them.
- `setNotifyValue(true, for:)`; confirm in `peripheral(_:didUpdateNotificationStateFor:error:)`.
- CoreBluetooth queues requests internally, but your protocol usually needs request-response pairing.
  Keep an application-level queue: one outstanding command, a timeout, then the next.
- Handle `peripheral(_:didModifyServices:)`: the GATT table changed (for example after DFU). Rediscover.

## Writes and MTU

- `writeValue(_:for:type:)` with `.withResponse` calls `peripheral(_:didWriteValueFor:error:)`;
  `.withoutResponse` gives no result and no error.
- Flow control for `.withoutResponse`: send while `canSendWriteWithoutResponse` is true, resume in
  `peripheralIsReady(toSendWriteWithoutResponse:)`.
- `maximumWriteValueLength(for:)` is the largest single write for that write type, and the two types can
  return different values. Ask for the type you actually use, after connect, and size chunks from it.
- The app cannot request an MTU. iOS negotiates it; read the size after connect, not at launch.

## State restoration and background

- Opt in with `CBCentralManagerOptionRestoreIdentifierKey`. The string must be identical on every launch.
- Scene-based apps get `nil` launch options, so you cannot read restored identifiers from them. Create the
  central with the same identifier early on every launch (for example in the app delegate's launch method).
- `centralManager(_:willRestoreState:)` delivers `CBCentralManagerRestoredStatePeripheralsKey` with
  connected or pending peripherals, including discovered services and notification state when possible.
  Set delegates and strong references there. If keys are missing, rebuild from your own stored state.
- TN3115 relaunch rules (summarised; read the note for your case):
  - Relaunched: removed from memory by the system, crashed, device restarted (after first unlock).
  - Not relaunched: user force quit, Bluetooth power toggled in Settings.
  - iOS 26 and later: for the cases marked with note 5 (force quit, Control Center Bluetooth toggle,
    Airplane Mode), only apps that set up accessories with AccessorySetupKit are relaunched.
  - Relaunch happens only for a pending event: an ongoing scan, a pending connect, or a subscribed
    notification that fires.
- In the background, keep work short. Each wake-up gets limited execution time; do not start long uploads
  from a notification without a background task.

```swift
func centralManager(_ central: CBCentralManager, willRestoreState dict: [String: Any]) {
    let restored = dict[CBCentralManagerRestoredStatePeripheralsKey] as? [CBPeripheral] ?? []
    for p in restored {
        p.delegate = self
        peripherals[p.identifier] = p
    }
    continuation.yield(.restored(restored.map(\.identifier)))
}
```

## Pairing on iOS

- Apps cannot start pairing directly. iOS pairs when the app accesses a characteristic that requires
  encryption or authentication; the system shows the dialog.
- Outside AccessorySetupKit (which supports removing an accessory's pairing), only the user can remove a
  pairing in Settings. If the device lost its keys, the app must guide the user to "Forget This Device"
  and pair again. Detect this from repeated encryption errors after connect.

## Logging

- Do not log `peripheral.identifier` together with account data in production. Redact payloads; log length,
  opcode and status. Use `os.Logger` with `privacy: .private` for anything identifying.

```swift
logger.debug("rx opcode=\(opcode) len=\(data.count) dev=\(peripheral.identifier, privacy: .private)")
```
