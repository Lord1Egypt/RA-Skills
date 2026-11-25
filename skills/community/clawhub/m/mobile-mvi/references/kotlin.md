# MVI with Kotlin, Jetpack Compose and StateFlow

Load this when building or reviewing an MVI store in Kotlin. Assumes Kotlin 2.x, AndroidX Lifecycle 2.8
or newer, Hilt, and Turbine in tests. No MVI library is required; the store is a plain `ViewModel`.

The feature: repository search with a 300 ms debounce, latest-query-wins, retry after failure, and
opening a result's details as a one-off effect.

## Contract

```kotlin
data class Repo(val id: String, val name: String)

interface RepoRepository {
    suspend fun search(query: String): List<Repo> // throws IOException on network failure
}
```

## Actions, state and effects

```kotlin
sealed interface SearchAction

/** Sent by the UI. */
sealed interface SearchIntent : SearchAction {
    data class QueryChanged(val query: String) : SearchIntent
    data object RetryClicked : SearchIntent
    data class ResultClicked(val id: String) : SearchIntent
}

/** Produced by effects only. Carries the query so stale results can be rejected. */
sealed interface SearchResult : SearchAction {
    data class Loaded(val query: String, val items: List<Repo>) : SearchResult
    data class Failed(val query: String) : SearchResult
}

data class SearchState(
    val query: String = "",
    val items: List<Repo> = emptyList(),
    val isLoading: Boolean = false,
    val hasError: Boolean = false,
) {
    val showEmpty: Boolean get() = query.isNotBlank() && !isLoading && !hasError && items.isEmpty()
}

sealed interface SearchEffect {
    data class OpenDetails(val id: String) : SearchEffect
}
```

- `onIntent` accepts `SearchIntent` only, so the UI cannot fake a `SearchResult`.

## Reducer

```kotlin
fun reduce(state: SearchState, action: SearchAction): SearchState = when (action) {
    is SearchIntent.QueryChanged ->
        if (action.query.isBlank()) {
            SearchState(query = action.query)
        } else {
            state.copy(query = action.query, isLoading = true, hasError = false)
        }

    SearchIntent.RetryClicked -> state.copy(isLoading = true, hasError = false)

    is SearchIntent.ResultClicked -> state

    is SearchResult.Loaded ->
        if (action.query != state.query) state
        else state.copy(items = action.items, isLoading = false, hasError = false)

    is SearchResult.Failed ->
        if (action.query != state.query) state
        else state.copy(isLoading = false, hasError = true)
}
```

- Exhaustive `when` without `else`: adding an action breaks the build until it is handled.
- Previous items stay visible while a new query loads; the UI shows a progress bar over them.

## Store

```kotlin
@HiltViewModel
class SearchViewModel @Inject constructor(
    private val repository: RepoRepository,
) : ViewModel() {

    private val _state = MutableStateFlow(SearchState())
    val state: StateFlow<SearchState> = _state.asStateFlow()

    private val _effects = Channel<SearchEffect>(Channel.BUFFERED)
    val effects: Flow<SearchEffect> = _effects.receiveAsFlow()

    private var searchJob: Job? = null

    fun onIntent(intent: SearchIntent) {
        dispatch(intent)
        when (intent) {
            is SearchIntent.QueryChanged -> search(intent.query, debounce = true)
            SearchIntent.RetryClicked -> search(_state.value.query, debounce = false)
            is SearchIntent.ResultClicked -> _effects.trySend(SearchEffect.OpenDetails(intent.id))
        }
    }

    private fun dispatch(action: SearchAction) {
        _state.update { reduce(it, action) }
    }

    private fun search(query: String, debounce: Boolean) {
        searchJob?.cancel()
        if (query.isBlank()) return
        searchJob = viewModelScope.launch {
            if (debounce) delay(DEBOUNCE_MS)
            val result = try {
                SearchResult.Loaded(query, repository.search(query))
            } catch (e: IOException) {
                SearchResult.Failed(query)
            }
            dispatch(result)
        }
    }

    companion object {
        const val DEBOUNCE_MS = 300L
    }
}
```

Notes:
- Concurrency policy: cancel previous. The reducer's query check covers the window where a result
  completes just before the cancel.
- `CancellationException` is not caught: only `IOException` becomes a result.
- `ResultClicked` could also navigate directly from the UI. It goes through the store here because real
  screens usually record it (recent searches, analytics) before navigating.

## Screen

```kotlin
@Composable
fun SearchRoute(
    onOpenDetails: (String) -> Unit,
    viewModel: SearchViewModel = hiltViewModel(),
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    val lifecycleOwner = LocalLifecycleOwner.current // androidx.lifecycle.compose.LocalLifecycleOwner
    val currentOnOpenDetails by rememberUpdatedState(onOpenDetails)

    LaunchedEffect(viewModel, lifecycleOwner) {
        lifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
            withContext(Dispatchers.Main.immediate) {
                viewModel.effects.collect { effect ->
                    when (effect) {
                        is SearchEffect.OpenDetails -> currentOnOpenDetails(effect.id)
                    }
                }
            }
        }
    }

    SearchScreen(state = state, onIntent = viewModel::onIntent)
}

@Composable
fun SearchScreen(
    state: SearchState,
    onIntent: (SearchIntent) -> Unit,
    modifier: Modifier = Modifier,
) {
    Column(modifier) {
        OutlinedTextField(
            value = state.query,
            onValueChange = { onIntent(SearchIntent.QueryChanged(it)) },
            label = { Text(stringResource(R.string.search_label)) },
            singleLine = true,
        )
        if (state.isLoading) LinearProgressIndicator(Modifier.fillMaxWidth())
        if (state.hasError) {
            ErrorRow(onRetry = { onIntent(SearchIntent.RetryClicked) })
        }
        if (state.showEmpty) Text(stringResource(R.string.search_empty))
        LazyColumn {
            items(state.items, key = { it.id }) { repo ->
                RepoRow(repo = repo, onClick = { onIntent(SearchIntent.ResultClicked(repo.id)) })
            }
        }
    }
}
```

