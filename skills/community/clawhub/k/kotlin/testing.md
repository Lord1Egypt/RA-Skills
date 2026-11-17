# Testing — Virtual Time, Flows, And Final Classes

Kotlin's two testing-specific problems: coroutines make time and threading part of the test, and classes are final by default so the mocking habits from Java do not transfer.

## Symptom → Cause

| Symptom | Cause | Fix |
|---|---|---|
| Test hangs, then fails on a timeout | Real dispatcher inside `runTest`, or a `StateFlow` collected with a terminal operator that never completes | Inject the test dispatcher; use `take(n).toList()` or a background collector |
| Passes alone, fails in the suite | `Dispatchers.setMain` never reset | `Dispatchers.resetMain()` in teardown, or a shared JUnit rule |
| Assertions run before the coroutine did | Work scheduled on `StandardTestDispatcher` and never advanced | `advanceUntilIdle()`, or `UnconfinedTestDispatcher` for eager execution |
| Flaky by timing | A real `delay`, a real thread, or a wall-clock assertion | Virtual time only; inject a clock |
| "Module with the Main dispatcher had failed to initialize" | Android Main dispatcher on a JVM unit test | `Dispatchers.setMain(StandardTestDispatcher())` |
| Mock fails: "cannot mock final class" | Kotlin classes are final | MockK, or a hand-written fake against an interface |
| Test sees only the last state | `StateFlow` conflation dropped the intermediates (SKILL.md rule 6) | Collect into a list from a background coroutine before acting |
| `runTest` finishes but a launched coroutine never ran | The coroutine was started in a scope outside the test's | Use `backgroundScope`, or the injected scope |

## runTest And Virtual Time

- `runTest { }` runs the body on a `TestScope` with a virtual clock: `delay(10.minutes)` returns immediately, and the total wall time is the CPU work only.
- It waits for the coroutines of its own scope to finish and fails on a timeout (60 seconds by default in kotlinx-coroutines-test; override with `runTest(timeout = …)`). A hang almost always means a real dispatcher slipped in.
- `backgroundScope` inside `runTest` is for collectors and services that never complete: they are cancelled when the test body ends, instead of hanging it.
- Dispatcher choice inside the test:
  - `StandardTestDispatcher` — queues coroutines; nothing runs until you `advanceUntilIdle()`, `runCurrent()` or `advanceTimeBy(n)`. Use it when the ordering *is* the thing under test.
  - `UnconfinedTestDispatcher` — runs eagerly to the first suspension. Use it when you only care about the end state; it makes most ViewModel tests read straightforwardly.
- `advanceTimeBy(n)` executes everything scheduled strictly before `now + n`; a task scheduled at exactly `now + n` is still pending — follow with `runCurrent()` when a boundary matters.
- Never mix real and virtual time: one `Thread.sleep`, one `withContext(Dispatchers.IO)` on a real dispatcher, and the virtual clock no longer describes the test.

## Injecting Dispatchers

```kotlin
class UserViewModel(private val io: CoroutineDispatcher = Dispatchers.IO) { … }

// test
val vm = UserViewModel(StandardTestDispatcher(testScheduler))
```

- Passing `testScheduler` (from `runTest`'s scope) into every constructed dispatcher keeps all of them on the same virtual clock — dispatchers created with different schedulers deadlock waiting for each other.
- For `viewModelScope` and any other framework-owned scope, the only entry point is `Dispatchers.setMain(...)` in setup and `Dispatchers.resetMain()` in teardown. Put both in one rule/extension and apply it everywhere; the missing reset is the single most common cause of suite-order flakiness.
- An interface (`DispatcherProvider`) beats four constructor parameters once a class needs more than one dispatcher.

## Testing Flows

- The three shapes, from most to least precise:
  1. Turbine-style: `flow.test { assertEquals(Loading, awaitItem()); … awaitComplete() }` — asserts the sequence and fails on unconsumed events.
  2. Manual background collection: `val seen = mutableListOf<S>(); backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) { flow.toList(seen) }` — then act and assert on `seen`.
  3. `flow.take(n).toList()` — fine for a cold flow with a known number of emissions, useless for a `StateFlow` (it never completes).
- A `StateFlow` produced with `stateIn(WhileSubscribed())` emits nothing until it has a subscriber: a test that only reads `.value` sees the initial value forever.
- Conflation means intermediate states may legitimately never be emitted. Assert on the states that must be observable, not on an exact count, unless the count is the contract.
- Turn a hot flow into a testable one by injecting the source (a `MutableSharedFlow` fake repository) rather than by mocking operators.

## Mocks, Fakes, And Final Classes

- Kotlin classes and members are final unless `open`. Mockito needs the inline mock maker to touch them; MockK handles Kotlin natively (`mockk`, `every`, `coEvery` for suspend functions, `mockkStatic`/`mockkObject` for top-level and `object` members).
- Prefer a fake: a small class implementing the interface with a `MutableStateFlow` inside is faster, survives refactors, and reads like the production collaborator. Reach for a mock when you must *verify an interaction* with a dependency you do not own.
- Mocking a data class or a value class is a smell — construct the real one.
- `mockkStatic` and `mockkObject` are global state: unmock them in teardown or the next test inherits them.
- Relaxed mocks (`mockk(relaxed = true)`) hide missing stubs and make a failing test pass with default values; use them for wide interfaces you barely touch, never for the collaborator under test.

## Test Structure

- One behaviour per test, and a name that states it: `` fun `emits Locked when the account is disabled`() `` — backticked names are the one place Kotlin allows prose.
- JUnit4 vs JUnit5: JUnit5 gives `@Nested`, parameterized tests and extensions; JUnit4 is still the Android instrumentation default. Do not mix runners in one module without a reason.
- Fixture construction: default arguments on a factory (`fun user(id: String = "1", name: String = "x") = User(id, name)`) beat builders and beat repeating full constructors — the test then states only what matters to it.
- Assertion libraries (Truth, AssertK, Strikt, Kotest matchers) exist for the failure message: `assertThat(list).containsExactly(a, b)` prints both sides, `assertTrue(list == …)` prints "expected true".
- Property-based tests (Kotest) pay off on pure functions with algebraic properties: parsers, comparators, serializers, arithmetic.
- Coverage of a suspend function that only forwards to a repository proves nothing. Test the decisions: branch selection, error mapping, state transitions, cancellation behaviour.

## Testing Cancellation And Timeouts

- Cancellation is a behaviour worth asserting: launch the work in a `TestScope` job, `advanceTimeBy` past a checkpoint, `job.cancelAndJoin()`, then assert the cleanup ran (a flag set in `finally`).
- A test that a timeout fires: `withTimeout` inside virtual time is instantaneous — `advanceTimeBy(timeout + 1)` and expect `TimeoutCancellationException`.
- A function that ignores cancellation (no suspension point in its loop) will not stop in a test either — that is the test that catches SKILL.md rule 4 violations.

## Review Checklist

- No real dispatcher, real `sleep`, or wall-clock read inside a unit test.
- `Dispatchers.setMain`/`resetMain` paired in a shared rule.
- Flow assertions cover the sequence, not just the final value.
- Fakes for owned interfaces; mocks only for interaction verification with foreign code.
- Every `mockkStatic`/`mockkObject` unwound in teardown.
- Cancellation and error paths tested, not only the happy path.
