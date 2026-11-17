---
name: mobile-java
description: "Writes, reviews and modernizes Java in Android apps: Java 17 and 21 features that D8 supports, immutability, JSpecify nullability for Kotlin interop, leak-free threading without static Context or inner-class Handlers, ExecutorService, LiveData, ViewBinding, ListAdapter and DiffUtil, tests with JUnit, Mockito and Espresso, and incremental migration to Kotlin. Use when editing, reviewing or migrating .java files in an Android project."
license: MIT
metadata:
  author: Ahmad Hussain
  version: "1.0.1"
  pack: mobile-dev-kit
---

# Java on Android

Keep Java Android code correct, leak-free and Kotlin-friendly while it lives, and move it to Kotlin in
small safe steps when the team decides to.

## When to use

- Editing, fixing or reviewing `.java` files in an Android app or library.
- Bumping the Java language level, or using a JDK API that may not exist on the app's `minSdk`.
- Java code that Kotlin code calls (or will call) and needs nullability and interop annotations.
- Leaks, ANRs or crashes caused by Handlers, executors, Fragments, adapters or unclosed resources.
- Planning or executing an incremental Java-to-Kotlin migration.

Not for: Kotlin-first code (use `mobile-kotlin`), architecture choices (use `mobile-mvvm`, `mobile-mvi`).

## Workflow

1. Read the module's build file: `compileOptions` source and target level, `minSdk`, and whether
   `isCoreLibraryDesugaringEnabled` is on. These decide which features and APIs are safe.
2. Load the reference that matches the task: [Threading](references/threading.md),
   [Migration to Kotlin](references/migration-to-kotlin.md), [Testing](references/testing.md).
3. If the project already builds Kotlin and the team has not said otherwise, write new classes in Kotlin.
   Change existing Java minimally and in place.
4. Add nullability annotations to every public signature you touch.
5. Apply the rules below. Prefer fixing leaks and threading over stylistic rewrites.
6. Run lint (`./gradlew lint`) for `NewApi`, threading annotation and resource-leak checks, then the tests.
7. Keep conversion or modernization commits separate from behaviour changes.

## Toolchain: what Java you can use

| Feature | Java | On Android |
|---|---|---|
| Lambdas, method references, default and static interface methods | 8 | Desugared by D8 for every API level |
| `var`, switch expressions, text blocks, `instanceof` patterns | 10-16 | Compile-time features, every API level |
| Records | 16 | Supported by current AGP (D8 desugars them). Check reflection-based JSON libraries |
| Sealed classes and interfaces | 17 | Only on recent AGP / D8. Verify before relying on them |
| Pattern matching for `switch`, record patterns | 21 | Needs Java 21 source level and AGP / D8 support. Verify first |
| `java.time` (API 26), `java.util.stream`, `Optional`, `java.util.function` (API 24) | library | Below those API levels only with core library desugaring |
| Newer JDK methods (`List.of`, `List.getFirst()`, `Stream.toList()`) | library | Tied to newer API levels. Trust lint `NewApi`; desugaring covers only part |

The JDK that runs Gradle (17+ for current AGP) is separate from the language level and from the APIs
available at runtime. The runtime APIs come from the device's Android version.

## Rules

### 1. Language level is free, library APIs are not

```java
// BAD: compiles against a recent compileSdk, crashes on older devices (added to Android in API 35)
Device first = devices.getFirst();

// GOOD
Device first = devices.get(0);
```

```kotlin
// GOOD: java.time on minSdk below 26 through core library desugaring (app/build.gradle.kts)
android {
    compileOptions {
        isCoreLibraryDesugaringEnabled = true
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
dependencies { coreLibraryDesugaring(libs.desugar.jdk.libs) }
```

Never suppress `NewApi` without a `Build.VERSION.SDK_INT` check or confirmed desugaring.

### 2. Immutable by default

```java
// BAD: public mutable fields, internal list shared with callers
public class Device {
    public String name;
    public List<String> tags;
}

// GOOD: record with a defensive copy (works on every API level)
public record Device(String id, String name, List<String> tags) {
    public Device {
        Objects.requireNonNull(id);
        tags = Collections.unmodifiableList(new ArrayList<>(tags));
    }
}
```

- No records? `final` class, `private final` fields, no setters, copies in and unmodifiable views out.
- `static final` constants only for truly immutable values. A `static final List` is still mutable.

### 3. Nullability is declared for Kotlin callers

```java
// package-info.java: everything in the package is non-null unless marked
@NullMarked
package com.example.devices;

import org.jspecify.annotations.NullMarked;
```

```java
// BAD: Kotlin sees String! (platform type) and skips null checks, NPE at runtime
public String findName(String id) { return names.get(id); }

// GOOD: inside @NullMarked, only nullable values are annotated
public @Nullable String findName(String id) { return names.get(id); }
```

