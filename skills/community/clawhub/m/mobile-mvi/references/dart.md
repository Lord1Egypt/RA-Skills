# MVI with Dart, Flutter and Bloc

Load this when building or reviewing a Bloc or Cubit feature. Assumes Dart 3, Flutter stable, `bloc`,
`flutter_bloc`, `bloc_concurrency`, `equatable`, and `bloc_test` in tests.

Bloc maps onto MVI directly: events are intents, the handler runs effects, `emit` publishes the next state.
To keep the reducer pure, handlers call a top-level `reduce` function and do IO only around it.

The feature: repository search with debounce, latest-query-wins, retry, and navigation to details
driven by state.

## Contract

```dart
class Repo extends Equatable {
  const Repo({required this.id, required this.name});

  final String id;
  final String name;

  @override
  List<Object?> get props => [id, name];
}

class SearchException implements Exception {}

abstract interface class RepoRepository {
  Future<List<Repo>> search(String query);
}
```

## Actions and state

```dart
sealed class SearchAction {
  const SearchAction();
}

/// Events: sent by the UI.
sealed class SearchEvent extends SearchAction {
  const SearchEvent();
}

final class QueryChanged extends SearchEvent {
  const QueryChanged(this.query);
  final String query;
}

final class RetryPressed extends SearchEvent {
  const RetryPressed();
}

final class ResultTapped extends SearchEvent {
  const ResultTapped(this.id);
  final String id;
}

final class DetailsOpened extends SearchEvent {
  const DetailsOpened();
}

/// Results: produced inside the Bloc by effects. Not events, so the UI cannot add them.
sealed class SearchResult extends SearchAction {
  const SearchResult();
}

final class SearchSucceeded extends SearchResult {
  const SearchSucceeded(this.query, this.items);
  final String query;
  final List<Repo> items;
}

final class SearchFailed extends SearchResult {
  const SearchFailed(this.query);
  final String query;
}

enum SearchStatus { idle, loading, success, failure }

final class SearchState extends Equatable {
  const SearchState({
    this.query = '',
    this.items = const [],
    this.status = SearchStatus.idle,
    this.selectedRepoId,
  });

  final String query;
  final List<Repo> items;
  final SearchStatus status;
  final String? selectedRepoId;

  bool get showEmpty => status == SearchStatus.success && items.isEmpty;

  SearchState copyWith({
    String? query,
    List<Repo>? items,
    SearchStatus? status,
    String? Function()? selectedRepoId,
  }) =>
      SearchState(
        query: query ?? this.query,
        items: items ?? this.items,
        status: status ?? this.status,
        selectedRepoId: selectedRepoId != null ? selectedRepoId() : this.selectedRepoId,
      );

  @override
  List<Object?> get props => [query, items, status, selectedRepoId];
}
```

- `Equatable` gives value equality. Bloc skips emitting a state equal to the current one, and
  `bloc_test` compares emitted states with `==`.

## Reducer

```dart
SearchState reduce(SearchState state, SearchAction action) => switch (action) {
      QueryChanged(:final query) when query.trim().isEmpty => SearchState(query: query),
      QueryChanged(:final query) => state.copyWith(query: query, status: SearchStatus.loading),
      RetryPressed() => state.copyWith(status: SearchStatus.loading),
      ResultTapped(:final id) => state.copyWith(selectedRepoId: () => id),
      DetailsOpened() => state.copyWith(selectedRepoId: () => null),
      SearchSucceeded(:final query, :final items) => query != state.query
          ? state
          : state.copyWith(items: items, status: SearchStatus.success),
      SearchFailed(:final query) =>
        query != state.query ? state : state.copyWith(status: SearchStatus.failure),
    };
```

- A switch expression over the sealed `SearchAction` is exhaustive; a new event or result does not
  compile until handled.

## Bloc (store and effects)

