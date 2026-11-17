# Jetpack Compose reference

Load this when writing or changing composables, screen state wiring, effects, lists or previews.

## Screen and content split

```kotlin
@Composable
fun DevicesRoute(
    onOpenDevice: (DeviceId) -> Unit,
    viewModel: DevicesViewModel = hiltViewModel(),
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    DevicesScreen(
        state = state,
        onQueryChange = viewModel::onQueryChange,
        onDeviceClick = onOpenDevice,
    )
}

@Composable
fun DevicesScreen(
    state: DevicesUiState,
    onQueryChange: (String) -> Unit,
    onDeviceClick: (DeviceId) -> Unit,
    modifier: Modifier = Modifier,
) { /* pure UI, previewable, testable without a ViewModel */ }
```

- The route composable is the only one that knows about the ViewModel and navigation.
- Parameter order: required data, event lambdas, `modifier`, other optional parameters, trailing content
  lambda.
- Event lambdas are named for what happened (`onDeviceClick`), not what the parent will do.

## State

| Need | API |
|---|---|
| Survive recomposition | `remember { }` |
| Survive rotation and process death | `rememberSaveable { }` (Bundle-able types, `@Parcelize`, or a `Saver`) |
| Value computed from other state that changes less often than its inputs | `remember { derivedStateOf { } }` |
| Recompute when an input changes | `remember(input) { }` |
| Turn Compose state into a Flow | `snapshotFlow { }` |
| Load into state from a suspend source | `produceState` |

```kotlin
// BAD: recomposes on every scroll pixel
val showButton = listState.firstVisibleItemIndex > 0

// GOOD: recomposes only when the boolean flips
val showButton by remember { derivedStateOf { listState.firstVisibleItemIndex > 0 } }

// BAD: derivedStateOf adds overhead, output changes as often as input
val fullName by remember { derivedStateOf { "$first $last" } }

// GOOD
val fullName = "$first $last"
```

- `remember` keys include every input of the calculation, or the cached value goes stale.
- Read fast-changing state as late as possible: lambda modifiers (`Modifier.offset { }`,
  `Modifier.graphicsLayer { }`, `drawBehind { }`) read in layout or draw, skipping composition.

## Stability and skipping

- Strong skipping is on by default since Kotlin 2.0.20. Restartable composables skip when every argument
  is equal: stable types by `equals`, unstable types by instance (`===`).
- Lambdas are remembered automatically under strong skipping. Do not wrap them in `remember` by hand.
- What still breaks skipping: creating new list or object instances on every emission or recomposition,
  and mapping inside the composable body.

```kotlin
// BAD: new list each recomposition, child never skips
DeviceList(devices = state.devices.filter { it.online })

// GOOD: filter in the ViewModel, pass an ImmutableList
DeviceList(devices = state.onlineDevices)
```

- `kotlinx.collections.immutable`: `ImmutableList`, `persistentListOf()`, `toImmutableList()`.
- `@Immutable`: all public properties are `val` and deeply immutable.
- `@Stable`: mutable, but changes are observable through Compose state and `equals` is consistent.
- Types from modules without the Compose compiler (domain, third-party) are unstable. Either map to a UI
  model in the UI module or list them in a stability configuration file in the `composeCompiler {}` block.
- Measure before optimizing: Layout Inspector recomposition counts and the compiler reports
  (`composeCompiler { reportsDestination = ...; metricsDestination = ... }`).

## Side effects

| API | Use |
|---|---|
| `LaunchedEffect(key)` | Suspend work tied to composition, restarted when keys change |
| `rememberCoroutineScope()` | Launch from event callbacks (click, swipe) |
| `DisposableEffect(key)` | Register and unregister listeners, observers, callbacks |
| `rememberUpdatedState(value)` | Latest value inside a long-lived effect without restarting it |
| `SideEffect` | Publish Compose state to non-Compose code after every successful recomposition |
| `LifecycleStartEffect`, `LifecycleResumeEffect` | Work paired with lifecycle start/stop or resume/pause |

```kotlin
@Composable
fun ConnectionObserver(deviceId: DeviceId, onStateChange: (LinkState) -> Unit) {
    val currentOnStateChange by rememberUpdatedState(onStateChange)
    val monitor = LocalLinkMonitor.current
    DisposableEffect(deviceId, monitor) {
        val listener = LinkListener { currentOnStateChange(it) }
        monitor.register(deviceId, listener)
        onDispose { monitor.unregister(deviceId, listener) }
    }
}
```

- Never call ViewModel functions, start navigation or log analytics directly in the composable body.
- `LaunchedEffect(Unit)` and `LaunchedEffect(true)` are only correct when the effect reads nothing that
  can change.

## Lazy lists

```kotlin
LazyColumn(
    modifier = modifier,
    contentPadding = contentPadding,
) {
    item(key = "header", contentType = "header") { Header() }
    items(
        items = state.messages,
        key = { it.id.value },
        contentType = { it.kind },
    ) { message ->
        MessageRow(message, Modifier.animateItem())
    }
}
```

- `key` is stable and unique (database or server id, never index). It preserves item state and scroll
  position across updates.
- `contentType` lets the list reuse compositions between rows of the same type.
- Keys must be Bundle-able types (String, Int, Long, Parcelable) if they are saved with the list state.
- No nested scrollable in the same direction without a fixed height.

## Modifiers

- Modifier order matters: `Modifier.padding(16.dp).clickable { }` has a smaller touch area than
  `Modifier.clickable { }.padding(16.dp)`.
- Apply the incoming `modifier` once, to the root, first in the chain:
  `modifier.fillMaxWidth().padding(...)`.
- Do not create `Modifier` chains in a loop body when they are constant; hoist them.

## Accessibility and semantics

```kotlin
// BAD: tappable icon, no label, 24dp target
Icon(Icons.Default.Refresh, null, Modifier.clickable { onRefresh() })

// GOOD
IconButton(onClick = onRefresh) {
    Icon(Icons.Default.Refresh, contentDescription = stringResource(R.string.refresh))
}
```

- `Modifier.semantics(mergeDescendants = true) { }` for rows read as one item.
- `Modifier.testTag("...")` only where text or content description cannot identify a node.
- Text sizes in `sp`, no fixed heights on text containers.

## Previews

```kotlin
@PreviewLightDark
@PreviewFontScale
@Composable
private fun DevicesScreenPreview(
    @PreviewParameter(DevicesStateProvider::class) state: DevicesUiState,
) {
    AppTheme { DevicesScreen(state = state, onQueryChange = {}, onDeviceClick = {}) }
}
```

- Previews take state, not a ViewModel. If a screen cannot be previewed, it is doing too much.
- Keep previews `private` and in the same file or a `debug` source set.

## Navigation

- Pass IDs between destinations, never whole objects. Load the object in the destination ViewModel.
- Navigation callbacks are lambdas from the route composable. Screens do not hold a `NavController`.
- With Navigation 3, the back stack is state the app owns; with Navigation 2.8+, routes are type-safe
  `@Serializable` classes and the ViewModel reads arguments from `SavedStateHandle`.
