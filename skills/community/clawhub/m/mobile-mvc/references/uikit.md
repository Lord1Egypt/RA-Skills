# UIKit MVC reference

Load this when the screen is a `UIViewController` written in Swift. Assumes Swift 6 language mode, where
`UIViewController` and `UIView` are `@MainActor`.

## Where each responsibility goes

| Found in the view controller | Move it to |
|---|---|
| `URLSession`, request building, JSON decoding | A service or repository protocol, injected through `init` |
| Core Data, SwiftData, file or Keychain access | A store type behind a protocol |
| Date, number, measurement formatting | Row or display models built from domain models |
| Input validation | A pure validator type with unit tests |
| `UITableViewDataSource`, `UICollectionViewDataSource` | A diffable data source plus a cell provider |
| `pushViewController`, `present`, building the next screen | A coordinator |
| Large view hierarchy built in `viewDidLoad` | A custom `UIView` subclass returned from `loadView()` |
| Independent regions (header, map, list) | Child view controllers |

What stays: owning the root view, binding data to views, forwarding user actions, lifecycle hooks.

## Custom root view

```swift
// BAD: 150 lines of constraints in viewDidLoad
override func viewDidLoad() {
    super.viewDidLoad()
    let stack = UIStackView()
    // ...
}

// GOOD: the view owns its layout; the controller binds
final class DevicesView: UIView {
    let tableView = UITableView(frame: .zero, style: .insetGrouped)
    let emptyLabel = UILabel()
    // layout in init
}

final class DevicesViewController: UIViewController {
    private var rootView: DevicesView { view as! DevicesView }
    override func loadView() { view = DevicesView() }
}
```

The forced cast is safe here because `loadView()` sets the type in the same class.

## Child view controllers

Every containment step is required. Skipping `addChild` or `didMove(toParent:)` breaks appearance
callbacks, trait propagation and safe-area handling.

```swift
// BAD
headerContainer.addSubview(header.view)

// GOOD
func embed(_ child: UIViewController, in container: UIView) {
    addChild(child)
    child.view.translatesAutoresizingMaskIntoConstraints = false
    container.addSubview(child.view)
    NSLayoutConstraint.activate([
        child.view.topAnchor.constraint(equalTo: container.topAnchor),
        child.view.bottomAnchor.constraint(equalTo: container.bottomAnchor),
        child.view.leadingAnchor.constraint(equalTo: container.leadingAnchor),
        child.view.trailingAnchor.constraint(equalTo: container.trailingAnchor),
    ])
    child.didMove(toParent: self)
}

func remove(_ child: UIViewController) {
    child.willMove(toParent: nil)
    child.view.removeFromSuperview()
    child.removeFromParent()
}
```

- Children talk to the parent through closures or a delegate, not by reaching into `parent`.
- Each child has its own dependencies and can be tested and previewed alone.

## Coordinators

The coordinator builds screens, injects their dependencies and performs navigation. Screens expose
intent through closures or a delegate.

```swift
@MainActor
protocol Coordinator: AnyObject {
    func start()
}

@MainActor
final class DevicesCoordinator: Coordinator {
    private let navigationController: UINavigationController
    private let service: DeviceService
    private var children: [Coordinator] = []

    init(navigationController: UINavigationController, service: DeviceService) {
        self.navigationController = navigationController
        self.service = service
    }

    func start() {
        let list = DevicesViewController(service: service)
        list.onSelectDevice = { [weak self] id in self?.showDetail(id) }
        navigationController.pushViewController(list, animated: false)
    }

    private func showDetail(_ id: Device.ID) {
        let detail = DeviceDetailViewController(deviceID: id, service: service)
        navigationController.pushViewController(detail, animated: true)
    }
}
```

- Closures from screens to coordinators capture the coordinator `[weak self]`.
- The coordinator holds the navigation controller, not the screens. Screens are owned by UIKit.
- Child coordinators are kept in `children` and removed when their flow finishes. Detect a user-driven
  back navigation with `UINavigationControllerDelegate.navigationController(_:didShow:animated:)`,
  or with a callback from the screen's `viewDidDisappear` when `isMovingFromParent` is true.
- Deep links and push notifications enter through the app coordinator, which routes to the right flow.

## Diffable data sources and cell registration

```swift
// BAD: model array and index paths drift apart; full reload loses animation and selection
devices.remove(at: indexPath.row)
tableView.reloadData()

// GOOD: identifiers in the snapshot, models looked up by id
enum Section { case main }

private lazy var dataSource = makeDataSource()

private func makeDataSource() -> UICollectionViewDiffableDataSource<Section, Device.ID> {
    let registration = UICollectionView.CellRegistration<UICollectionViewListCell, Device.ID> {
        [weak self] cell, _, id in
        guard let row = self?.rows[id] else { return }
        var content = cell.defaultContentConfiguration()
        content.text = row.title
        content.secondaryText = row.lastSeen
        cell.contentConfiguration = content
    }
    return UICollectionViewDiffableDataSource(collectionView: collectionView) { collectionView, indexPath, id in
        collectionView.dequeueConfiguredReusableCell(using: registration, for: indexPath, item: id)
    }
}

private func apply(_ devices: [Device]) {
    rows = Dictionary(uniqueKeysWithValues: devices.map { ($0.id, DeviceRow($0)) })
    var snapshot = NSDiffableDataSourceSnapshot<Section, Device.ID>()
    snapshot.appendSections([.main])
    snapshot.appendItems(devices.map(\.id))
    dataSource.apply(snapshot, animatingDifferences: true)
}
```

- Use stable identifiers as item identifiers, not whole models; duplicate identifiers crash at apply time.
- When content changes but identity does not, use `snapshot.reconfigureItems(_:)` instead of a reload.
- Create cell registrations once, outside the cell provider closure.
- For a large or reused data source, move `makeDataSource` and `apply` into a dedicated
  `DevicesListAdapter` object the controller owns.

## Async work in a view controller

```swift
// BAD: Task lives on after the screen is popped and retains it
override func viewDidLoad() {
    super.viewDidLoad()
    Task { self.apply(try await service.devices()) }
}

// GOOD
private var loadTask: Task<Void, Never>?

override func viewWillAppear(_ animated: Bool) {
    super.viewWillAppear(animated)
    loadTask = Task { [weak self, service] in
        do {
            let devices = try await service.devices()
            self?.apply(devices)
        } catch is CancellationError {
        } catch {
            self?.showError(error)
        }
    }
}

override func viewDidDisappear(_ animated: Bool) {
    super.viewDidDisappear(animated)
    loadTask?.cancel()
}
```

- Notification observers: store the token from block-based `addObserver(forName:object:queue:using:)`
  and remove it, or iterate `NotificationCenter.default.notifications(named:)` inside a stored task.
- Delegates are `weak`.

## Testing

- Unit-test row models, validators, services and coordinators without UIKit rendering.
- For controller tests, call `loadViewIfNeeded()` and drive it through its public API with fake services.
- Coordinators are tested by giving them a `UINavigationController` and asserting on `viewControllers`.
