---
name: mobile-mvc
description: "Fixes controller-based mobile code: UIKit MVC and Massive View Controllers (child view controllers, coordinators, separate data sources), legacy Android Activity-as-controller and MVP, and Flutter controllers, plus step-by-step migration to MVVM one screen at a time. Use when working on UIViewController, Activity, Fragment or presenter code, splitting a god class, or deciding whether MVC is still fine."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile MVC and MVP

Keep controller-based screens small, testable and leak-free, and move them to MVVM safely when that pays
off. Covers UIKit MVC, legacy Android Activity-as-controller and MVP, and Flutter controllers.

## When to use

- A `UIViewController`, `Activity` or `Fragment` has grown past a few hundred lines and mixes
  networking, formatting, navigation and view code.
- Adding a feature to a legacy MVC or MVP screen without rewriting it.
- Reviewing presenter code for leaks, or a Flutter widget whose `State` holds all the logic.
- Deciding whether a screen should stay MVC or move to MVVM.
- Planning or executing a screen-by-screen migration to ViewModels.

Not for: designing new screens in MVVM or MVI from scratch (use `mobile-mvvm`, `mobile-mvi`).

## Workflow

1. Identify the platform and pattern actually in use, and load the matching reference:
   [UIKit](references/uikit.md), [Android legacy and MVP](references/android-legacy.md),
   [Flutter controllers](references/flutter.md).
2. Map the controller's responsibilities. For each method, tag it: view setup, layout, data source,
   networking, persistence, formatting, validation, navigation, lifecycle.
3. Decide: keep, slim down, or migrate (see "When MVC is still fine" below). Prefer the smallest change
   that fixes the actual pain.
4. Before moving code, add characterization tests around behaviour that will move (formatting,
   validation, state transitions). If logic is untestable in place, extract it as a pure function first.
5. Extract one responsibility at a time, in this order: formatting, networking and persistence behind a
   service, data source objects, navigation into a coordinator or navigator, child controllers for
   independent regions.
6. Fix lifecycle on the way: presenters detach, observers are removed, tasks are cancelled, controllers
   are disposed.
7. If migrating, follow [migration to MVVM](references/migration-to-mvvm.md): one screen per MR,
   ViewModel introduced behind the existing controller, state moved field by field.
8. Build, run the tests, and exercise the screen on device, including rotation (Android) and
   background and foreground.

## When MVC is still fine

- Static or nearly static screens: settings lists, about pages, legal text, simple forms.
- Thin wrappers around system controllers (pickers, mail compose, share sheets, web views).
- Screens with no business rules and no state that must survive configuration change.
- Code scheduled for deletion. Do not migrate what is about to be removed.
- A team or codebase where MVC is consistent and screens stay small. Consistency beats a half-migrated mix.

Migrate when: logic needs unit tests, state is lost on rotation or process death, the same logic is
duplicated across screens, or the controller cannot be changed without regressions.

## Rules

### 1. The controller owns views, not networking or persistence

Swift:
```swift
// BAD: view controller builds requests and decodes JSON
override func viewDidLoad() {
    super.viewDidLoad()
    URLSession.shared.dataTask(with: URL(string: "https://api.example.com/devices")!) { data, _, _ in
        let devices = try! JSONDecoder().decode([Device].self, from: data!)
        DispatchQueue.main.async { self.devices = devices; self.tableView.reloadData() }
    }.resume()
}

// GOOD: injected service, the controller only renders
final class DevicesViewController: UIViewController {
    private let service: DeviceService
    init(service: DeviceService) {
        self.service = service
        super.init(nibName: nil, bundle: nil)
    }
    required init?(coder: NSCoder) { fatalError("init(coder:) is not supported") }
}
```

Java:
```java
// BAD: Activity opens sockets and parses responses
new Thread(() -> {
    String json = httpGet("https://api.example.com/devices");
    runOnUiThread(() -> adapter.submit(parse(json)));
}).start();

// GOOD: presenter asks a repository; the Activity only renders
presenter.loadDevices();
```

### 2. Navigation is decided outside the screen

