---
name: mobile-mvi
description: "Designs, implements and tests screens with MVI on Android, iOS and Flutter: intents as sealed types, one immutable state, a pure reducer and side effects fed back as actions, using Kotlin StateFlow stores, Swift @Observable stores (TCA as an option) and Dart Bloc or Cubit. Use for screens with many interacting events, debounced search or racing requests, or when adopting or reviewing Bloc or Redux-style code."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# MVI for mobile apps

Build screens where every change goes through one loop: the UI sends an intent, a pure reducer computes
the next state, effects do the IO outside the reducer and report back as new actions. State transitions
become plain functions that are trivial to test, replay and reason about under concurrency.

## When to use

- A screen has many events that interact: typing, retry, refresh, pagination, selection, live updates.
- Requests race each other (debounced search, rapid toggles, BLE or socket updates arriving mid-request).
- State transitions must be auditable or tested exhaustively (payments, onboarding wizards, editors).
- The codebase already uses Bloc, TCA, Orbit, Mavericks or a hand-rolled store, and new code must fit.
- Reviewing an MVI store for impure reducers, lost effects or oversized state.

Not for: simple read-only or CRUD screens; MVVM with a single `UiState` is enough there
(use `mobile-mvvm`). Do not convert a whole app to MVI to fix one complex screen.

## The loop

```
          +----------------------- State -----------------------+
          v                                                      |
   UI renders State --- Intent ---> Store --- (State, Action) ---> Reducer (pure)
                                      |                              ^
                                      | effect for this action       | Result action
                                      v                              |
                                   Effect runner (IO, timers, navigation)
```

| Part | What it is | Kotlin | Swift | Dart |
|---|---|---|---|---|
| Intent | What the user did | `sealed interface SearchIntent` | `enum SearchAction` cases | `sealed class SearchEvent` |
| Result | What an effect produced | `sealed interface SearchResult` | more `SearchAction` cases | internal result classes |
| State | Everything the screen renders | `data class` | `struct: Equatable` | `@immutable` class or `Equatable` |
| Reducer | `(State, Action) -> State`, no IO | top-level or `object` function | `static func` | top-level function |
| Effect | IO, timers, navigation, analytics | coroutine in `viewModelScope` | `Task` owned by the store | code in a Bloc handler |
| Store | Holds state, runs the loop | `ViewModel` + `StateFlow` | `@MainActor @Observable` class | `Bloc` |

## Workflow

1. Confirm the screen needs MVI (see When to use). If not, use `mobile-mvvm`.
2. Load the reference for the platform: [Kotlin and Compose](references/kotlin.md),
   [Swift and SwiftUI](references/swift.md), [Dart with Bloc](references/dart.md).
3. Write the `State`: the minimum the UI renders. Derive the rest with computed properties.
4. List intents from the UI as a sealed type, named after what happened (`QueryChanged`, `RetryClicked`).
5. List results the effects can produce (`Loaded`, `Failed`), each carrying what the reducer needs
   to reject stale data (for example the query it was for).
6. Write the reducer and its tests first. It is pure, so the tests need no mocks or dispatchers.
7. Write the store: apply the reducer, then start the effect for the action with an explicit
   concurrency policy (cancel previous, drop new, or queue).
8. Decide how one-off effects reach the UI: state field first, effect channel only if needed.
9. Build the UI: render `State`, send intents, never mutate state directly.
10. Write effect tests with fakes and virtual time. Run the existing test suite and report failures.

## Rules

### 1. Intents are one sealed type named after what happened

Kotlin:
```kotlin
// BAD: commands named after implementation, open to anything
fun setLoading(value: Boolean)
fun callSearchApi(query: String)

// GOOD
sealed interface SearchIntent {
    data class QueryChanged(val query: String) : SearchIntent
    data object RetryClicked : SearchIntent
    data class ResultClicked(val id: String) : SearchIntent
}
```

