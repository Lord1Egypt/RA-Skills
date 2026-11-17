---
name: mobile-code-review
description: "Reviews Kotlin, Java, Swift and Dart code and diffs in Android, iOS and Flutter apps for correctness, concurrency, lifecycle leaks, UI performance, architecture, error handling, tests, accessibility and i18n. Reports Blocker, Major, Minor and Nit findings with file:line and fix snippets, then an Approve or Request changes verdict. Use when reviewing a pull request, merge request, diff, branch or file before merging mobile code."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Mobile code review

Review mobile code the way a senior Android, iOS and Flutter engineer would: find the defects that will crash,
leak, hang or mislead users in production, explain why each one matters, and show the fix.

## When to use

- A pull request, merge request, branch, commit range or single file needs review.
- The user asks "review this", "is this safe to merge", "what is wrong with this code".
- Before merging changes in Kotlin, Java, Swift, Objective-C interop or Dart code.
- After the agent itself wrote mobile code and should check it before handing it over.

Not for: a full security audit (use `mobile-security`), or designing an architecture from scratch
(use `mobile-mvvm`, `mobile-mvi`).

## Workflow

1. Establish scope.
   - Diff against the merge base, not the tip of main: `git diff --merge-base origin/main`.
   - Read the MR description and linked ticket so findings are judged against intent.
2. Identify platforms and load the matching reference before reviewing:
   [Kotlin](references/kotlin.md), [Java](references/java.md), [Swift](references/swift.md),
   [Dart and Flutter](references/dart.md).
3. Read every changed file in full, plus direct callers and callees of changed functions.
   A hunk out of context hides most lifecycle and threading bugs.
4. Pass over the change once per dimension, in this order:
   correctness, concurrency, lifecycle and memory, security and privacy, UI performance,
   architecture, error handling, tests, accessibility, i18n.
5. Verify each candidate finding before reporting it.
   - Trace the code path. Check it is not already handled elsewhere (base class, interceptor, wrapper).
   - If it cannot be confirmed from the code, report it as a question, not a defect.
6. Assign a severity (see below) and write a minimal fix snippet for every Blocker and Major.
7. Give the verdict. Do not edit files unless the user asks for fixes.

## Severity levels

| Severity | Meaning | Merge impact |
|---|---|---|
| Blocker | Crash, data loss or corruption, security or privacy breach, broken build, store rejection | Must fix before merge |
| Major | Wrong behaviour on a realistic path, leak, race, ANR or hang, swallowed error, missing test for new logic, broken layer boundary | Fix before merge, or defer only with a ticket |
| Minor | Maintainability, small inefficiency, unclear naming that misleads, missing edge-case test | Should fix, may be a follow-up |
| Nit | Preference or polish. Never blocks | Optional |

Rules for severity:
- Rate by consequence and likelihood, not by how easy the fix is.
- Do not report what the formatter or linter already enforces.
- One root cause is one finding. List extra locations inside it.

## Rules

### 1. Coroutines and tasks are scoped to an owner and cancellable

Work outlives its screen when launched in a global scope. It leaks memory and writes to dead UI.

Kotlin:
```kotlin
// BAD
GlobalScope.launch { repo.sync() }

// GOOD
viewModelScope.launch { repo.sync() }
```

Swift:
```swift
// BAD: unstructured task keeps running after the view disappears
.onAppear { Task { await model.load() } }

// GOOD: cancelled automatically when the view disappears
.task { await model.load() }
```

Dart:
```dart
// BAD
_sub = stream.listen(_onData); // never cancelled

// GOOD
@override
void dispose() {
  _sub?.cancel();
  super.dispose();
}
```

Java:
```java
// BAD: executor never shut down, callbacks hit a destroyed Activity
executor.execute(() -> textView.setText(load()));

// GOOD: work in a ViewModel, result exposed as LiveData, executor shut down in onCleared()
executor.execute(() -> result.postValue(load()));
```

### 2. Cancellation is never swallowed

Kotlin:
```kotlin
// BAD: runCatching also catches CancellationException and breaks structured concurrency
val user = runCatching { api.user() }.getOrNull()

// GOOD
val user = try {
    api.user()
} catch (e: IOException) {
    null
}
```

