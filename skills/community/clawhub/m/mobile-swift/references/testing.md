# Testing reference

Load this when adding or changing tests. Swift Testing for unit and integration tests; XCTest for UI
tests and performance tests. Both frameworks can live in the same test target.

## Swift Testing basics

```swift
import Testing
@testable import DeviceFeature

@Suite("Frame decoder")
struct FrameDecoderTests {
    let decoder = FrameDecoder() // fresh instance per test, no shared state

    @Test func decodesBatteryLevel() throws {
        let packet = try decoder.decode(Fixtures.batteryFrame)
        let battery = try #require(packet.battery)
        #expect(battery == 87)
    }

    @Test func rejectsBadChecksum() {
        #expect(throws: FrameError.badChecksum) {
            try decoder.decode(Fixtures.corruptedFrame)
        }
    }
}
```

- `#expect` records a failure and continues. `try #require` stops the test; use it for preconditions and
  to unwrap optionals.
- A `struct` suite gets a new instance per test. Setup goes in `init`, teardown in `deinit` of a
  `final class` suite only when cleanup is required.
- `#expect(throws: SomeError.self)` checks the type; passing an `Equatable` error value checks the case.
- Write the expectation as a plain expression. `#expect(a == b)` already reports both sides on failure.

## Parameterized tests

```swift
@Test(arguments: [
    (Data([0x01, 0x00]), Opcode.ping),
    (Data([0x02, 0x10]), Opcode.status),
])
func decodesOpcode(frame: Data, expected: Opcode) throws {
    #expect(try FrameDecoder().decode(frame).opcode == expected)
}

@Test(arguments: [0, 1, 19, 20])
func rejectsFramesShorterThanHeader(length: Int) {
    #expect(throws: FrameError.self) {
        try FrameDecoder().decode(Data(count: length))
    }
}
```

- Each argument runs as its own test case and can be re-run alone.
- Two argument collections produce every combination. Use `zip(inputs, outputs)` for pairs.
- Prefer parameterized tests over a `for` loop inside one test.

## Async code

```swift
@MainActor
@Test func loadPublishesDevices() async {
    let model = DeviceListModel(repository: FakeDeviceRepository(stubbedDevices: [.sample]))
    await model.load()
    #expect(model.devices == [.sample])
}
```

- Mark tests or suites `@MainActor` when they touch main-actor types.
- `await` the operation under test. Never `sleep` and hope.

Callbacks and events that must fire use `confirmation`:

```swift
@Test func emitsConnectedEvent() async {
    let session = DeviceSession(transport: FakeTransport())
    await confirmation("connected event") { connected in
        session.onEvent = { event in
            if event == .connected { connected() }
        }
        await session.connect()
    }
}
```

- The confirmation must be confirmed before the closure returns. It does not wait for later callbacks.
- `confirmation(expectedCount: 3)` for an exact count; `expectedCount: 0` asserts something never happens.

## Time and dependencies

- Inject `any Clock<Duration>` and use a manual test clock (own implementation or a library) so backoff,
  timeouts and debounce run instantly and deterministically.
- Put protocols at boundaries (network, BLE transport, storage, keychain) and inject fakes. Avoid mocking
  frameworks that rely on runtime tricks.
- SwiftData tests use `ModelConfiguration(isStoredInMemoryOnly: true)`.

```swift
protocol DeviceRepository: Sendable {
    func devices() async throws -> [Device]
}

struct FakeDeviceRepository: DeviceRepository {
    var stubbedDevices: [Device] = []
    var stubbedError: (any Error)?
    func devices() async throws -> [Device] {
        if let stubbedError { throw stubbedError }
        return stubbedDevices
    }
}
```

## Traits and organisation

```swift
extension Tag {
    @Tag static var ble: Self
    @Tag static var parsing: Self
}

@Suite(.tags(.ble), .timeLimit(.minutes(1)))
struct ReconnectTests { /* tests */ }

@Test(.disabled("Flaky on CI simulator, see TICKET-123"))
func scansInBackground() async { /* test body */ }
```

- `.serialized` on a suite whose tests share an external resource. Tests run in parallel by default.
- `.enabled(if:)` for environment-dependent tests.
- `.bug("https://...")` links a known issue.

## XCTest: what still needs it

UI tests:

```swift
final class PairingUITests: XCTestCase {
    func testPairingFlow() throws {
        let app = XCUIApplication()
        app.launchArguments = ["-ui-testing", "-fake-ble"]
        app.launch()

        app.buttons["pair-device"].tap()
        XCTAssertTrue(app.staticTexts["paired-status"].waitForExistence(timeout: 5))
    }
}
```

- Query by `accessibilityIdentifier`, not by visible text that changes with localisation.
- Launch arguments switch the app to fake transports and fixed data. UI tests never depend on real
  devices, servers or BLE hardware.

Performance tests:

```swift
func testDecodePerformance() {
    measure(metrics: [XCTClockMetric(), XCTMemoryMetric()]) {
        _ = try? FrameDecoder().decodeAll(Fixtures.largeCapture)
    }
}
```

- Set a baseline in Xcode and run on a fixed device class; simulator numbers vary.
- Async XCTest waits use `await fulfillment(of: [expectation], timeout: 2)`, not `wait(for:)`.

## Running

- Packages that build on macOS: `swift test`.
- iOS-only packages and the app: `xcodebuild test -scheme <Scheme> -destination '<simulator>'` or a
  test plan.
- Keep fast unit tests in package test targets so they run without launching the simulator app.