Swift:
```swift
enum SearchAction: Equatable, Sendable {
    case queryChanged(String)                  // from the view
    case retryTapped
    case resultTapped(Repo.ID)
    case detailsDismissed
    case loaded(query: String, [Repo])         // from effects
    case failed(query: String)
}
```

Dart:
```dart
sealed class SearchEvent { const SearchEvent(); }
final class QueryChanged extends SearchEvent { const QueryChanged(this.query); final String query; }
final class RetryPressed extends SearchEvent { const RetryPressed(); }
```

- Exhaustive `when` / `switch` over a sealed type makes the compiler flag every unhandled intent.
- Kotlin can split public intents and internal results into two sealed sub-interfaces of one `SearchAction`,
  so the UI cannot send a result. Swift enums cannot; mark effect-only cases with a comment.

### 2. One immutable State; derive instead of duplicating

```kotlin
// BAD: flags that can contradict each other, list duplicated for filtering
data class SearchState(
    val isLoading: Boolean, val isError: Boolean, val isEmpty: Boolean,
    val items: List<Repo>, val filteredItems: List<Repo>,
)

// GOOD
data class SearchState(
    val query: String = "",
    val items: List<Repo> = emptyList(),
    val isLoading: Boolean = false,
    val hasError: Boolean = false,
) {
    val showEmpty: Boolean get() = query.isNotBlank() && !isLoading && !hasError && items.isEmpty()
}
```

- When states are mutually exclusive (loading, content, error), model them as a sealed type or enum
  instead of booleans; keep shared fields like `query` outside it.

### 3. The reducer is pure

Same state and action in, same state out. No IO, no clock, no random ids, no logging, no launching work.

```kotlin
// BAD: IO and a launched coroutine inside the reducer
fun reduce(state: SearchState, intent: SearchIntent): SearchState = when (intent) {
    is SearchIntent.QueryChanged -> {
        scope.launch { repository.search(intent.query) }
        state.copy(query = intent.query, isLoading = true)
    }
    ...
}

// GOOD: only computes the next state
fun reduce(state: SearchState, action: SearchAction): SearchState = when (action) {
    is SearchIntent.QueryChanged ->
        state.copy(query = action.query, isLoading = action.query.isNotBlank(), hasError = false)
    is SearchResult.Loaded ->
        if (action.query != state.query) state else state.copy(items = action.items, isLoading = false)
    ...
}
```

```swift
// GOOD: a static function on a value type; `inout` is equally pure for structs
enum SearchReducer {
    static func reduce(_ state: SearchState, _ action: SearchAction) -> SearchState {
        var state = state
        switch action {
        case .queryChanged(let query):
            state.query = query
            state.isLoading = !query.isEmpty
        case let .loaded(query, items):
            guard query == state.query else { return state }
            state.items = items
            state.isLoading = false
        // ...
        }
        return state
    }
}
```

- Kotlin: `MutableStateFlow.update` may run its lambda more than once under contention. A pure reducer
  makes that harmless; one with side effects would run them twice.
- Values the reducer needs from the outside world (current time, generated id) arrive inside the action.

### 4. Effects run outside the reducer and report back as actions

```kotlin
fun onIntent(intent: SearchIntent) {
    dispatch(intent)                                   // 1. reduce
    when (intent) {                                    // 2. start the effect for this intent
        is SearchIntent.QueryChanged -> search(intent.query, debounce = true)
        SearchIntent.RetryClicked -> search(state.value.query, debounce = false)
        is SearchIntent.ResultClicked -> _effects.trySend(SearchEffect.OpenDetails(intent.id))
    }
}

private fun dispatch(action: SearchAction) = _state.update { reduce(it, action) }

private fun search(query: String, debounce: Boolean) {
    searchJob?.cancel()
    if (query.isBlank()) return
    searchJob = viewModelScope.launch {
        if (debounce) delay(300)
        val result = try {
            SearchResult.Loaded(query, repository.search(query))
        } catch (e: IOException) {
            SearchResult.Failed(query)
        }
        dispatch(result)                               // 3. result goes back through the reducer
    }
}
```