Swift:
```swift
// BAD: the screen knows the next screen and how to build it
let detail = DeviceDetailViewController(service: DeviceServiceImpl(), device: device)
navigationController?.pushViewController(detail, animated: true)

// GOOD: the screen reports intent; a coordinator decides
var onSelectDevice: ((Device.ID) -> Void)?
func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
    guard let id = dataSource.itemIdentifier(for: indexPath) else { return }
    onSelectDevice?(id)
}
```

Kotlin:
```kotlin
// BAD: presenter starts Activities
class DevicesPresenter(private val activity: Activity) {
    fun onDeviceClicked(id: String) = activity.startActivity(Intent(activity, DetailActivity::class.java))
}

// GOOD: presenter calls a view method; the Activity or a navigator performs it
interface DevicesView { fun openDetail(deviceId: String) }
```

### 3. Data sources and delegates are separate objects

Swift:
```swift
// BAD: index-based data source in the controller, reloadData on every change
extension DevicesViewController: UITableViewDataSource {
    func tableView(_ t: UITableView, numberOfRowsInSection s: Int) -> Int { devices.count }
    func tableView(_ t: UITableView, cellForRowAt i: IndexPath) -> UITableViewCell { ... }
}

// GOOD: diffable data source keyed by stable ids, owned by the controller, configured once
private lazy var dataSource = UITableViewDiffableDataSource<Section, Device.ID>(tableView: tableView) {
    [weak self] tableView, indexPath, id in
    self?.cellProvider.cell(in: tableView, at: indexPath, for: id)
}
```

Kotlin:
```kotlin
// BAD: notifyDataSetChanged on every update
adapter.items = devices; adapter.notifyDataSetChanged()

// GOOD: ListAdapter with DiffUtil, stable ids in areItemsTheSame
adapter.submitList(devices)
```

### 4. Formatting lives in formatters, not in cells or controllers

Swift:
```swift
// BAD: new formatter per cell, logic untestable
cell.detail.text = { let f = DateFormatter(); f.dateFormat = "dd.MM.yyyy"; return f.string(from: d.lastSeen) }()

// GOOD: a testable row model built outside the cell
struct DeviceRow { let title: String; let lastSeen: String }
extension DeviceRow {
    init(_ d: Device) {
        title = d.name
        lastSeen = d.lastSeen.formatted(date: .abbreviated, time: .shortened)
    }
}
```

Dart:
```dart
// BAD: formatting inside build
Text('${(device.battery * 100).round()}% - ${device.lastSeen.toLocal()}')

// GOOD: controller or row model exposes display strings, tested without widgets
Text(row.batteryLabel)
```

### 5. A presenter never outlives its view

Java:
```java
// BAD: presenter keeps the Activity after onDestroy; async callback touches a dead view
@Override public void onDevicesLoaded(List<Device> devices) { view.showDevices(devices); }

// GOOD: attach and detach with the lifecycle; callbacks check the view
public void attach(DevicesContract.View view) { this.view = view; }
public void detach() { this.view = null; cancelPending(); }

@Override public void onDevicesLoaded(List<Device> devices) {
    if (view != null) view.showDevices(devices);
}
// Activity: presenter.detach() in onDestroy()
```

- `WeakReference<View>` hides the leak but keeps the work running. Cancel the work too.

### 6. Presenters and controllers are free of framework types

Kotlin:
```kotlin
// BAD: presenter needs Context and a Looper, so it cannot run in a plain JUnit test
class LoginPresenter(private val context: Context) {
    fun onLogin() = Toast.makeText(context, context.getString(R.string.error), Toast.LENGTH_SHORT).show()
}

// GOOD: presenter depends on interfaces; the view decides how to show an error
class LoginPresenter(private val auth: AuthRepository, private val scope: CoroutineScope) {
    private var view: LoginContract.View? = null
    fun onLogin(email: String, password: String) {
        scope.launch {
            val result = auth.login(email, password)
            view?.render(if (result.isSuccess) LoginState.Done else LoginState.Error(LoginError.InvalidCredentials))
        }
    }
}
```

Swift: controllers' helpers (formatters, validators, services) import `Foundation`, not `UIKit`.

### 7. Flutter controllers are owned by State and disposed

