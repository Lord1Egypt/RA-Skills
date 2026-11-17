# Compose — State, Recomposition, And Why It Redraws

Compose reruns composables whose observed state changed. Almost every Compose bug is one of: state stored in the wrong place, state read too early, an unstable parameter defeating skipping, or a side effect running on every recomposition.

`ui_toolkit = compose` (the default) is what routes Android UI questions to this file; under `views` the same state and lifecycle problems are answered with ViewBinding and lifecycle callbacks instead, and nothing in this file applies.

## Symptom → Cause

| Symptom | Cause | Fix |
|---|---|---|
| State resets on rotation | `remember` only survives recomposition | `rememberSaveable`, or hoist into a ViewModel |
| State resets when scrolling a lazy list | The item left composition, taking its `remember` with it | Hoist the state out of the item, keyed by the item's id |
| Whole screen recomposes on every keystroke | State read at a level higher than it is used | Read the state as deep as possible; pass lambdas, not values |
| A composable never skips | An unstable parameter (mutable class, `List`, lambda recreated each time) | Stable types, `remember`ed lambdas, or an immutable collection |
| Infinite recomposition loop | State written during composition | Move the write into `LaunchedEffect` or an event callback |
| `LaunchedEffect` reruns unexpectedly | An unstable or changing key | Key on identity (`id`), not on the whole object |
| Effect uses a stale value | The lambda captured the value at launch | `rememberUpdatedState` for values a long-lived effect reads |
| List scroll janks and items flicker | No `key` in the lazy list; items re-created on every change | `items(list, key = { it.id })` |
| Crash: "Vertically scrollable component was measured with an infinite maximum height" | A vertical scroller nested inside another vertical scroller | One scrolling container per axis; use a lazy list's own item slots |
| Text field lags behind typing | State round-tripping through an async layer before returning | Keep the field state local and synchronous, sync outward on debounce |

## Where State Lives

| Scope | API | Survives |
|---|---|---|
| One composition | `remember { }` | Recomposition |
| One screen instance | `rememberSaveable { }` | Recomposition + configuration change; goes through the saved-state bundle, so keep it to ids and small values |
| Screen logic | ViewModel `StateFlow` + `collectAsStateWithLifecycle()` | Configuration change; not process death by itself |
| App | Repository, DataStore, database | Process death |

- Hoist state to the lowest common ancestor of the composables that read *and* write it; below that, pass a value plus an `onValueChange` lambda.
- `rememberSaveable` stores through the saved-instance bundle, so the value must be `Parcelable`, `Serializable`, or come with a custom `Saver`. Big objects here are how a screen hits `TransactionTooLargeException`.
- `remember(key1, key2) { }` recomputes when a key changes — that is the correct way to reset derived local state when the input identity changes.
- `mutableStateListOf` / `mutableStateMapOf` track *internal* mutations; `mutableStateOf(mutableListOf())` does not — adding an element mutates the same instance, the state's `equals` sees no change, and nothing recomposes.
- `derivedStateOf { }` for state computed from other state that changes far more often than the result does (a scroll offset feeding a boolean "is scrolled"). Used everywhere else it is overhead.
- `by` delegation (`var text by remember { mutableStateOf("") }`) reads better than `.value`; both do the same snapshot read.

## Recomposition And Skipping