- The effect never writes state directly. Every change is visible as an action in logs and tests.
- Swift: the store keeps a `Task` per effect and calls `send(.loaded(...))` when it finishes.
- Dart (Bloc): the handler awaits the repository, then `emit(reduce(state, result))`.

### 5. Effect concurrency is a decision, not an accident

| Policy | Use for | Kotlin | Swift | Dart (Bloc) |
|---|---|---|---|---|
| Cancel previous | Search, filters, latest-wins loads | `job?.cancel()` before `launch` | `task?.cancel()` before `Task {}` | `restartable()` |
| Drop new while busy | Submit, pay, pull to refresh | `if (job?.isActive == true) return` | `guard task == nil` | `droppable()` |
| Queue | Ordered writes, BLE command sequences | `Channel` + one consumer, or `Mutex` | `AsyncStream` + one consumer | `sequential()` |

- Results carry their input (query, page, request id); the reducer drops results that no longer match.
  Cancellation alone is not enough: a result can arrive between completion and cancel.
- Dart: after an `await` in a `restartable()` handler, check `emit.isDone` before doing more IO;
  cancellation stops `emit`, not your `Future`.

### 6. One-off effects: state first, channel when it is truly fire-and-forget

```kotlin
// GOOD (preferred): navigation as state, cleared by an intent after the UI acts
data class SearchState(val openDetailsId: String? = null, ...)

// ACCEPTABLE: effect channel, buffered, collected with the lifecycle on Main.immediate
private val _effects = Channel<SearchEffect>(Channel.BUFFERED)
val effects: Flow<SearchEffect> = _effects.receiveAsFlow()

// BAD: SharedFlow without replay loses effects while the UI is stopped or rotating
val effects = MutableSharedFlow<SearchEffect>()
```

```swift
// GOOD: SwiftUI navigation driven by state
.navigationDestination(item: Binding(
    get: { store.state.selectedRepo },
    set: { if $0 == nil { store.send(.detailsDismissed) } }
)) { id in
    RepoDetailView(id: id)
}
```

```dart
// GOOD: Bloc state field plus BlocListener with listenWhen
BlocListener<SearchBloc, SearchState>(
  listenWhen: (previous, current) => previous.selectedRepoId != current.selectedRepoId,
  listener: (context, state) { /* navigate, then add(const DetailsOpened()) */ },
  child: ...,
)
```

- A `Channel` keeps effects while nobody collects, but an effect can still be lost if the collector is
  cancelled between receive and handling. Collect on `Dispatchers.Main.immediate` inside
  `repeatOnLifecycle(STARTED)`; if losing one is unacceptable, use state.

### 7. The store is the only writer; the UI only renders and sends

```kotlin
// BAD: UI writes state and calls store internals, bypassing the reducer
viewModel.mutableState.value = state.copy(isLoading = true)
viewModel.searchNow("x")

// GOOD: one entry point
@Composable fun SearchScreen(state: SearchState, onIntent: (SearchIntent) -> Unit, modifier: Modifier = Modifier)
```

- Swift: `private(set) var state` on the store; the view calls `store.send(_:)`.
- Dart: widgets call `context.read<SearchBloc>().add(...)`; they never call `emit`.
- Text fields: reduce the text change synchronously on the main thread, otherwise the cursor jumps.

### 8. Keep state lean and render slices

Every action produces a new state and every observer compares it.

- `StateFlow` and Bloc skip equal states using `equals` / `==`; on large lists that comparison is O(n)
  per action. Keep big collections out of state that changes on every keystroke, or page them.
- Compose: pass each child only the fields it reads, not the whole `State`; with strong skipping,
  unchanged arguments let children skip.
- SwiftUI: `@Observable` tracks `store.state` as one property, so any change re-evaluates every reader.
  Pass child views plain values, or split rarely changing parts into separate store properties.
- Flutter: `BlocSelector` or `context.select` for slices; `buildWhen` on `BlocBuilder`.
- High-frequency streams (BLE notifications, sensor data) are sampled or throttled before they become
  actions; one action per packet will flood the reducer and the UI.