- `rememberUpdatedState` keeps the long-lived effect collector from calling a stale `onOpenDetails`.
- The text field round trip is synchronous (`update` on the main thread), so the cursor does not jump.
- `SearchScreen` takes state and one callback, so previews pass any `SearchState`.

## Reducer tests (pure, no coroutines)

```kotlin
class SearchReducerTest {
    private val repo = Repo("1", "kotlinx.coroutines")

    @Test
    fun `query change starts loading and clears error`() {
        val next = reduce(SearchState(query = "ko", hasError = true), SearchIntent.QueryChanged("kot"))
        assertEquals(SearchState(query = "kot", isLoading = true), next)
    }

    @Test
    fun `blank query resets results`() {
        val state = SearchState(query = "k", items = listOf(repo))
        assertEquals(SearchState(query = ""), reduce(state, SearchIntent.QueryChanged("")))
    }

    @Test
    fun `loaded result for current query shows items`() {
        val state = SearchState(query = "kotlin", isLoading = true)
        val next = reduce(state, SearchResult.Loaded("kotlin", listOf(repo)))
        assertEquals(SearchState(query = "kotlin", items = listOf(repo)), next)
    }

    @Test
    fun `stale result for an older query is ignored`() {
        val state = SearchState(query = "kotlin", isLoading = true)
        assertEquals(state, reduce(state, SearchResult.Loaded("kot", listOf(repo))))
    }

    @Test
    fun `failure shows error and stops loading`() {
        val state = SearchState(query = "kotlin", isLoading = true)
        assertEquals(SearchState(query = "kotlin", hasError = true), reduce(state, SearchResult.Failed("kotlin")))
    }
}
```

## Store and effect tests

```kotlin
class FakeRepoRepository : RepoRepository {
    val queries = mutableListOf<String>()
    var failNext = false
    var results: Map<String, List<Repo>> = emptyMap()

    override suspend fun search(query: String): List<Repo> {
        queries += query
        if (failNext) {
            failNext = false
            throw IOException("offline")
        }
        return results[query].orEmpty()
    }
}

class SearchViewModelTest {
    // StandardTestDispatcher, not Unconfined: each launched effect runs as its own step,
    // so Turbine sees every intermediate state instead of a conflated one.
    @get:Rule val mainDispatcherRule = MainDispatcherRule(StandardTestDispatcher())

    private val repo = Repo("1", "kotlin")
    private val repository = FakeRepoRepository().apply { results = mapOf("kotlin" to listOf(repo)) }

    @Test
    fun `typing quickly searches only the last query`() = runTest {
        val viewModel = SearchViewModel(repository)

        viewModel.onIntent(SearchIntent.QueryChanged("k"))
        viewModel.onIntent(SearchIntent.QueryChanged("ko"))
        viewModel.onIntent(SearchIntent.QueryChanged("kotlin"))
        advanceUntilIdle()

        assertEquals(listOf("kotlin"), repository.queries)
        assertEquals(SearchState(query = "kotlin", items = listOf(repo)), viewModel.state.value)
    }

    @Test
    fun `failure then retry recovers`() = runTest {
        repository.failNext = true
        val viewModel = SearchViewModel(repository)

        viewModel.state.test {
            assertEquals(SearchState(), awaitItem())

            viewModel.onIntent(SearchIntent.QueryChanged("kotlin"))
            assertEquals(SearchState(query = "kotlin", isLoading = true), awaitItem())
            assertEquals(SearchState(query = "kotlin", hasError = true), awaitItem())

            viewModel.onIntent(SearchIntent.RetryClicked)
            assertEquals(SearchState(query = "kotlin", isLoading = true), awaitItem())
            assertEquals(SearchState(query = "kotlin", items = listOf(repo)), awaitItem())
        }
    }

    @Test
    fun `clicking a result emits OpenDetails`() = runTest {
        val viewModel = SearchViewModel(repository)

        viewModel.effects.test {
            viewModel.onIntent(SearchIntent.ResultClicked("42"))
            assertEquals(SearchEffect.OpenDetails("42"), awaitItem())
        }
    }
}
```

- `MainDispatcherRule` is the same rule as in the `mobile-mvvm` Kotlin reference. Because `Dispatchers.Main`
  is a `TestDispatcher`, `runTest` shares its scheduler: `delay(300)` is skipped in virtual time and
  `advanceUntilIdle()` drives `viewModelScope`.
- `StateFlow` conflates. With an unconfined Main dispatcher and a fake that never suspends, the loading
  state of a retry can be overwritten before the collector sees it; the standard dispatcher avoids that.
- Assert whole `SearchState` values. A stray field change fails the test instead of slipping through.
- Effects are tested on their own flow; they never appear in state assertions.