Swift:
```swift
// BAD: loop ignores cancellation
for id in ids { await upload(id) }

// GOOD
for id in ids {
    try Task.checkCancellation()
    await upload(id)
}
```

### 3. UI state is touched only on the main thread or actor

Kotlin:
```kotlin
// BAD: hardcoded dispatcher, untestable and easy to misuse
withContext(Dispatchers.IO) { dao.insert(item) }

// GOOD: injected dispatcher
class Repo(private val io: CoroutineDispatcher) {
    suspend fun save(item: Item) = withContext(io) { dao.insert(item) }
}
```

Swift:
```swift
// BAD: UI state mutated from an arbitrary executor
final class FeedModel: ObservableObject { @Published var items: [Item] = [] }

// GOOD
@MainActor @Observable
final class FeedModel { var items: [Item] = [] }
```

Dart:
```dart
// BAD: 5 MB JSON parsed on the UI isolate, drops frames
final data = jsonDecode(body);

// GOOD
final data = await Isolate.run(() => jsonDecode(body));
```

### 4. No long-lived references to short-lived objects

Kotlin:
```kotlin
// BAD: Activity leaked for the lifetime of the process
object Analytics { lateinit var context: Context }

// GOOD
class Analytics @Inject constructor(@ApplicationContext private val context: Context)
```

Swift:
```swift
// BAD: self -> timer -> closure -> self
timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in self.tick() }

// GOOD
timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { [weak self] _ in self?.tick() }
```

Dart:
```dart
// BAD: controller created in build, never disposed
Widget build(BuildContext context) => TextField(controller: TextEditingController());

// GOOD: owned by the State object, disposed in dispose()
late final _controller = TextEditingController();
```

### 5. Async UI code re-checks lifecycle after every suspension point

Dart:
```dart
// BAD
await repo.save();
Navigator.of(context).pop();

// GOOD
await repo.save();
if (!context.mounted) return;
Navigator.of(context).pop();
```

Kotlin (Compose):
```kotlin
// BAD: collects while the app is in the background
val state by viewModel.state.collectAsState()

// GOOD
val state by viewModel.state.collectAsStateWithLifecycle()
```

### 6. UI recomposes and rebuilds only what changed

Kotlin (Compose):
```kotlin
// BAD: no key, item state jumps on reorder
LazyColumn { items(messages) { MessageRow(it) } }

// GOOD
LazyColumn { items(messages, key = { it.id }) { MessageRow(it) } }
```

Swift (SwiftUI):
```swift
// BAD: index identity, wrong rows animate on insert
ForEach(items.indices, id: \.self) { i in Row(item: items[i]) }

// GOOD: Item is Identifiable with a stable id
ForEach(items) { item in Row(item: item) }
```

Dart (Flutter):
```dart
// BAD: whole screen rebuilds on every tick
setState(() => _seconds++);

// GOOD: only the label listens
ValueListenableBuilder<int>(
  valueListenable: _seconds,
  builder: (context, value, _) => Text('$value'),
)
```

### 7. Errors are handled where they can be acted on, and never silently dropped

Kotlin:
```kotlin
// BAD
try { upload() } catch (e: Exception) { }

// GOOD
try {
    upload()
} catch (e: IOException) {
    _state.update { it.copy(error = UiError.Network) }
}
```

Swift:
```swift
// BAD
let data = try? await api.fetch()

// GOOD
do {
    state = .loaded(try await api.fetch())
} catch {
    state = .failed(error)
}
```

### 8. Layer boundaries hold

- ViewModels and domain code do not import `android.view`, `UIKit` views or `BuildContext`.
- Domain models are not network DTOs or database entities. Map at the data-layer edge.
- UI does not call repositories or APIs directly.

```kotlin
// BAD: ViewModel holds a View and returns a Retrofit DTO
class ProfileViewModel(private val view: TextView, private val api: Api)

// GOOD
class ProfileViewModel(private val getProfile: GetProfileUseCase) : ViewModel()
```

### 9. New logic ships with tests, and tests are deterministic