- JSpecify `@Nullable` is a type-use annotation: `List<@Nullable String>`, `String @Nullable []`.
- Packages not yet `@NullMarked` use AndroidX `@NonNull` / `@Nullable` on every public parameter and return.
- Recent Kotlin compilers report JSpecify violations as errors, so wrong annotations break the Kotlin build.

### 4. Nothing long-lived references an Activity, Fragment or View

```java
// BAD: static field keeps the Activity alive for the process lifetime
private static Context context;

// BAD: non-static inner class holds the outer Activity while queued or running
private class Poller implements Runnable {
    @Override public void run() { statusView.setText(read()); }
}

// GOOD: application context where a Context must be stored; work moved to a ViewModel
public final class StatusRepository {
    private final Context appContext;
    public StatusRepository(Context context) { this.appContext = context.getApplicationContext(); }
}
```

- Anonymous classes and lambdas that use outer members capture the outer instance too.
- `WeakReference` is a last resort for legacy callbacks, not a design.

### 5. Main-thread work goes through an explicit Looper; no AsyncTask

```java
// BAD: deprecated, binds to the calling thread's Looper
Handler handler = new Handler();

// BAD: AsyncTask is deprecated (API 30); leaks the Activity and loses results on rotation
new LoadTask().execute();

// GOOD
private final Handler main = new Handler(Looper.getMainLooper());

@Override protected void onDestroy() {
    main.removeCallbacksAndMessages(null);
    super.onDestroy();
}
```

Replace `AsyncTask` with an `ExecutorService` in a ViewModel that publishes through `LiveData`
(see [Threading](references/threading.md)).

### 6. Every executor has an owner that shuts it down; every Future can be cancelled

```java
// BAD: new thread pool per call, never shut down
Executors.newFixedThreadPool(4).execute(this::sync);

// GOOD: owned by the ViewModel, cancelled with it
public final class DevicesViewModel extends ViewModel {
    private final ExecutorService io = Executors.newSingleThreadExecutor();
    private @Nullable Future<?> loading;

    public void load() {
        if (loading != null) loading.cancel(true);
        loading = io.submit(this::loadBlocking);
    }

    @Override protected void onCleared() { io.shutdownNow(); }
}
```

If the executor is injected and shared app-wide, cancel the `Future`s in `onCleared()` instead of shutting
the executor down.

### 7. LiveData: right setter, read-only exposure, view lifecycle owner

```java
// BAD: setValue from a worker thread throws; mutable type exposed
public MutableLiveData<UiState> state = new MutableLiveData<>();
io.execute(() -> state.setValue(load()));

// GOOD
private final MutableLiveData<UiState> state = new MutableLiveData<>(UiState.loading());
public LiveData<UiState> getState() { return state; }
io.execute(() -> state.postValue(load()));
```

```java
// BAD (Fragment): observers pile up after each view recreation
viewModel.getState().observe(this, this::render);

// GOOD
viewModel.getState().observe(getViewLifecycleOwner(), this::render);
```

`postValue` keeps only the latest pending value. Use it for state, not for events that must all arrive.

### 8. ViewBinding is cleared in onDestroyView

```java
// BAD: binding outlives the Fragment's view and leaks the whole view tree
private FragmentDevicesBinding binding;

// GOOD
private @Nullable FragmentDevicesBinding binding;

@Override
public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
    binding = FragmentDevicesBinding.bind(view);
}

@Override
public void onDestroyView() {
    binding = null;
    super.onDestroyView();
}
```

Use the `Fragment(R.layout.fragment_devices)` constructor so `onCreateView` is not needed.

### 9. Lists use ListAdapter and DiffUtil

```java
// BAD: full rebind, no animations, scroll state jumps
adapter.setItems(items);
adapter.notifyDataSetChanged();

// GOOD
public final class DeviceAdapter extends ListAdapter<Device, DeviceAdapter.Holder> {
    private static final DiffUtil.ItemCallback<Device> DIFF = new DiffUtil.ItemCallback<>() {
        @Override public boolean areItemsTheSame(@NonNull Device a, @NonNull Device b) { return a.id().equals(b.id()); }
        @Override public boolean areContentsTheSame(@NonNull Device a, @NonNull Device b) { return a.equals(b); }
    };

    public DeviceAdapter() { super(DIFF); }
    // onCreateViewHolder / onBindViewHolder use getItem(position)
}

adapter.submitList(items); // new list instance each time; never mutate a submitted list
```

### 10. Resources are closed with try-with-resources

```java
// BAD: leaks on exception, StrictMode reports it
InputStream in = resolver.openInputStream(uri);
byte[] data = readAll(in);
in.close();

// GOOD
try (InputStream in = resolver.openInputStream(uri)) {
    if (in == null) throw new FileNotFoundException(uri.toString());
    return readAll(in);
}
```