Dart:
```dart
// BAD: controller created in build, logic in State, never disposed
@override
Widget build(BuildContext context) {
  final controller = PairingController(repo);
  return ListenableBuilder(listenable: controller, builder: (_, __) => Text(controller.status));
}

// GOOD
class _PairingScreenState extends State<PairingScreen> {
  late final PairingController _controller = PairingController(widget.repo);

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => ListenableBuilder(
        listenable: _controller,
        builder: (context, _) => Text(_controller.status),
      );
}
```

### 8. Async results check that the screen is still there

Swift:
```swift
// BAD: retains the controller and updates it after it was popped
loadTask = Task { self.render(try await service.devices()) }

// GOOD: weak self, capture only the service, cancel on disappear
loadTask = Task { [weak self, service] in
    do {
        let devices = try await service.devices()
        self?.render(devices)
    } catch {
        self?.showError(error)
    }
}
override func viewDidDisappear(_ animated: Bool) {
    super.viewDidDisappear(animated)
    loadTask?.cancel()
}
```

Dart:
```dart
// BAD
await _controller.pair();
Navigator.of(context).pop();

// GOOD
await _controller.pair();
if (!mounted) return;
Navigator.of(context).pop();
```

### 9. Dependencies come in through the initializer or constructor

Swift:
```swift
// BAD: hidden singletons, impossible to fake
let devices = try await APIClient.shared.devices()

// GOOD: storyboard screens can still use init injection via a custom init?(coder:service:)
let vc = storyboard.instantiateViewController(identifier: "Devices") { coder in
    DevicesViewController(coder: coder, service: service)
}
```

Kotlin:
```kotlin
// BAD
private val repo = DeviceRepository.getInstance()

// GOOD: presenter constructed with its dependencies (Hilt or a manual factory)
class DevicesPresenter @Inject constructor(private val repo: DeviceRepository)
```

### 10. Migrate one screen at a time, tests first

```text
# BAD
refactor: migrate whole app to MVVM (214 files)

# GOOD: one screen, three small MRs
test(devices): characterization tests for DevicesPresenter
refactor(devices): add DevicesViewModel behind DevicesActivity
refactor(devices): move device list state to DevicesViewModel, remove presenter
```

Details and code: [migration to MVVM](references/migration-to-mvvm.md).

## Anti-patterns

- Massive View Controller: networking, parsing, formatting, data source, delegate and navigation in one
  class with a dozen `extension`s that only hide the size.
- "Manager" or "Helper" singletons that every controller calls, replacing one god class with a global one.
- Presenter holding `Activity` or `Context` and never detached; work keeps running after `onDestroy`.
- Using `AsyncTask` (deprecated) or Loaders (deprecated) in maintained code.
- Child view controllers added as subviews without `addChild` and `didMove(toParent:)`, so appearance
  callbacks and trait changes do not propagate.
- Coordinators holding strong references to the view controllers they push and never releasing them.
- Flutter `State` classes with hundreds of lines of business logic and `setState` calls from async code.
- Big-bang migration of every screen in one MR, or migrating screens that work and are not changing.
- Introducing a ViewModel but leaving the old state in the controller too, so there are two sources of truth.

## Checklist

- [ ] Controller code is view setup, binding and lifecycle only
- [ ] Networking and persistence behind injected services or repositories
- [ ] Formatting and validation in testable types, not in cells, widgets or controllers
- [ ] Table and collection data sources are separate objects, diffable or DiffUtil based
- [ ] Navigation goes through a coordinator, navigator or view callback
- [ ] Child view controllers use the full containment calls
- [ ] Presenters attach and detach with the lifecycle and cancel pending work
- [ ] Presenters and helpers do not import `android.*` or `UIKit`
- [ ] Flutter controllers created in `initState` or a `late final` field and disposed in `dispose`
- [ ] Async callbacks check `mounted`, a non-null view or `[weak self]` before updating UI
- [ ] Characterization tests exist before logic is moved
- [ ] Migration is one screen per MR, with one source of truth for each piece of state

## Related skills

- `mobile-mvvm` -- target architecture when migrating
- `mobile-mvi` -- alternative target for complex, event-heavy screens
- `mobile-design-patterns` -- coordinator, adapter, strategy and facade patterns used here
- `mobile-swift`, `mobile-java`, `mobile-kotlin`, `mobile-flutter` -- language rules for the code being moved
- `mobile-code-review` -- reviewing the refactoring MRs
- `mobile-testing` -- characterization tests before a migration
