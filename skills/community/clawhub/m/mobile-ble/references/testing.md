# Testing BLE code

Load this when adding tests for a BLE layer or planning device testing. Most BLE bugs are timing,
ordering and error-path bugs; they can be reproduced with fakes and virtual time long before a phone
touches real hardware.

## What simulators and emulators can do

| Environment | BLE support | Use it for |
|---|---|---|
| iOS Simulator | No Core Bluetooth radio; the central never reaches `.poweredOn` | UI and logic with a fake `BleClient` only |
| Android Emulator, API 31+ images | Simulated Bluetooth (classic and BLE profiles) through the emulator's virtual radio | Permission flows, emulator-to-emulator experiments; not a substitute for your peripheral |
| JVM / Swift / Dart unit tests | None | State machine, queue, parser, retry and backoff logic with fakes |
| Real phones | Full | Everything that touches the stack: MTU, bonding, 133, background, DFU |

Re-check the emulator documentation for your emulator version; Bluetooth support has changed across
releases. Treat any emulator result as "logic works", never as "works on phones".

## Put the platform behind an interface

The app talks to a small interface. The platform implementation is thin; the logic above it (state
machine, queue, protocol, DFU) is tested against a fake.

Kotlin:

```kotlin
interface GattPort {
    val events: Flow<GattEvent>                       // Connected, Dropped(status), Notified(bytes), MtuChanged(mtu)
    suspend fun connect(address: String)
    suspend fun write(char: UUID, value: ByteArray, withResponse: Boolean): GattResult
    suspend fun close()
}

class FakeGattPort : GattPort {
    private val _events = MutableSharedFlow<GattEvent>(extraBufferCapacity = 64)
    override val events: Flow<GattEvent> = _events
    val writes = mutableListOf<ByteArray>()
    var connectStatuses = ArrayDeque(listOf(133, 133, 0))   // fail twice, then succeed
    var closeCount = 0

    override suspend fun connect(address: String) {
        val status = connectStatuses.removeFirst()
        _events.emit(if (status == 0) GattEvent.Connected else GattEvent.Dropped(status))
    }
    override suspend fun write(char: UUID, value: ByteArray, withResponse: Boolean): GattResult {
        writes += value.copyOf(); return GattResult.Ok()
    }
    override suspend fun close() { closeCount++ }
    suspend fun notify(bytes: ByteArray) = _events.emit(GattEvent.Notified(bytes))
}
```

```kotlin
@Test fun retriesStatus133WithBackoffAndClosesEachTime() = runTest {
    val port = FakeGattPort()
    val link = DeviceLink(port, backoff = listOf(1.seconds, 2.seconds), dispatcher = StandardTestDispatcher(testScheduler))

    link.connect("AA:BB:CC:DD:EE:FF")
    advanceTimeBy(3.seconds); runCurrent()

    assertEquals(Link.Ready::class, link.state.value::class)
    assertEquals(2, port.closeCount)
}
```

Swift:

```swift
protocol PeripheralPort: Sendable {
    var events: AsyncStream<PeripheralEvent> { get }
    func connect(_ id: UUID) async
    func write(_ data: Data, withResponse: Bool) async throws
    func maximumWriteLength(withResponse: Bool) -> Int
}

final class FakePeripheralPort: PeripheralPort, @unchecked Sendable {
    let (events, continuation) = AsyncStream.makeStream(of: PeripheralEvent.self)
    var written: [Data] = []
    var maxLength = 20
    func connect(_ id: UUID) async { continuation.yield(.connected) }
    func write(_ data: Data, withResponse: Bool) async throws { written.append(data) }
    func maximumWriteLength(withResponse: Bool) -> Int { maxLength }
}

@Test func chunksRespectMaximumWriteLength() async throws {
    let port = FakePeripheralPort()
    port.maxLength = 20
    let sender = FrameSender(port: port)
    try await sender.send(Data(repeating: 0xAB, count: 100))
    #expect(port.written.allSatisfy { $0.count <= 20 })
}
```

Dart:

```dart
class FakeBleClient implements BleClient {
  final _state = StreamController<LinkState>.broadcast();
  final _notifications = StreamController<Uint8List>.broadcast();
  final sent = <Uint8List>[];

  @override Stream<LinkState> get state => _state.stream;
  @override Stream<Uint8List> get notifications => _notifications.stream;
  @override Future<void> connect(String id) async => _state.add(LinkState.ready);
  @override Future<Uint8List> request(Uint8List c, {Duration timeout = const Duration(seconds: 3)}) async {
    sent.add(c);
    return Uint8List.fromList([0x00]);
  }
  @override Future<void> disconnect() async => _state.add(LinkState.idle);

  void dropLink() => _state.add(LinkState.dropped);
}

test('command times out when the device never answers', () {
  fakeAsync((async) {
    final client = SilentBleClient();               // request() never completes
    Object? error;
    DeviceRepository(client).readVersion().catchError((Object e) { error = e; return ''; });
    async.elapse(const Duration(seconds: 4));
    expect(error, isA<TimeoutException>());
  });
});
```

## What to test with fakes

- State machine: every (state, event) pair, including illegal ones (notification while `Connecting`).
- Queue: one operation at a time; timeout fails the operation; a drop fails the pending operation.
- Status 133 and other connect failures: close is called each time; backoff timing; give-up after N attempts.
- Chunking: every chunk fits `MTU - 3` or `maximumWriteValueLength(for:)`; reassembly limits; out-of-order chunks.
- Parser: truncated frames, maximum lengths, length fields larger than the buffer, wrong CRC, unknown opcode.
- CRC: the standard check value for `"123456789"` (see [Protocol and DFU](protocol-and-dfu.md)).
- DFU: resume from offset after a drop, refusal on low battery, version check after reboot.
- Logging: assert redaction (no raw MAC, no key material) in the formatted log lines.

## Device testing

Manual tools:
- nRF Connect for Mobile (Android and iOS): scan, inspect advertisement data and RSSI, connect, read and
  write characteristics, toggle notifications and indications, view a log, and run a Nordic DFU.
  Use it to confirm the peripheral behaves as documented before debugging the app.
- Android HCI snoop log (Developer options) to see packets on the phone; open it with a protocol analyser.
- A hardware sniffer for link-layer problems the phone cannot show.

Device matrix (minimum):
- Android: a Pixel on the latest release, a Samsung, one more OEM, and the oldest supported API level.
  Include one device below API 31 if `minSdk` allows it (location permission path).
- iOS: oldest supported iOS and the latest release.
- Peripheral: current firmware and the oldest firmware still in the field.

Scenarios to run by hand on every release that touches BLE:
- [ ] First pairing, permission denied, Bluetooth off, then on
- [ ] Walk out of range and back; peripheral power cycle; phone Bluetooth toggle
- [ ] App backgrounded for 10 minutes with an active link; screen off; Doze on Android
- [ ] App killed by the system (iOS restoration) and force quit (expected: no relaunch)
- [ ] Bond removed on the phone, then on the peripheral (Android 16 and 17 bond-loss dialogs)
- [ ] DFU with a drop in the middle, with low battery, and with an incompatible image
- [ ] Two devices connected at once, if the product supports it