```kotlin
// BAD: real delay, flaky and slow
Thread.sleep(500)

// GOOD: virtual time, runs instantly
@Test fun retriesAfterBackoff() = runTest {
    val repo = Repo(api = failingOnceApi, io = StandardTestDispatcher(testScheduler))
    val result = async { repo.load() }
    advanceTimeBy(500)
    assertEquals(expected, result.await())
}
```

Swift: use `await` on the operation under test, not `sleep`. Dart: use `fakeAsync` or `tester.pump(duration)`.

### 10. Accessibility and i18n are part of correctness

```kotlin
// BAD
Icon(Icons.Default.Delete, contentDescription = null) // actionable icon, no label

// GOOD
Icon(Icons.Default.Delete, contentDescription = stringResource(R.string.delete))
```

```swift
// BAD: concatenated String is shown verbatim, never localized, no plural rules
Text("You have " + String(count) + " messages")

// GOOD: localized key with a plural variation in the String Catalog
Text("You have \(count) messages", comment: "Inbox count")
```

- Touch targets at least 48dp (Android) or 44pt (iOS).
- Text scales with system font size. No fixed heights on text containers.
- Use start/end, not left/right, so RTL layouts work.
- Never build sentences by concatenating translated fragments.

## Anti-patterns

- Reviewing only the diff hunks without opening the full file.
- Reporting style issues the linter already catches.
- "Consider refactoring" with no reason and no snippet.
- Twenty Nits hiding one Blocker. Order by severity, cap Nits at five.
- Guessing at a bug the code does not show. Ask instead.
- Approving with an open Blocker or Major because "it was already like that". Pre-existing issues in
  touched lines are in scope; elsewhere, mention them once as out of scope.
- Rewriting the author's whole function in the fix snippet. Show the smallest change.

## Checklist

- [ ] Read the MR description, ticket and every changed file in full
- [ ] Coroutines, Tasks, Futures and Streams have an owner and are cancelled
- [ ] Cancellation is propagated (no catch-all over suspending or async code)
- [ ] UI state mutated only on main thread or `@MainActor`
- [ ] No Activity, Context, View or BuildContext stored beyond its lifecycle
- [ ] Closures capturing `self` checked for cycles; controllers and subscriptions disposed
- [ ] Lists have stable keys or identity; no heavy work in composition, body or build
- [ ] No swallowed errors; user-facing failure state exists
- [ ] No secrets, tokens or personal data in code or logs (escalate to `mobile-security`)
- [ ] Layer boundaries respected; DTOs mapped at the data layer
- [ ] New logic has deterministic tests
- [ ] Accessibility labels, touch targets, dynamic text size
- [ ] User-visible strings localized, plurals handled, RTL safe
- [ ] Every Blocker and Major has a fix snippet

## Output format

~~~markdown
## Review: <MR title or scope>

Scope: <files / commits reviewed>. Platforms: <Android | iOS | Flutter>.

### Findings

1. [Blocker] path/to/File.kt:42 -- <one-line issue>
   Why: <consequence for users or the codebase>
   Fix:
   ```kotlin
   <minimal snippet>
   ```

2. [Major] path/to/View.swift:88 -- <issue>
   Why: ...
   Fix: ...

### Questions
- path/to/file.dart:17 -- <thing that could not be confirmed from the code>

### Clean
- <dimensions checked with no findings, for example "Concurrency: no issues">

### Verdict
Request changes -- 1 Blocker, 1 Major.
~~~

Verdict rule: any Blocker or Major means Request changes. Otherwise Approve, listing Minor and Nit items as optional.

## Related skills

- `mobile-security` -- deep MASVS audit when the change touches storage, network, auth or crypto
- `mobile-kotlin`, `mobile-java`, `mobile-swift`, `mobile-flutter` -- language rules the review applies
- `mobile-mvvm`, `mobile-mvi`, `mobile-design-patterns` -- architecture expectations
- `mobile-merge-request` -- MR description, commits and reviewer etiquette
- `mobile-testing` -- what test coverage a change should come with
- `mobile-performance` -- measuring a suspected jank, startup or memory regression
- `mobile-accessibility` -- full accessibility audit against WCAG 2.2