Applies to `Cursor`, streams, `ParcelFileDescriptor`, `TypedArray` (API 31+ implements `AutoCloseable`;
call `recycle()` below that).

### 11. equals and hashCode are overridden together

```java
// BAD: equals without hashCode breaks HashSet, HashMap and DiffUtil
@Override public boolean equals(Object o) { return o instanceof Device d && id.equals(d.id); }

// GOOD: both, over the same fields (or use a record)
@Override public boolean equals(@Nullable Object o) {
    return o instanceof Device d && id.equals(d.id) && name.equals(d.name);
}
@Override public int hashCode() { return Objects.hash(id, name); }
```

### 12. Exceptions and interrupts are never swallowed

```java
// BAD
try { worker.join(); } catch (InterruptedException e) { }
try { sync(); } catch (Exception e) { e.printStackTrace(); }

// GOOD
try {
    worker.join();
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    return;
}
try {
    sync();
} catch (IOException e) {
    state.postValue(UiState.offline());
}
```

### 13. Interop annotations follow the direction of calls

```kotlin
// Kotlin code called from Java
class Units {
    companion object {
        @JvmStatic fun celsius(f: Double): Double = (f - 32) / 1.8 // Units.celsius(..) from Java
        const val MAX_MTU = 517                                     // compile-time constant
    }
}
class ScanSpec @JvmOverloads constructor(val timeoutMs: Long = 10_000, val lowLatency: Boolean = false)
```

`@JvmField` exposes a non-`const` property as a field. Details and ordering are in
[Migration to Kotlin](references/migration-to-kotlin.md).

### 14. Tests are deterministic

```java
// BAD: real threads and sleeps
viewModel.load();
Thread.sleep(500);

// GOOD: inject a direct executor; InstantTaskExecutorRule runs LiveData synchronously
@Rule public InstantTaskExecutorRule liveData = new InstantTaskExecutorRule();

DevicesViewModel vm = new DevicesViewModel(fakeRepo, Runnable::run);
```

See [Testing](references/testing.md) for Mockito, Espresso and `IdlingResource`.

## Anti-patterns

- Rewriting a working Java class in a review that was about a bug fix.
- `static` fields holding `Context`, `Activity`, `View`, `Fragment`, adapters or listeners.
- `new Handler()`, `AsyncTask`, `Executors.new...` inside an Activity or Fragment.
- `observe(this, ...)` in a Fragment; ViewBinding fields never cleared.
- `notifyDataSetChanged()` for list updates; mutating a list already passed to `submitList`.
- Public signatures without nullability annotations in code Kotlin calls.
- `catch (Exception e) { e.printStackTrace(); }` and empty `InterruptedException` handlers.
- Raising the Java level and assuming the JDK library on the device matches.
- Converting a file to Kotlin and changing its behaviour in the same commit.
- Logging tokens, device identifiers or personal data with `Log.d` (escalate to `mobile-security`).

## Checklist

- [ ] Language level, `minSdk` and core library desugaring checked before using a JDK API
- [ ] Lint `NewApi` clean; no blanket suppressions
- [ ] Value types immutable (records or final fields, defensive copies)
- [ ] Package `@NullMarked` or public signatures annotated with `@Nullable` / `@NonNull`
- [ ] No static or long-lived references to Activity, Fragment, View or non-application Context
- [ ] Handlers use `Looper.getMainLooper()` and are cleared; no `AsyncTask` in new code
- [ ] Executors shut down by their owner; Futures cancelled in `onCleared()`
- [ ] `setValue` on main thread, `postValue` from workers; `LiveData` exposed read-only
- [ ] Fragments observe with `getViewLifecycleOwner()`; binding nulled in `onDestroyView()`
- [ ] RecyclerView uses `ListAdapter` + `DiffUtil` with id-based `areItemsTheSame`
- [ ] Closeables in try-with-resources
- [ ] `equals` and `hashCode` overridden together
- [ ] No swallowed exceptions; interrupt status restored
- [ ] Tests use direct executors and `InstantTaskExecutorRule`; Espresso uses `IdlingResource`, not sleeps

## Related skills

- `mobile-kotlin` -- target idioms when migrating, and Kotlin-side interop rules
- `mobile-mvvm` -- ViewModel and LiveData or StateFlow architecture
- `mobile-design-patterns` -- Builder, Factory and Strategy where Java needs them
- `mobile-code-review` -- review workflow and severity levels
- `mobile-security` -- storage, logging and network rules for legacy Java code
- `mobile-ci-cd` -- lint and test gates in the build pipeline
- `mobile-testing` -- cross-platform test strategy
