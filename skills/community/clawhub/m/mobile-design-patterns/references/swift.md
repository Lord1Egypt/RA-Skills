# Swift pattern implementations

Load this when implementing or reviewing patterns in Swift for iOS. Assumes Swift 6 language mode,
async/await, `@Observable` (iOS 17+) and SwiftUI. Older targets can swap `@Observable` for
`ObservableObject` without changing the patterns.

## Repository

```swift
// Protocol because view models are tested with a fake and the feature module must not see URLSession.
protocol DeviceRepository: Sendable {
    func devices() async throws -> [Device]
    func refresh() async throws
}

actor CachedDeviceRepository: DeviceRepository {
    private let api: DeviceAPI
    private let store: DeviceStore           // disk cache, the source of truth
    private var refreshTask: Task<Void, Error>?

    init(api: DeviceAPI, store: DeviceStore) {
        self.api = api
        self.store = store
    }

    func devices() async throws -> [Device] {
        try await store.load().map(Device.init(record:))
    }

    // Concurrent callers share one in-flight refresh (actor reentrancy safe).
    func refresh() async throws {
        if let refreshTask { return try await refreshTask.value }
        let task = Task { try await store.save(api.devices().map(DeviceRecord.init(dto:))) }
        refreshTask = task
        defer { refreshTask = nil }
        try await task.value
    }
}
```

- DTOs (`Decodable`) and persistence records stay in the data layer; the protocol returns domain types.

## Factory

```swift
enum ExportFormat { case pdf, csv }

protocol Exporter { func export(_ report: Report) throws -> Data }

struct ExporterFactory {
    let fonts: FontProvider

    func make(_ format: ExportFormat) -> any Exporter {
        switch format {
        case .pdf: PDFExporter(fonts: fonts)
        case .csv: CSVExporter(separator: ";")
        }
    }
}

// Failable static factory for validated values.
struct SerialNumber: Hashable, Sendable {
    let value: String
    private init(_ value: String) { self.value = value }

    static func parse(_ raw: String) -> SerialNumber? {
        let s = raw.trimmingCharacters(in: .whitespaces).uppercased()
        guard s.count == 12, s.allSatisfy({ $0.isASCII && ($0.isLetter || $0.isNumber) }) else { return nil }
        return SerialNumber(s)
    }
}
```

## Builder replaced by memberwise initializers

```swift
struct ScanOptions: Sendable {
    var timeout: Duration = .seconds(10)
    var serviceFilter: CBUUID? = nil
    var allowDuplicates = false
}

let options = ScanOptions(serviceFilter: telemetryService) // defaulted members may be omitted
var longer = options
longer.timeout = .seconds(30)                               // value semantics replace copy()
```

- Memberwise initializers are internal. Public types need an explicit `public init` with default arguments.
- Result builders (`@resultBuilder`) are for nested declarative structures, not option bags.

## Singleton replaced by injection

```swift
@main
struct GatewayApp: App {
    // Composition root: the only place that knows concrete types.
    @State private var devices = DevicesModel(repository: CachedDeviceRepository(api: .live, store: .disk))

    var body: some Scene {
        WindowGroup { DevicesView().environment(devices) }
    }
}

struct DevicesView: View {
    @Environment(DevicesModel.self) private var model
    var body: some View { List(model.items) { DeviceRow(device: $0) } }
}
```

- `static let shared` is acceptable for truly stateless or system-owned services, and only referenced at the
  composition root, never inside view models.
- Tests construct `DevicesModel(repository: FakeDeviceRepository())` directly.

## Strategy

```swift
struct BackoffPolicy: Sendable {
    let delay: @Sendable (_ attempt: Int) -> Duration

    static let fixed = BackoffPolicy { _ in .seconds(1) }
    static let exponential = BackoffPolicy { attempt in .milliseconds(500 * (1 << min(attempt, 6))) }
}

final class Uploader {
    private let backoff: BackoffPolicy
    init(backoff: BackoffPolicy = .exponential) { self.backoff = backoff }
}
```

A protocol is the better fit when the strategy has several methods or its own state.

## Observer

