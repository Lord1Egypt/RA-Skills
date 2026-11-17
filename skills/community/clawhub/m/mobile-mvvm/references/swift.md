# MVVM with Swift, SwiftUI and Observation

Load this when building or reviewing a SwiftUI screen and its view model. Assumes Swift 6 language mode,
iOS 17 or newer (`@Observable`), and Swift Testing.

The feature: a device list loaded from a repository, pull to refresh, an "online only" filter restored
per scene, favorites with optimistic update and rollback, and an alert when something fails.

## Domain and data contract

```swift
struct Device: Identifiable, Equatable, Sendable {
    let id: String
    var name: String
    var isOnline: Bool
    var isFavorite: Bool
}

protocol DeviceRepository: Sendable {
    func fetchDevices() async throws -> [Device]
    func setFavorite(_ favorite: Bool, for id: Device.ID) async throws
}
```

- The protocol is the seam for fakes. The real implementation owns `URLSession`, decoding and caching.

## State

```swift
enum UserMessage: Equatable {
    case loadFailed
    case favoriteFailed

    var title: String {
        switch self {
        case .loadFailed: String(localized: "Could not load devices")
        case .favoriteFailed: String(localized: "Could not update favorite")
        }
    }
}

struct DeviceListState: Equatable {
    var devices: [Device] = []
    var onlineOnly = false
    var isLoading = false
    var userMessage: UserMessage?

    var visibleDevices: [Device] {
        onlineOnly ? devices.filter(\.isOnline) : devices
    }
}
```

- `visibleDevices` is derived, so it can never disagree with `devices` and `onlineOnly`.

## View model

```swift
@MainActor
@Observable
final class DeviceListModel {
    private(set) var state = DeviceListState()

    @ObservationIgnored private let repository: any DeviceRepository

    init(repository: any DeviceRepository) {
        self.repository = repository
    }

    func load() async {
        state.isLoading = true
        defer { state.isLoading = false }
        do {
            state.devices = try await repository.fetchDevices()
        } catch is CancellationError {
            return
        } catch {
            state.userMessage = .loadFailed
        }
    }

    func setOnlineOnly(_ value: Bool) {
        state.onlineOnly = value
    }

    func toggleFavorite(_ id: Device.ID) async {
        guard let index = state.devices.firstIndex(where: { $0.id == id }) else { return }
        let newValue = !state.devices[index].isFavorite
        state.devices[index].isFavorite = newValue
        do {
            try await repository.setFavorite(newValue, for: id)
        } catch {
            if let i = state.devices.firstIndex(where: { $0.id == id }) {
                state.devices[i].isFavorite = !newValue
            }
            state.userMessage = .favoriteFailed
        }
    }

    func userMessageShown() {
        state.userMessage = nil
    }
}
```

Notes:
- `@MainActor` makes every state mutation main-thread safe; repository calls suspend off it.
- `@ObservationIgnored` on dependencies, so reading them does not register view dependencies.
- After `await`, the array may have changed. The rollback looks the index up again instead of reusing it.
- `URLSession` reports cancellation as `URLError(.cancelled)`, not `CancellationError`. Map it in the
  repository or check `Task.isCancelled` before reporting an error.

## View