### 9. Test the reducer as a pure function, the store with fakes

```kotlin
@Test fun `stale result for an older query is ignored`() {
    val state = SearchState(query = "kotlin", isLoading = true)
    assertEquals(state, reduce(state, SearchResult.Loaded("kot", listOf(repo))))
}
```

```swift
@Test func queryChangeStartsLoading() {
    let next = SearchReducer.reduce(SearchState(hasError: true), .queryChanged("swift"))
    #expect(next == SearchState(query: "swift", isLoading: true))
}
```

```dart
test('failure for an old query is ignored', () {
  const state = SearchState(query: 'flutter', status: SearchStatus.loading);
  expect(reduce(state, const SearchFailed('flut')), state);
});
```

- Reducer tests: one test per transition, including the stale-result and no-op cases. No mocks.
- Store tests: fake repository, virtual time (`runTest`), Turbine for state and effect sequences,
  `bloc_test` for Blocs, `await store.send(...)?.value` for Swift stores.
- Assert whole states, not single fields, so unexpected changes fail the test.

### 10. Use the platform's established MVI tools when the team has them

- Swift: The Composable Architecture (TCA) gives reducers, effects, dependency injection and an exhaustive
  test store. Worth it for large apps that want enforced structure; it is a significant dependency with its
  own learning curve and API changes between versions. Follow its current documentation and do not mix
  it with hand-rolled stores inside one feature.
- Dart: `Bloc` for event-driven screens (named events, transformers, event traceability in `onTransition`);
  `Cubit` for simple screens, with methods instead of events and `emit` directly.

```dart
// Cubit: fine for a counter-sized screen
class FilterCubit extends Cubit<bool> {
  FilterCubit() : super(false);
  void toggle() => emit(!state);
}
```

## Anti-patterns

- Giant state: one `State` for a whole tab or app. Each screen owns its state; share data through
  repositories.
- Reducers doing IO, logging, reading the clock or generating ids.
- Effects writing state directly instead of returning a result action.
- Losing effects: `SharedFlow(replay = 0)`, collecting outside the lifecycle, or `trySend` on a full
  `RENDEZVOUS` channel without checking the result.
- State explosion: a sealed state per combination (`LoadingWithError`, `RefreshingEmpty`). Use a few
  orthogonal fields plus one sealed sub-state for truly exclusive cases.
- Over-engineering: intents, reducer, effects and a store for a settings toggle or a static detail page.
- Booleans that can contradict each other (`isLoading` and `hasError` both true with no meaning defined).
- One action per BLE packet or scroll pixel, flooding reducer and UI.
- A generic "base MVI" framework written in-house before two screens need it.
- Tests that mock the reducer or assert on private functions instead of states.

## Checklist

- [ ] The screen really needs MVI (interacting events, races or auditable transitions)
- [ ] Intents are one sealed type, named after user actions; results carry their input
- [ ] One immutable `State`, minimal, derived values computed
- [ ] Reducer is pure: no IO, clock, random, logging or launching
- [ ] Effects run outside the reducer and report back through actions
- [ ] Concurrency policy chosen per effect (cancel previous, drop, queue); stale results ignored
- [ ] One-off effects modelled as state, or a buffered channel collected with the lifecycle
- [ ] UI renders state and sends intents only; children receive slices
- [ ] High-frequency inputs throttled before they become actions
- [ ] Reducer tests per transition; store tests with fakes and virtual time; existing tests pass

## Related skills

- `mobile-mvvm` -- the simpler default for screens that do not need a reducer
- `mobile-mvc` -- legacy UIKit and Activity-centric screens
- `mobile-design-patterns` -- state, command and observer patterns behind MVI
- `mobile-kotlin`, `mobile-swift`, `mobile-flutter` -- language rules for each platform
- `mobile-code-review` -- reviewing stores, reducers and effects
- `mobile-testing` -- where reducer and store tests sit in the overall test strategy
- `mobile-kmp` -- sharing a store between Android and iOS