```swift
// UI state: Observation framework.
@MainActor @Observable
final class DevicesModel {
    private(set) var items: [Device] = []
    private let repository: any DeviceRepository
    init(repository: any DeviceRepository) { self.repository = repository }
    func load() async { items = (try? await repository.devices()) ?? [] } // real code maps errors to state
}

// Event stream with a single consumer: AsyncStream.
final class TelemetryFeed: Sendable {
    let readings: AsyncStream<Reading>
    private let continuation: AsyncStream<Reading>.Continuation

    init() {
        (readings, continuation) = AsyncStream.makeStream(of: Reading.self, bufferingPolicy: .bufferingNewest(64))
    }

    func publish(_ reading: Reading) { continuation.yield(reading) }
    deinit { continuation.finish() }
}

// Several subscribers that each need the latest value: Combine.
final class BatteryMonitor {
    private let subject = CurrentValueSubject<Int?, Never>(nil)
    var level: AnyPublisher<Int?, Never> { subject.eraseToAnyPublisher() }
    func update(_ level: Int) { subject.send(level) }
}
```

- One `AsyncStream` is meant for one consumer; two loops iterating it split the elements between them.
- Combine subscribers keep their `AnyCancellable` and capture `self` weakly in `sink`.
- Consume streams in `.task { for await r in feed.readings { ... } }` so the loop cancels with the view.

## Adapter

```swift
// Completion-handler API -> async. Resume exactly once on every path.
extension LegacyPrinter {
    func printReceipt(_ job: PrintJob) async throws -> PrintReceipt {
        try await withCheckedThrowingContinuation { continuation in
            submit(job) { result in continuation.resume(with: result) }
        }
    }
}

// Delegate API -> ordered AsyncStream. CBCentralManager keeps its delegate weakly; the owner retains this object.
final class CentralEvents: NSObject, CBCentralManagerDelegate {
    let events: AsyncStream<CentralEvent>
    private let continuation: AsyncStream<CentralEvent>.Continuation
    private var central: CBCentralManager?

    override init() {
        (events, continuation) = AsyncStream.makeStream(of: CentralEvent.self)
        super.init()
        central = CBCentralManager(delegate: self, queue: DispatchQueue(label: "ble.central"))
    }

    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        continuation.yield(.powered(central.state == .poweredOn))
    }

    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        continuation.yield(.connected(peripheral.identifier))
    }

    func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: (any Error)?) {
        continuation.yield(.disconnected(peripheral.identifier))
    }
}
```

- Add cancellation with `withTaskCancellationHandler` when the wrapped API can be cancelled.
- Yielding into one stream keeps callback order. Spawning a `Task { await ... }` per callback does not.

## Decorator

```swift
struct TimedDeviceAPI: DeviceAPI {
    let inner: any DeviceAPI
    let metrics: Metrics

    func firmwareInfo(id: Device.ID) async throws -> FirmwareInfo {
        let start = ContinuousClock.now
        defer { metrics.record("firmwareInfo", ContinuousClock.now - start) }
        return try await inner.firmwareInfo(id: id)
    }

    // Swift has no automatic forwarding: every other requirement is forwarded by hand.
    func devices() async throws -> [DeviceDTO] { try await inner.devices() }
}
```

Large protocols make decorators expensive in Swift. Keep the decorated protocol small.

## Facade

```swift
actor DeviceSession {
    private let central: CentralClient
    private let machine: ConnectionStateMachine

    init(central: CentralClient, machine: ConnectionStateMachine) {
        self.central = central
        self.machine = machine
    }

    func open(_ id: UUID) async throws(SessionError) -> PeripheralLink {
        await machine.send(.connect)
        do {
            let link = try await central.connect(id)
            try await link.discoverServices([telemetryService])
            try await link.enableNotifications(for: telemetryCharacteristic)
            await machine.send(.linkUp(mtu: link.maximumWriteLength))
            return link
        } catch {
            throw SessionError.setupFailed(String(describing: error))
        }
    }
}
```

`maximumWriteLength` here stands for a wrapper over `CBPeripheral.maximumWriteValueLength(for:)`.

## State machine (connection)