```swift
struct DeviceListView: View {
    @State private var model: DeviceListModel
    @SceneStorage("deviceList.onlineOnly") private var storedOnlineOnly = false

    init(repository: any DeviceRepository) {
        _model = State(initialValue: DeviceListModel(repository: repository))
    }

    var body: some View {
        List(model.state.visibleDevices) { device in
            DeviceRow(device: device) {
                Task { await model.toggleFavorite(device.id) }
            }
        }
        .overlay {
            if model.state.isLoading && model.state.devices.isEmpty {
                ProgressView()
            }
        }
        .refreshable { await model.load() }
        .toolbar {
            Toggle("Online only", isOn: Binding(
                get: { model.state.onlineOnly },
                set: { model.setOnlineOnly($0) }
            ))
        }
        .alert(model.state.userMessage?.title ?? "", isPresented: Binding(
            get: { model.state.userMessage != nil },
            set: { if !$0 { model.userMessageShown() } }
        )) {
            Button("OK", role: .cancel) {}
        }
        .task {
            model.setOnlineOnly(storedOnlineOnly)
            await model.load()
        }
        .onChange(of: model.state.onlineOnly) { _, newValue in
            storedOnlineOnly = newValue
        }
    }
}

struct DeviceRow: View {
    let device: Device
    let onFavoriteTap: () -> Void

    var body: some View {
        HStack {
            Text(device.name)
            Spacer()
            Button(action: onFavoriteTap) {
                Image(systemName: device.isFavorite ? "star.fill" : "star")
            }
            .accessibilityLabel(device.isFavorite ? "Remove favorite" : "Add favorite")
        }
    }
}
```

- `@State` owns the model; the view that creates it is the only owner. Child views get values and closures,
  or the model as a plain property (`@Bindable` when they need bindings).
- `State(initialValue:)` in `init` is evaluated on every parent redraw but only the first instance is kept.
  Keep the model `init` cheap; start work in `.task`.
- `.task` cancels `load()` when the view disappears.
- `@SceneStorage` restores the filter per window after the app is terminated in the background.
  It is not encrypted; store only non-sensitive UI values.
- Dependencies can also come from a custom `EnvironmentValues` entry instead of the initializer.

## Tests (Swift Testing)

```swift
import Testing
@testable import Devices

struct FakeDeviceRepository: DeviceRepository {
    var devices: [Device] = []
    var loadError: (any Error)?
    var favoriteError: (any Error)?

    func fetchDevices() async throws -> [Device] {
        if let loadError { throw loadError }
        return devices
    }

    func setFavorite(_ favorite: Bool, for id: Device.ID) async throws {
        if let favoriteError { throw favoriteError }
    }
}

extension Device {
    static let online = Device(id: "1", name: "Gateway", isOnline: true, isFavorite: false)
    static let offline = Device(id: "2", name: "Sensor", isOnline: false, isFavorite: false)
}

@MainActor
struct DeviceListModelTests {
    @Test func loadPublishesDevices() async {
        let model = DeviceListModel(repository: FakeDeviceRepository(devices: [.online, .offline]))

        await model.load()

        #expect(model.state.devices == [.online, .offline])
        #expect(model.state.isLoading == false)
    }

    @Test func onlineOnlyFiltersDevices() async {
        let model = DeviceListModel(repository: FakeDeviceRepository(devices: [.online, .offline]))
        await model.load()

        model.setOnlineOnly(true)

        #expect(model.state.visibleDevices == [.online])
    }

    @Test func loadFailureShowsMessageUntilAcknowledged() async {
        let model = DeviceListModel(repository: FakeDeviceRepository(loadError: URLError(.notConnectedToInternet)))

        await model.load()
        #expect(model.state.userMessage == .loadFailed)

        model.userMessageShown()
        #expect(model.state.userMessage == nil)
    }

    @Test func favoriteFailureRollsBack() async throws {
        let repository = FakeDeviceRepository(devices: [.online], favoriteError: URLError(.timedOut))
        let model = DeviceListModel(repository: repository)
        await model.load()

        await model.toggleFavorite(Device.online.id)

        let device = try #require(model.state.devices.first)
        #expect(device.isFavorite == false)
        #expect(model.state.userMessage == .favoriteFailed)
    }
}
```

- The suite is `@MainActor` because the model is. Tests `await` the model's async functions directly;
  no sleeps, no expectations with timeouts.
- `Error` is `Sendable`, so a struct fake holding `(any Error)?` is `Sendable` without annotations.
- For time-based logic (debounce, polling), inject `any Clock<Duration>` into the model.
