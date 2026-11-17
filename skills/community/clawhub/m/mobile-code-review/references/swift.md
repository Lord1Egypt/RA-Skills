# Swift and iOS review reference

Load this when the change contains `.swift` files. Assume Swift 6 language mode with strict concurrency
unless the project settings say otherwise.

## Quick scan

| Pattern | Why | Usual severity |
|---|---|---|
| `!` force unwrap, `try!`, `as!` | Crash on unexpected input | Major, Blocker on external data |
| Implicitly unwrapped `var x: T!` outside IBOutlets | Crash if read early | Minor |
| Escaping closure using `self` without `[weak self]`, stored by `self` | Retain cycle | Major |
| `unowned self` | Crash if the owner is gone first | Major unless lifetime is guaranteed |
| `@unchecked Sendable` | Silences data-race checking | Major unless a lock guards every field |
| `nonisolated(unsafe)` | Same | Major unless justified |
| `DispatchQueue.main.async` inside `async` code | Mixes models, loses isolation checking | Minor |
| `Task.detached` | Drops actor context and priority | Minor, needs a reason |
| `DispatchSemaphore.wait()` / `.sync` on main | Deadlock or hang | Blocker |
| `@ObservedObject var model = Model()` | Model recreated on every parent redraw | Major |
| `ForEach(..., id: \.self)` over non-unique values | Wrong rows update, crashes on duplicates | Major |
| `AnyView` in lists | Defeats diffing | Minor |
| `print(` with tokens, emails, device IDs | Personal data in logs | Major, see `mobile-security` |

## Concurrency

- UI-facing models are `@MainActor`. View models built with `@Observable` are usually `@MainActor final class`.
- Types crossing isolation boundaries are `Sendable`. Prefer value types; make reference types final with
  immutable state or protect them with an actor.
- Actor reentrancy: state read before an `await` may have changed after it.

```swift
// BAD: two concurrent calls both see nil and both download
actor ImageCache {
    var images: [URL: Image] = [:]
    func image(for url: URL) async throws -> Image {
        if let cached = images[url] { return cached }
        let image = try await download(url)
        images[url] = image
        return image
    }
}

// GOOD: cache the in-flight task, not just the result
actor ImageCache {
    private var tasks: [URL: Task<Image, Error>] = [:]
    func image(for url: URL) async throws -> Image {
        if let task = tasks[url] { return try await task.value }
        let task = Task { try await download(url) }
        tasks[url] = task
        return try await task.value
    }
}
```

- Long-running `for await` loops inside a `Task` stored by a class capture `self` until the loop ends,
  so `deinit` never runs. Use `[weak self]` inside the loop body, or tie the work to `.task` in the view.

```swift
// BAD: self is retained by the task forever, deinit never cancels it
task = Task {
    for await value in stream { self.handle(value) }
}

// GOOD
task = Task { [weak self] in
    for await value in stream {
        guard let self else { return }
        self.handle(value)
    }
}
```

- Cancellation is checked in long loops (`try Task.checkCancellation()` or `Task.isCancelled`).
- `withTaskGroup` / `withThrowingTaskGroup` instead of manually spawning many `Task {}` and joining.

## Memory

- Delegates are `weak var delegate: SomeDelegate?` with a class-constrained protocol.
- Combine: `sink` closures capture `self` weakly; `AnyCancellable` stored and released with the owner.
- Block-based `NotificationCenter` observers are removed, or replaced by
  `for await _ in NotificationCenter.default.notifications(named: ...)` inside `.task`.

## SwiftUI

- Ownership: `@State private var model = Model()` for `@Observable` models the view creates;
  `@StateObject` for legacy `ObservableObject`. Passed-in models are plain properties (`@Observable`) or
  `@ObservedObject` (legacy).
- `body` is cheap and pure: no formatting with new `DateFormatter()` per call, no I/O, no sorting large arrays.
- Async work starts in `.task` or `.task(id:)`, which cancels on disappear or id change.
- Identity: `ForEach` uses stable `Identifiable` ids. `.id(x)` on a view resets its state when `x` changes;
  check that is intended.
- `NavigationStack` with a typed path for programmatic navigation; no deprecated `NavigationView` in new code.
- Accessibility: images that convey meaning have `.accessibilityLabel`; decorative images use
  `Image(decorative:)`; custom controls set `.accessibilityAddTraits(.isButton)`; text uses Dynamic Type
  styles, not fixed sizes.

## Errors and safety

- `try?` only where failure is truly irrelevant; otherwise `do / catch` with a user-visible state.
- Typed throws (`throws(MyError)`) where the error set is closed and callers switch over it.
- `guard let` early exits instead of nested `if let` pyramids.
- `Codable` models tolerate missing optional fields from the server (`decodeIfPresent` or optional properties).

## Testing

- Swift Testing (`@Test`, `#expect`, `#require`) for new tests; XCTest is fine in existing suites.
- Async tests `await` the operation. In XCTest async contexts use `await fulfillment(of:timeout:)`,
  not `wait(for:)`.
- No `sleep` in tests. Inject clocks (`any Clock<Duration>`) or schedulers.
- Protocols at boundaries (network, storage) so fakes can be injected.

## Project and dependencies

- New SPM packages pinned to a version range, `Package.resolved` committed for apps.
- New `Info.plist` keys, entitlements, background modes or privacy usage strings are called out in the MR.
- New required-reason API usage is reflected in `PrivacyInfo.xcprivacy`.
