# MVI with Swift, SwiftUI and a small Store

Load this when building or reviewing an MVI-style feature in Swift. Assumes Swift 6 language mode,
iOS 17 or newer, and Swift Testing. The store below is hand-rolled and dependency-free; see the end of
this file for when to use The Composable Architecture (TCA) instead.

The feature: repository search with debounce, latest-query-wins, retry, and navigation to details
driven by state.

## Contract

```swift
struct Repo: Identifiable, Equatable, Sendable {
    let id: String
    let name: String
}

protocol SearchClient: Sendable {
    func search(_ query: String) async throws -> [Repo]
}
```

## Actions and state

```swift
enum SearchAction: Equatable, Sendable {
    // From the view
    case queryChanged(String)
    case retryTapped
    case resultTapped(Repo.ID)
    case detailsDismissed
    // From effects only
    case loaded(query: String, [Repo])
    case failed(query: String)
}

struct SearchState: Equatable {
    var query = ""
    var items: [Repo] = []
    var isLoading = false
    var hasError = false
    var selectedRepo: Repo.ID?

    var showEmpty: Bool { !query.isEmpty && !isLoading && !hasError && items.isEmpty }
}
```

- Navigation is state (`selectedRepo`), so it survives view re-creation and is visible in tests.

## Reducer

```swift
enum SearchReducer {
    static func reduce(_ state: SearchState, _ action: SearchAction) -> SearchState {
        var state = state
        switch action {
        case .queryChanged(let query):
            state.query = query
            state.hasError = false
            state.isLoading = !query.isEmpty
            if query.isEmpty { state.items = [] }

        case .retryTapped:
            state.isLoading = true
            state.hasError = false

        case .resultTapped(let id):
            state.selectedRepo = id

        case .detailsDismissed:
            state.selectedRepo = nil

        case let .loaded(query, items):
            guard query == state.query else { return state }
            state.items = items
            state.isLoading = false

        case .failed(let query):
            guard query == state.query else { return state }
            state.isLoading = false
            state.hasError = true
        }
        return state
    }
}
```

- `switch` without `default`: a new action is a compile error until handled.
- `var state = state` mutates a local copy of a value type; the function stays pure.

## Store

```swift
@MainActor
@Observable
final class SearchStore {
    private(set) var state = SearchState()

    @ObservationIgnored private let client: any SearchClient
    @ObservationIgnored private let debounce: Duration
    @ObservationIgnored private var searchTask: Task<Void, Never>?

    init(client: any SearchClient, debounce: Duration = .milliseconds(300)) {
        self.client = client
        self.debounce = debounce
    }

    /// Reduces the action, then starts its effect. Returns the effect's task so tests can await it.
    @discardableResult
    func send(_ action: SearchAction) -> Task<Void, Never>? {
        state = SearchReducer.reduce(state, action)
        switch action {
        case .queryChanged(let query):
            return search(query, after: debounce)
        case .retryTapped:
            return search(state.query, after: .zero)
        case .resultTapped, .detailsDismissed, .loaded, .failed:
            return nil
        }
    }

    private func search(_ query: String, after delay: Duration) -> Task<Void, Never>? {
        searchTask?.cancel()
        guard !query.isEmpty else { return nil }
        let task = Task { [client] in
            do {
                try await Task.sleep(for: delay)
                let items = try await client.search(query)
                guard !Task.isCancelled else { return }
                send(.loaded(query: query, items))
            } catch {
                guard !Task.isCancelled else { return }
                send(.failed(query: query))
            }
        }
        searchTask = task
        return task
    }
}
```

Notes:
- The store is `@MainActor`, and the `Task` inherits it, so `send` from the effect is a main-actor call.
- `Task.sleep` throws when cancelled, which is the debounce. The `Task.isCancelled` checks stop a cancelled
  request from reporting `failed` (for example `URLError(.cancelled)`) after a newer query started.
- Effects never assign `state`; they call `send` with a result action.
- For time-heavy logic, inject `any Clock<Duration>` instead of a `Duration` and sleep on the clock.

## View