```dart
class SearchBloc extends Bloc<SearchEvent, SearchState> {
  SearchBloc(this._repository, {this.debounce = const Duration(milliseconds: 300)})
      : super(const SearchState()) {
    on<QueryChanged>(_onQueryChanged, transformer: restartable());
    on<RetryPressed>(_onRetry, transformer: droppable());
    on<ResultTapped>((event, emit) => emit(reduce(state, event)));
    on<DetailsOpened>((event, emit) => emit(reduce(state, event)));
  }

  final RepoRepository _repository;
  final Duration debounce;

  Future<void> _onQueryChanged(QueryChanged event, Emitter<SearchState> emit) async {
    emit(reduce(state, event));
    if (event.query.trim().isEmpty) return;
    await Future<void>.delayed(debounce);
    if (emit.isDone) return; // a newer QueryChanged cancelled this handler
    await _search(event.query, emit);
  }

  Future<void> _onRetry(RetryPressed event, Emitter<SearchState> emit) async {
    emit(reduce(state, event));
    await _search(state.query, emit);
  }

  Future<void> _search(String query, Emitter<SearchState> emit) async {
    try {
      final items = await _repository.search(query);
      emit(reduce(state, SearchSucceeded(query, items)));
    } on SearchException {
      emit(reduce(state, SearchFailed(query)));
    }
  }
}
```

Notes:
- `restartable()` cancels the previous `QueryChanged` handler. Cancelling stops its `emit` calls but not
  its `Future`, so the handler checks `emit.isDone` before starting the request.
- `droppable()` ignores retries while one is running.
- A result for an old query (for example a retry that finishes after the user typed) is dropped by the
  reducer's query check.
- Handlers never build state inline; every state comes from `reduce`, so the reducer tests cover it.

## Screen

```dart
class SearchPage extends StatelessWidget {
  const SearchPage({super.key});

  @override
  Widget build(BuildContext context) => BlocProvider(
        create: (context) => SearchBloc(context.read<RepoRepository>()),
        child: const SearchView(),
      );
}

class SearchView extends StatelessWidget {
  const SearchView({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocListener<SearchBloc, SearchState>(
      listenWhen: (previous, current) => previous.selectedRepoId != current.selectedRepoId,
      listener: (context, state) {
        final id = state.selectedRepoId;
        if (id == null) return;
        context.read<SearchBloc>().add(const DetailsOpened());
        Navigator.of(context).push(MaterialPageRoute<void>(builder: (_) => RepoDetailPage(id: id)));
      },
      child: Scaffold(
        appBar: AppBar(
          title: TextField(
            onChanged: (query) => context.read<SearchBloc>().add(QueryChanged(query)),
            decoration: InputDecoration(hintText: context.l10n.searchHint), // app's AppLocalizations
          ),
        ),
        body: BlocBuilder<SearchBloc, SearchState>(
          builder: (context, state) => switch (state.status) {
            SearchStatus.idle => const SizedBox.shrink(),
            SearchStatus.loading when state.items.isEmpty => const Center(child: CircularProgressIndicator()),
            SearchStatus.failure => RetryView(
                onRetry: () => context.read<SearchBloc>().add(const RetryPressed()),
              ),
            _ when state.showEmpty => const EmptyResultsView(),
            _ => ListView.builder(
                itemCount: state.items.length,
                itemBuilder: (context, index) {
                  final repo = state.items[index];
                  return ListTile(
                    key: ValueKey(repo.id),
                    title: Text(repo.name),
                    onTap: () => context.read<SearchBloc>().add(ResultTapped(repo.id)),
                  );
                },
              ),
          },
        ),
      ),
    );
  }
}
```

- The text field owns its text; the Bloc receives every change as an event. Do not feed `state.query`
  back into a controller on every build, or the cursor jumps.
- `BlocListener` performs navigation once per selection and acknowledges it with `DetailsOpened`.
- For large screens, use `BlocSelector` or `context.select` so widgets rebuild only for their slice.

## Reducer tests (pure)

