# State management reference

Load this when writing or changing providers, notifiers, blocs or cubits. Examples target Riverpod 3
and flutter_bloc 9. Pick one approach per app and follow what `pubspec.yaml` already uses.

## Choosing

| Need | Riverpod | Bloc |
|---|---|---|
| Dependency injection built in | Yes, providers are the DI graph | No, pair with `RepositoryProvider` or get_it |
| Async loading, error, data | `AsyncNotifier` and `AsyncValue` | Your own sealed state classes |
| Event debounce, cancel previous | Manual | `transformer:` with `bloc_concurrency` |
| Strict event log and replay | No | Yes, every change starts from an event |
| Boilerplate | Low, lower with codegen | Medium |

Both work. Switching mid-project costs more than either choice.

## Riverpod

### Provider types

| Type | Use for |
|---|---|
| `Provider` | Dependencies: repositories, API clients, config |
| `NotifierProvider` | Synchronous state with methods |
| `AsyncNotifierProvider` | State loaded asynchronously, with methods to change it |
| `FutureProvider` / `StreamProvider` | Read-only async values without methods |

### AsyncNotifier

```dart
final todosProvider =
    AsyncNotifierProvider.autoDispose<TodosNotifier, List<Todo>>(TodosNotifier.new);

class TodosNotifier extends AsyncNotifier<List<Todo>> {
  @override
  Future<List<Todo>> build() => ref.watch(todoRepositoryProvider).fetch();

  Future<void> add(Todo todo) async {
    final repo = ref.read(todoRepositoryProvider);
    state = const AsyncLoading();
    final result = await AsyncValue.guard(() async {
      await repo.add(todo);
      return repo.fetch();
    });
    if (!ref.mounted) return; // provider disposed while awaiting
    state = result;
  }
}
```

- `build` uses `ref.watch` for dependencies so the notifier rebuilds when they change.
- Methods use `ref.read`. Never `ref.watch` inside a method.
- `AsyncValue.guard` turns exceptions into `AsyncError` instead of try/catch boilerplate.

### Consuming

```dart
class TodosScreen extends ConsumerWidget {
  const TodosScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.listen(todosProvider, (previous, next) {
      if (next case AsyncError(:final error)) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$error')));
      }
    });

    return switch (ref.watch(todosProvider)) {
      AsyncData(:final value) => TodoList(todos: value),
      AsyncError(:final error) => ErrorView(error: error),
      _ => const Center(child: CircularProgressIndicator()),
    };
  }
}
```

| Call | Where | Effect |
|---|---|---|
| `ref.watch(p)` | `build` of widgets and providers | Rebuilds when `p` changes |
| `ref.watch(p.select((s) => s.x))` | `build` | Rebuilds only when `x` changes |
| `ref.read(p)` / `ref.read(p.notifier)` | Callbacks, notifier methods | One-off read, no subscription |
| `ref.listen(p, cb)` | `build` or notifier `build` | Side effects: snackbar, navigation, analytics |

- `ConsumerStatefulWidget` when the widget also owns controllers; `ref` is available on the State.
- Use the `_ =>` branch for `AsyncValue` loading only. Data and error are matched explicitly.

### Lifetime

```dart
// BAD: screen state kept forever, stale data on the next visit
final searchProvider = NotifierProvider<SearchNotifier, SearchState>(SearchNotifier.new);

// GOOD: disposed when the last listener goes away
final searchProvider =
    NotifierProvider.autoDispose<SearchNotifier, SearchState>(SearchNotifier.new);
```

- Generated providers (`@riverpod`) are auto-dispose by default; `@Riverpod(keepAlive: true)` opts out.
- Keep a provider alive conditionally with `final link = ref.keepAlive();` and `link.close()` later.
- Clean up in `ref.onDispose(...)`: close sockets, cancel timers, stop BLE scans.

### Parameters (family)

```dart
final deviceProvider = AsyncNotifierProvider.autoDispose
    .family<DeviceNotifier, Device, DeviceId>(DeviceNotifier.new);

class DeviceNotifier extends AsyncNotifier<Device> {
  DeviceNotifier(this.id);
  final DeviceId id;

  @override
  Future<Device> build() => ref.watch(deviceRepositoryProvider).byId(id);
}

// usage
ref.watch(deviceProvider(DeviceId('A1')));
```

- The parameter needs value equality (`==` and `hashCode`). Records, extension types over `String`
  and `int`, and `final class` with `==` work. A new `List` each build creates a new provider each build.

## Bloc

### Cubit or Bloc

```dart
// Cubit: methods emit states directly
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);
  void increment() => emit(state + 1);
}

// Bloc: events in, states out, with concurrency control
class SearchBloc extends Bloc<SearchEvent, SearchState> {
  SearchBloc(this._api) : super(SearchIdle()) {
    on<QueryChanged>(_onQueryChanged, transformer: restartable());
  }
  final SearchApi _api;

  Future<void> _onQueryChanged(QueryChanged event, Emitter<SearchState> emit) async {
    emit(SearchLoading());
    try {
      emit(SearchResults(await _api.search(event.query)));
    } on Exception {
      emit(SearchFailure());
    }
  }
}
```

- `bloc_concurrency` transformers: `restartable()` (search as you type), `droppable()` (ignore taps while
  busy), `sequential()` (queue writes). Default is concurrent.
- Streams inside a handler: `await emit.forEach(stream, onData: (v) => State(v));`. It cancels when the
  bloc closes. Do not `listen` manually in the constructor.
- Cubit methods that await check `if (isClosed) return;` before `emit`. Emitting after close throws.

### State equality

```dart
// BAD: list mutated in place, new state == old state, nothing rebuilds
state.items.add(item);
emit(state);

// GOOD: new immutable state
emit(state.copyWith(items: [...state.items, item]));
```

- Bloc skips a state equal (`==`) to the current one. Give states value equality (`equatable`,
  `freezed` or hand-written `==`) and never mutate them.

### Widgets

| Widget | Use for |
|---|---|
| `BlocProvider(create: ...)` | Creates and closes the bloc with the subtree |
| `BlocProvider.value(value: ...)` | Passes an existing bloc; does not close it |
| `BlocBuilder` | Builds UI from state; pure, no side effects |
| `BlocSelector` / `context.select` | Rebuilds only when a derived value changes |
| `BlocListener` | Side effects: navigation, snackbars, dialogs |
| `BlocConsumer` | Builder and listener on the same bloc |

```dart
// BAD: bloc created with .value inside build, never closed
BlocProvider.value(value: SearchBloc(api), child: const SearchView());

// GOOD
BlocProvider(create: (_) => SearchBloc(api), child: const SearchView());
```

- `context.read<T>()` in callbacks, `context.watch<T>()` or `context.select` in `build`. Same rule as Riverpod.
- Pass `listenWhen` and `buildWhen` to cut noise instead of filtering inside the callback.

## Both

- State classes are immutable. Use `final` fields and `copyWith`.
- Notifiers and blocs never hold `BuildContext`, widgets, controllers or `GlobalKey`s.
- Navigation is a side effect: trigger it from `ref.listen` or `BlocListener`, not from the notifier.
- Repositories are injected so tests can replace them. See [testing](testing.md).