```swift
struct SearchView: View {
    @State private var store: SearchStore

    init(client: any SearchClient) {
        _store = State(initialValue: SearchStore(client: client))
    }

    var body: some View {
        NavigationStack {
            List(store.state.items) { repo in
                Button(repo.name) { store.send(.resultTapped(repo.id)) }
            }
            .overlay {
                if store.state.isLoading {
                    ProgressView()
                } else if store.state.hasError {
                    ContentUnavailableView {
                        Label("Search failed", systemImage: "wifi.exclamationmark")
                    } actions: {
                        Button("Retry") { store.send(.retryTapped) }
                    }
                } else if store.state.showEmpty {
                    ContentUnavailableView.search(text: store.state.query)
                }
            }
            .searchable(text: Binding(
                get: { store.state.query },
                set: { store.send(.queryChanged($0)) }
            ))
            .navigationDestination(item: Binding(
                get: { store.state.selectedRepo },
                set: { if $0 == nil { store.send(.detailsDismissed) } }
            )) { id in
                RepoDetailView(id: id)
            }
        }
    }
}
```

- Bindings route writes through `send`; the view never assigns state.
- Every reader of `store.state` re-evaluates on any state change. Large screens pass child views plain
  values (`RepoRow(repo: repo)`) so SwiftUI can skip unchanged children.

## Reducer tests (pure)

```swift
import Testing
@testable import Search

extension Repo {
    static let swiftRepo = Repo(id: "1", name: "swift")
}

struct SearchReducerTests {
    @Test func queryChangeStartsLoadingAndClearsError() {
        let next = SearchReducer.reduce(SearchState(hasError: true), .queryChanged("swift"))
        #expect(next == SearchState(query: "swift", isLoading: true))
    }

    @Test func emptyQueryClearsResults() {
        let state = SearchState(query: "s", items: [.swiftRepo])
        #expect(SearchReducer.reduce(state, .queryChanged("")) == SearchState())
    }

    @Test func staleResultIsIgnored() {
        let state = SearchState(query: "swift", isLoading: true)
        #expect(SearchReducer.reduce(state, .loaded(query: "sw", [.swiftRepo])) == state)
    }

    @Test func failureShowsError() {
        let state = SearchState(query: "swift", isLoading: true)
        #expect(SearchReducer.reduce(state, .failed(query: "swift")) == SearchState(query: "swift", hasError: true))
    }

    @Test func tappingResultSelectsIt() {
        let next = SearchReducer.reduce(SearchState(), .resultTapped("1"))
        #expect(next.selectedRepo == "1")
    }
}
```

## Store and effect tests

```swift
actor FakeSearchClient: SearchClient {
    private(set) var queries: [String] = []
    private let results: [String: [Repo]]
    private let error: (any Error)?

    init(results: [String: [Repo]] = [:], error: (any Error)? = nil) {
        self.results = results
        self.error = error
    }

    func search(_ query: String) async throws -> [Repo] {
        queries.append(query)
        if let error { throw error }
        return results[query] ?? []
    }
}

@MainActor
struct SearchStoreTests {
    @Test func searchLoadsResults() async {
        let store = SearchStore(client: FakeSearchClient(results: ["swift": [.swiftRepo]]), debounce: .zero)

        await store.send(.queryChanged("swift"))?.value

        #expect(store.state == SearchState(query: "swift", items: [.swiftRepo]))
    }

    @Test func newQueryCancelsPreviousSearch() async {
        let client = FakeSearchClient()
        let store = SearchStore(client: client, debounce: .milliseconds(20))

        let first = store.send(.queryChanged("s"))
        let second = store.send(.queryChanged("sw"))
        await first?.value
        await second?.value

        #expect(await client.queries == ["sw"])
    }

    @Test func failureShowsError() async {
        let client = FakeSearchClient(error: URLError(.notConnectedToInternet))
        let store = SearchStore(client: client, debounce: .zero)

        await store.send(.queryChanged("swift"))?.value

        #expect(store.state == SearchState(query: "swift", hasError: true))
    }
}
```

- `send` returns the effect task, so tests `await` it instead of sleeping.
- The cancellation test waits a short real delay (20 ms). If the suite grows time-dependent tests,
  inject a clock and drive it from the test.
- The fake is an `actor`, so recording queries is data-race free under Swift 6 checking.

## The Composable Architecture (TCA)

Consider TCA instead of a hand-rolled store when:
- Several teams build features that must compose (parent and child features, shared dependencies).
- Exhaustive testing of every state change and effect is a requirement.
- The team accepts a large third-party dependency and its migration cost between major versions.

When the project uses TCA, follow its current documentation for reducers, effects, dependencies and its
test store. Keep the same principles: pure state changes, effects returned rather than performed inline,
results sent back as actions. Do not mix TCA features and hand-rolled stores inside one feature.