```dart
void main() {
  const repo = Repo(id: '1', name: 'flutter');

  group('reduce', () {
    test('query change starts loading and clears failure', () {
      expect(
        reduce(const SearchState(status: SearchStatus.failure), const QueryChanged('flu')),
        const SearchState(query: 'flu', status: SearchStatus.loading),
      );
    });

    test('blank query resets the screen', () {
      expect(reduce(const SearchState(query: 'f', items: [repo]), const QueryChanged('')), const SearchState());
    });

    test('stale success is ignored', () {
      const state = SearchState(query: 'flutter', status: SearchStatus.loading);
      expect(reduce(state, const SearchSucceeded('flut', [repo])), state);
    });

    test('failure for the current query shows the error', () {
      const state = SearchState(query: 'flutter', status: SearchStatus.loading);
      expect(
        reduce(state, const SearchFailed('flutter')),
        const SearchState(query: 'flutter', status: SearchStatus.failure),
      );
    });
  });
}
```

## Bloc and effect tests

```dart
class FakeRepoRepository implements RepoRepository {
  final queries = <String>[];
  Map<String, List<Repo>> results = {};
  bool failNext = false;

  @override
  Future<List<Repo>> search(String query) async {
    queries.add(query);
    if (failNext) {
      failNext = false;
      throw SearchException();
    }
    return results[query] ?? const [];
  }
}

void main() {
  const repo = Repo(id: '1', name: 'flutter');
  late FakeRepoRepository repository;

  setUp(() => repository = FakeRepoRepository()..results = {'flutter': [repo]});

  blocTest<SearchBloc, SearchState>(
    'typing quickly searches only the last query',
    build: () => SearchBloc(repository, debounce: const Duration(milliseconds: 10)),
    act: (bloc) => bloc
      ..add(const QueryChanged('flu'))
      ..add(const QueryChanged('flutter')),
    wait: const Duration(milliseconds: 50),
    expect: () => const [
      SearchState(query: 'flu', status: SearchStatus.loading),
      SearchState(query: 'flutter', status: SearchStatus.loading),
      SearchState(query: 'flutter', status: SearchStatus.success, items: [repo]),
    ],
    verify: (_) => expect(repository.queries, ['flutter']),
  );

  blocTest<SearchBloc, SearchState>(
    'failure then retry recovers',
    build: () => SearchBloc(repository..failNext = true, debounce: Duration.zero),
    act: (bloc) async {
      bloc.add(const QueryChanged('flutter'));
      await Future<void>.delayed(const Duration(milliseconds: 10));
      bloc.add(const RetryPressed());
    },
    wait: const Duration(milliseconds: 10),
    expect: () => const [
      SearchState(query: 'flutter', status: SearchStatus.loading),
      SearchState(query: 'flutter', status: SearchStatus.failure),
      SearchState(query: 'flutter', status: SearchStatus.loading),
      SearchState(query: 'flutter', status: SearchStatus.success, items: [repo]),
    ],
  );

  blocTest<SearchBloc, SearchState>(
    'tapping a result selects it for navigation',
    build: () => SearchBloc(repository),
    act: (bloc) => bloc.add(const ResultTapped('1')),
    expect: () => const [SearchState(selectedRepoId: '1')],
  );
}
```

- `blocTest` runs `build`, `act`, waits, then compares every emitted state in order.
- Short real waits are needed because the debounce uses a real `Future.delayed`. Keep the injected
  debounce small in tests; for heavier time logic, wrap the test in `fakeAsync` and elapse time manually.
- Fakes over mocks: the fake records queries, so the test verifies behaviour without interaction mocks.

## Cubit instead of Bloc

A `Cubit` exposes methods and calls `emit` directly. It suits screens without debounce, cancellation or
event ordering needs:

```dart
class FavoritesFilterCubit extends Cubit<FavoritesFilterState> {
  FavoritesFilterCubit() : super(const FavoritesFilterState());

  void toggleOnlineOnly() => emit(state.copyWith(onlineOnly: !state.onlineOnly));
}
```

- Switch a Cubit to a Bloc when you need event transformers (`restartable`, `droppable`, `sequential`)
  or a log of named events (`onTransition`, a `BlocObserver`).
- Keep the reducer-style discipline in a Cubit too: compute the next state in a pure function, do IO
  around it, and test the function without the Cubit.
