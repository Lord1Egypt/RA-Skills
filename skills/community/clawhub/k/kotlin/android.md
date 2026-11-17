# Android — Lifecycle, ViewModel, And Process Death

Android's failure modes are all about *when* code runs relative to a lifecycle you do not control: rotation, backgrounding, process death, and the return trip. Compose-specific state and recomposition live in the Compose guide; this file is the host lifecycle underneath it.

`ui_toolkit` selects the UI layer these examples assume: `compose` (the default) keeps screen state in composables and this file supplies the lifecycle around them; `views` makes the ViewBinding and lifecycle-callback patterns below the primary path; `none` leaves only the lifecycle, scope and process-death rules.

## Symptom → Cause

| Symptom | Cause | Fix |
|---|---|---|
| Crash on rotation with "Fragment not attached" | Work started in a scope that outlived the view, then touched `requireContext()` | Collect in `viewLifecycleOwner.lifecycleScope` with `repeatOnLifecycle` |
| Data reloads on every rotation | State held in the Activity/Fragment, not in a ViewModel | Hoist to a ViewModel; it survives configuration changes |
| State lost after the app was backgrounded for a while | Process death, not a configuration change | `SavedStateHandle` for the small identifying state |
| Memory leak reported for an Activity | A long-lived object holds a `Context`, a `View`, or a listener | Application context, weak reference, or unregister in the teardown callback |
| Flow collection continues while the screen is invisible | Collection tied to `lifecycleScope` alone | `repeatOnLifecycle(Lifecycle.State.STARTED)` |
| `TransactionTooLargeException` | Saved state exceeded the Binder transaction budget (1 MB per process, shared across all in-flight transactions) | Save ids, not objects; keep payloads in a repository or on disk |
| Work never finishes when the app is backgrounded | A coroutine scope died with the UI | `WorkManager` for anything that must survive the process |
| Double-triggered navigation after rotation | A one-shot event replayed to the new collector | Consume-once event carrier (SKILL.md Concurrency Primitive Selection) |

## The Three Lifetimes

| Survives | Configuration change | Process death | Owner |
|---|---|---|---|
| `remember` / local field | No | No | Composition or Activity instance |
| ViewModel + `viewModelScope` | Yes | No | ViewModel store |
| `SavedStateHandle` / `onSaveInstanceState` | Yes | Yes (size-limited) | System bundle |
| Repository cache, DataStore, database, `WorkManager` | Yes | Yes | Application / disk |

Design rule: identity and navigation arguments go in `SavedStateHandle`; derived or fetchable data goes in a repository and is re-fetched from that identity. Restoring 200 KB of list content through the bundle is how apps hit the Binder limit.

## Collecting Flows Safely

- `repeatOnLifecycle(STARTED)` inside `lifecycleScope.launch` cancels collection at STOP and restarts it at START. This is the default for a Fragment or Activity.
- `flowWithLifecycle(lifecycle, STARTED)` is the single-flow shorthand; the `repeatOnLifecycle` block is better when you collect several flows, because one block covers them all.
- `launchWhenStarted` and friends are deprecated: they *suspend* the coroutine instead of cancelling it, so the upstream producer keeps running and buffering.
- In a Fragment, use `viewLifecycleOwner.lifecycleScope`, not `lifecycleScope` — the Fragment outlives its view on back-stack navigation, and the difference is exactly where the "detached view" crashes come from.
- Cold-flow upstreams keep restarting with the lifecycle; if the query is expensive, share it in the ViewModel with `stateIn` so only the collection restarts, not the work.

## ViewModel

- `viewModelScope` cancels in `onCleared()`. Anything that must outlive the screen (an upload, a purchase confirmation) does not belong in it — that is `WorkManager` or an application-scoped component.
- Expose one immutable UI state per screen: `val state: StateFlow<UiState>` backed by a private `MutableStateFlow`, updated with `update { it.copy(...) }` (SKILL.md rule 6).
- Never hold a `Context`, `Activity`, `View`, `Fragment` or navigation controller in a ViewModel. Application context via `AndroidViewModel` when unavoidable; a resource-provider interface is the testable version.
- `SavedStateHandle` is injectable and behaves like a `Map` with flow support (`getStateFlow(key, default)`); it is also how a navigation argument arrives.
- One ViewModel per screen, not per app. A shared, activity-scoped ViewModel is a deliberate choice for a multi-step flow, and it must be cleared when the flow ends.
- Do not start work in the `init` block if the screen may never display it: `init` runs when the ViewModel is created, which is before the first frame and outside any user intent.

## Context And Leaks

- Application context for anything long-lived (singletons, DI graph, DataStore); Activity context only for UI, themes and dialogs.
- Registered listeners, `BroadcastReceiver`s, sensors, callbacks and `Handler` messages must be unregistered in the mirroring lifecycle callback — one registration without its teardown leaks the whole view hierarchy.
- Anonymous inner classes and non-static inner classes capture their outer instance implicitly: a long-lived callback declared inline in an Activity pins that Activity.
- Coroutines started in an Activity-owned scope keep captured views alive until they finish; cancellation is what releases them.
- LeakCanary in debug builds gives the retention chain — the leak is almost always the last object in that chain that you registered by hand.

## Views, Bindings, Resources

- A `ViewBinding` reference in a Fragment must be nulled in `onDestroyView`; the standard pattern is a private nullable backing field plus a non-null accessor that throws with a clear message.
- `findViewById` and binding lookups return views tied to the current view tree — caching one across `onCreateView` calls is a stale reference to a destroyed hierarchy.
- Configuration-dependent resources (dimensions, strings, colors) must be resolved when they are used, not stored at construction — the values change on rotation, locale change and theme change.

## Background Work Boundaries

| Need | Mechanism |
|---|---|
| Work tied to a visible screen | `viewModelScope` / `lifecycleScope` |
| Must complete even if the user leaves | `WorkManager` (persisted, constraint-aware, retried) |
| Long-running with a visible notification | Foreground service |
| Exact time | `AlarmManager` (with its exact-alarm permission constraints) |
| Periodic sync | `WorkManager` periodic request, minimum interval 15 minutes |

Background execution limits mean a plain coroutine in a backgrounded process can be killed at any moment: if losing the work is unacceptable, it must be persisted before it starts.

## Testing On Android

- ViewModel tests need the Main dispatcher replaced (`Dispatchers.setMain`) and reset afterwards; a missing reset is why a suite fails while each test passes alone.
- `InstantTaskExecutorRule` for LiveData; for `StateFlow`, collect into a list on a background test coroutine instead of asserting `.value`.
- Lifecycle behaviour (`repeatOnLifecycle`, `SavedStateHandle` restoration) is testable without a device: `TestLifecycleOwner` and constructing `SavedStateHandle(mapOf(...))` directly.
- Process death is reproducible: background the app, terminate the process from the tooling, then return through the launcher — not by rotating the device, which only tests the configuration-change path.

## Review Checklist

- Every flow collection in a view is lifecycle-aware, and Fragments use `viewLifecycleOwner`.
- No `Context`, `View` or navigation reference stored in a ViewModel.
- Everything needed to rebuild the screen after process death is in `SavedStateHandle`, and nothing large is.
- Every registration has a matching unregistration in the mirroring callback.
- Work that must survive the screen runs in `WorkManager`, not in a UI-owned scope.
