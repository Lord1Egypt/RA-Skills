# SwiftUI reference

Load this when writing or refactoring SwiftUI views and their models. Assumes iOS 17+ and the Observation
framework. For older targets keep `ObservableObject` and `@StateObject` and say so.

## Property wrapper choice

| Situation | Use |
|---|---|
| View creates and owns an `@Observable` model | `@State private var model = Model()` |
| Model passed in, view only reads it | `let model: Model` (or `var`) |
| Model passed in, view needs `$model.field` bindings | `@Bindable var model: Model` |
| Simple value owned by this view | `@State private var isExpanded = false` |
| Value owned by the parent, edited here | `@Binding var isOn: Bool` |
| App-wide dependency or model | `@Environment(Store.self) private var store` |
| System or custom environment value | `@Environment(\.dismiss) private var dismiss` |
| Legacy `ObservableObject` | `@StateObject` (owner) / `@ObservedObject` (passed in) |

`@State` is always `private`. A value that comes from outside is not `@State`.

## Observable models

```swift
@MainActor @Observable
final class DeviceListModel {
    private(set) var devices: [Device] = []
    private(set) var error: LoadError?
    var filter = ""

    @ObservationIgnored private let repository: DeviceRepository

    init(repository: DeviceRepository) { self.repository = repository }

    func load() async {
        do { devices = try await repository.devices() }
        catch is CancellationError { }
        catch { self.error = LoadError(error) }
    }
}
```

- Views re-render only when a property they actually read changes.
- `@ObservationIgnored` for dependencies and caches the UI never reads.
- Keep `init` cheap. `@State private var model = Model()` evaluates the initializer each time the
  parent re-creates the view value; the extra instances are discarded but their init cost is paid.
  Load data in `.task`, not in `init`.

## Bindings from an observable model

```swift
struct DeviceSettingsView: View {
    @Bindable var settings: DeviceSettings
    var body: some View {
        Form {
            Toggle("Auto reconnect", isOn: $settings.autoReconnect)
            Stepper("Interval: \(settings.interval)s", value: $settings.interval, in: 5...60)
        }
    }
}
```

When the model comes from the environment, create the bindable locally:

```swift
@Environment(DeviceSettings.self) private var settings
var body: some View {
    @Bindable var settings = settings
    Toggle("Auto reconnect", isOn: $settings.autoReconnect)
}
```

## Environment

```swift
// Inject an observable model
ContentView().environment(store)

// Read it
@Environment(Store.self) private var store
```

Custom values use the `@Entry` macro:

```swift
// TelemetryClient is a Sendable protocol, so the default value is safe to share
extension EnvironmentValues {
    @Entry var telemetryClient: any TelemetryClient = NoopTelemetryClient()
}

// Inject and read
RootView().environment(\.telemetryClient, LiveTelemetryClient())
@Environment(\.telemetryClient) private var telemetry
```

- `@Environment(Store.self)` crashes at runtime if no ancestor injected it. Inject at the root and in
  every `#Preview`.
- The environment is for dependencies and app-wide state, not for passing one value two levels down.

## Async work

```swift
// Restarts on every query change, previous run is cancelled
.task(id: query) {
    try? await Task.sleep(for: .milliseconds(300))
    guard !Task.isCancelled else { return }
    await model.search(query)
}
```

- `.task` starts before the view appears and is cancelled when it disappears.
- `.refreshable { await model.reload() }` for pull to refresh.
- Consume `AsyncSequence` values in `.task` with `for await`; the loop ends when the view disappears.
- `.onChange(of: value) { oldValue, newValue in }` for synchronous reactions; avoid chains of `onChange`
  that feed each other.

## Navigation

```swift
enum Route: Hashable {
    case device(Device.ID)
    case firmware(Device.ID)
    case settings
}

struct RootView: View {
    @State private var path: [Route] = []

    var body: some View {
        NavigationStack(path: $path) {
            DeviceList(onSelect: { path.append(.device($0)) })
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .device(let id): DeviceDetail(id: id)
                    case .firmware(let id): FirmwareUpdate(id: id)
                    case .settings: SettingsView()
                    }
                }
        }
    }
}
```

- Routes carry identifiers, not models, so they are cheap, `Hashable` and restorable.
- One `navigationDestination(for:)` per type, attached inside the stack, not inside lazy containers.
- `NavigationPath` only when the stack really holds unrelated types.
- `NavigationSplitView` for iPad and Mac layouts. `NavigationView` is deprecated.

## Identity and performance

```swift
// BAD: id regenerated on every render, every row is new every time
ForEach(readings.map { RowItem(id: UUID(), reading: $0) }) { RowView(item: $0) }

// GOOD
ForEach(readings) { reading in ReadingRow(reading: reading) } // Reading.id comes from the data
```

- `.id(value)` on a view discards its state when `value` changes. Use it only to reset on purpose.
- Prefer `if` / `switch` inside a `@ViewBuilder` over `AnyView`. Same-type branches can use modifiers
  (`.opacity`, `.disabled`) instead of swapping views, which keeps identity.
- `body` does no I/O, sorting of large arrays, or formatter creation. Precompute in the model or use
  `Text(date, format: .dateTime.hour().minute())`.
- `LazyVStack` / `List` for long or unbounded lists; `VStack` only for short fixed content.
- Split views at natural boundaries. A subview re-renders only when its inputs change.

## Previews

```swift
#Preview {
    DeviceListScreen()
        .environment(Store.preview)
}

#Preview("Toggle states") {
    @Previewable @State var isOn = true
    Toggle("Auto reconnect", isOn: $isOn)
}
```

- Previews use in-memory or fake dependencies, never live network or BLE.

## Accessibility

- Meaningful images get `.accessibilityLabel`; decorative ones use `Image(decorative:)`.
- Use text styles (`.font(.body)`), not fixed point sizes, so Dynamic Type works.
- Combine row content with `.accessibilityElement(children: .combine)` when a row reads as one item.
- Tap targets at least 44x44 points.