- A composable is skipped when all of its parameters are *stable and unchanged*. Stable means: the type tells Compose that `equals` is reliable and public properties do not change without notifying the snapshot system.
- Stable by default: primitives, `String`, function types, `@Immutable`/`@Stable` annotated types, and classes with only `val` properties of stable types.
- Unstable by default: interfaces (`List`, `Map`, `Set` — the runtime instance may be mutable), classes with `var` properties, and any class from a module compiled without the Compose compiler.
- Strong skipping (on by default in the Compose compiler plugin shipped with Kotlin >=2.0.20) memoizes lambdas automatically and compares unstable parameters by instance equality — many older "wrap it in `remember`" workarounds are obsolete on that floor, so verify against `kotlin_floor` before recommending them.
- The evidence, not the guess: enable the compiler's stability report or run the layout inspector's recomposition counts. Optimizing a composable that already skips is churn.
- Defer state reads: `Modifier.offset { IntOffset(x, 0) }` (lambda, read at layout) instead of `Modifier.offset(x.dp)` (read at composition) moves the invalidation from recomposition to layout, which is a phase cheaper.
- Passing a lambda that captures changing state makes the child recompose; passing a stable method reference or a `remember`ed lambda does not.

## Side Effects

| API | Runs | Use for |
|---|---|---|
| `LaunchedEffect(key)` | On first composition and whenever a key changes; cancelled on leaving | Suspend work tied to the composable: loading, animation, snackbars |
| `DisposableEffect(key)` | Same lifecycle, with an `onDispose` block | Registering and unregistering listeners |
| `SideEffect { }` | After every successful composition | Publishing state to a non-Compose object |
| `rememberCoroutineScope()` | Scope tied to the composition, launched from callbacks | Work started by a user event, not by composition |
| `produceState(initial)` | Converts a non-Compose async source into state | Bridging callbacks into `State<T>` |
| `snapshotFlow { }` | Converts a snapshot read into a `Flow` | Reacting to scroll position or field content with flow operators |
| `rememberUpdatedState(v)` | Keeps a long-lived effect reading the latest value | Timeouts and callbacks that outlive the value they close over |

- `LaunchedEffect(Unit)` means "once per composition entry". Anything else in the key position is a restart trigger — pass ids, not objects whose `equals` you have not checked.
- Never launch work from the composable body directly: the body may run several times per frame, and there is nothing to cancel it.
- Reading state in a callback (`onClick`) is not a composition read, so it does not cause recomposition — that is the intended place for "current value at click time".

## Lists And Layout

- `LazyColumn`/`LazyRow` compose only visible items. Give `items(list, key = { it.id })` so state and animations follow the item across reorders and deletions.
- `contentType` on heterogeneous lists lets Compose reuse the right kind of item, cutting composition cost on scroll.
- Nesting a `LazyColumn` inside a `Column` with `verticalScroll` throws: the outer container offers infinite height. Use one lazy container with `item { }` slots for the header and footer.
- `Modifier` order is evaluation order: `padding` before `background` paints a smaller background than `background` before `padding`. Both compile.
- A `Modifier` built inline is a new object per recomposition; hoist constant modifier chains into a top-level `val`.
- Custom layouts and `SubcomposeLayout` are expensive by construction — measure twice before using subcomposition for a problem an intrinsic measurement could solve.

## Integration With ViewModel State

- `collectAsStateWithLifecycle()` (lifecycle-runtime-compose) stops collection when the screen is not started; `collectAsState()` keeps collecting in the background. Use the lifecycle-aware one for anything backed by a data source.
- One state object per screen beats a dozen individual `StateFlow`s: it makes impossible combinations unrepresentable and gives Compose one comparison instead of many.
- One-shot effects (navigation, snackbars) do not belong in the state stream without a consume-once mechanism (SKILL.md Concurrency Primitive Selection).
- Preview functions must not depend on a ViewModel: take the state as a parameter, and let the screen-level composable do the wiring. That split is also what makes the composable testable.

## Review Checklist

- Every `remember` that must survive rotation is a `rememberSaveable` or lives in a ViewModel.
- No state written during composition; every write is in an effect or a callback.
- Every lazy list has a stable `key`.
- Every `LaunchedEffect`/`DisposableEffect` key is deliberate, and every `DisposableEffect` has a real `onDispose`.
- Collections in composable parameters are immutable types, or the module is on a strong-skipping compiler floor.
- Skipping claims backed by a stability report or recomposition counts, not by inspection.