```swift
enum ConnectionError: Error, Equatable, Sendable { case timeout, rejected, poweredOff }

enum ConnectionState: Equatable, Sendable {
    case disconnected
    case connecting(attempt: Int)
    case connected(mtu: Int)
    case disconnecting
    case failed(ConnectionError)
}

enum ConnectionEvent: Sendable {
    case connect, disconnect, closed
    case linkUp(mtu: Int)
    case linkLost(ConnectionError)
}

extension ConnectionState {
    func next(on event: ConnectionEvent, maxAttempts: Int = 3) -> ConnectionState {
        switch (self, event) {
        case (.disconnected, .connect), (.failed, .connect):
            .connecting(attempt: 1)
        case (.connecting, .linkUp(let mtu)):
            .connected(mtu: mtu)
        case (.connecting(let attempt), .linkLost(let error)):
            attempt < maxAttempts ? .connecting(attempt: attempt + 1) : .failed(error)
        case (.connected, .linkLost):
            .connecting(attempt: 1)
        case (.connecting, .disconnect), (.connected, .disconnect):
            .disconnecting
        case (.disconnecting, .closed), (.disconnecting, .linkLost):
            .disconnected
        default:
            self // illegal transition: ignored, logged by the caller
        }
    }
}

actor ConnectionStateMachine {
    private(set) var state: ConnectionState = .disconnected
    let states: AsyncStream<ConnectionState>
    private let continuation: AsyncStream<ConnectionState>.Continuation

    init() {
        (states, continuation) = AsyncStream.makeStream(of: ConnectionState.self, bufferingPolicy: .bufferingNewest(1))
    }

    func send(_ event: ConnectionEvent) {
        let next = state.next(on: event)
        guard next != state else { return }
        state = next
        continuation.yield(next)
    }
}
```

- Feed delegate events in order: one task iterates `CentralEvents.events` and calls `await machine.send(...)`.
- `next(on:)` is pure; test it without Bluetooth:

```swift
@Test func linkLostWhileConnectedReconnects() {
    #expect(ConnectionState.connected(mtu: 185).next(on: .linkLost(.timeout)) == .connecting(attempt: 1))
}
```

## Command

```swift
final class CommandQueue<Command: Sendable>: Sendable {
    private let continuation: AsyncStream<Command>.Continuation
    private let worker: Task<Void, Never>

    init(execute: @escaping @Sendable (Command) async -> Void) {
        let (stream, continuation) = AsyncStream.makeStream(of: Command.self)
        self.continuation = continuation
        worker = Task { for await command in stream { await execute(command) } }
    }

    func enqueue(_ command: Command) { continuation.yield(command) }

    deinit {
        continuation.finish()
        worker.cancel()
    }
}
```

- CoreBluetooth queues individual read and write requests itself. On iOS a command queue is about
  app-level sequences (write config, wait for acknowledgement, then read status) and undo, not about the stack.
- Writes without response use flow control: check `canSendWriteWithoutResponse` and resume on
  `peripheralIsReady(toSendWriteWithoutResponse:)`.
- Undo in document-style apps: `UndoManager` from the environment rather than a custom stack.

## Coordinator / Router

```swift
enum OnboardingRoute: Hashable { case permissions, pairing, done }

@MainActor @Observable
final class OnboardingCoordinator {
    var path: [OnboardingRoute] = []
    func start() { path.append(.permissions) }
    func permissionsGranted() { path.append(.pairing) }
    func paired() { path.append(.done) }
    func finish() { path.removeAll() }
}

struct OnboardingFlow: View {
    @State private var coordinator = OnboardingCoordinator()

    var body: some View {
        NavigationStack(path: $coordinator.path) {
            WelcomeView(onContinue: { coordinator.start() })
                .navigationDestination(for: OnboardingRoute.self) { route in
                    switch route {
                    case .permissions: PermissionsView(onGranted: { coordinator.permissionsGranted() })
                    case .pairing: PairingView(onPaired: { coordinator.paired() })
                    case .done: DoneView(onFinish: { coordinator.finish() })
                    }
                }
        }
    }
}
```

- Child views receive closures, not the coordinator, so they stay previewable and reusable.
- UIKit apps use the classic coordinator owning a `UINavigationController`; keep child coordinators in an
  array and remove them when their flow finishes, or they leak.

## Result and typed throws

```swift
enum PairingError: Error { case timeout, rejected(reason: String), bluetoothOff }

func pair(id: Device.ID) async throws(PairingError) -> Device { ... }

func onPairTapped() async {
    do throws(PairingError) {
        state = .paired(try await pair(id: selected))
    } catch {
        switch error { // error is PairingError, exhaustive switch
        case .timeout: state = .retryable
        case .rejected(let reason): state = .failed(reason)
        case .bluetoothOff: state = .needsBluetooth
        }
    }
}
```

- Typed throws only where the error set is closed and callers switch over it; otherwise `throws` (any Error).
- `Result<Success, Failure>` when an outcome must be stored or passed around, not for normal control flow.

## Delegation

```swift
protocol ScannerDelegate: AnyObject {
    func scanner(_ scanner: Scanner, didFind device: Device)
}

final class Scanner {
    weak var delegate: ScannerDelegate?
}
```

- Prefer closures or `AsyncStream` for new APIs with one callback; delegates suit many related callbacks.
- `unowned` only when the delegate provably outlives the delegator; otherwise `weak`.
