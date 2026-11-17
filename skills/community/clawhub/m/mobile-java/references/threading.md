# Threading in Java Android code

Load this when Java code starts background work, touches the main thread, handles callbacks from
system services (Bluetooth, location, sensors) or replaces `AsyncTask`.

## Quick scan

| Pattern | Why | Fix |
|---|---|---|
| `new Thread(...).start()` in UI code | Unowned, no cancellation, leaks the Activity | Owned executor in a ViewModel or repository |
| `AsyncTask` | Deprecated, leaks, loses results on rotation | `ExecutorService` + `LiveData` |
| `new Handler()` | Deprecated, implicit Looper | `new Handler(Looper.getMainLooper())` |
| `Executors.new...` without `shutdown()` | Thread leak | Owner shuts it down, or inject a shared one |
| `future.get()` on the main thread | ANR | Callback, `LiveData`, or `get` only on a worker |
| `CompletableFuture.supplyAsync(task)` with no executor | Runs on the common ForkJoin pool | Pass an explicit executor |
| Work inside a `BluetoothGattCallback` method | Blocks a binder thread | Hand off to a single-thread executor |
| Check-then-act on a shared `HashMap` | Race | `ConcurrentHashMap.computeIfAbsent` or a lock |

## Replacing AsyncTask

```java
// BAD
private class LoadTask extends AsyncTask<Void, Void, List<Device>> {
    @Override protected List<Device> doInBackground(Void... v) { return repo.devices(); }
    @Override protected void onPostExecute(List<Device> d) { adapter.submitList(d); }
}

// GOOD: ViewModel owns the work, the Fragment only observes
@HiltViewModel
public final class DevicesViewModel extends ViewModel {
    private final DeviceRepository repo;
    private final ExecutorService io;
    private final MutableLiveData<UiState> state = new MutableLiveData<>(UiState.loading());
    private @Nullable Future<?> pending;

    @Inject
    public DevicesViewModel(DeviceRepository repo, @IoExecutor ExecutorService io) {
        this.repo = repo;
        this.io = io;
    }

    public LiveData<UiState> getState() { return state; }

    public void load() {
        if (pending != null) pending.cancel(true);
        pending = io.submit(() -> {
            try {
                state.postValue(UiState.loaded(repo.devices()));
            } catch (IOException e) {
                state.postValue(UiState.error());
            }
        });
    }

    @Override protected void onCleared() {
        if (pending != null) pending.cancel(true); // shared executor: cancel work, do not shut it down
    }
}
```

`@IoExecutor` is a project-defined qualifier. Tests pass an `ExecutorService` that runs tasks synchronously
(see [Testing](testing.md)).

## Executors

- One shared, injected pool for IO (`@Singleton` in DI). Per-feature pools only when work must be serialized,
  usually `Executors.newSingleThreadExecutor()`.
- Owners that create an executor call `shutdown()` (finish queued work) or `shutdownNow()` (interrupt) when
  their lifecycle ends.
- `Future.cancel(true)` only interrupts. Blocking code must respond: check
  `Thread.currentThread().isInterrupted()` in loops and do not swallow `InterruptedException`.
- Main-thread executor without a Context dependency on the call site: `ContextCompat.getMainExecutor(context)`.
- Name threads with a `ThreadFactory` so stack traces and profilers show what each pool is for.

```java
ThreadFactory named = r -> new Thread(r, "ble-io");
ExecutorService bleIo = Executors.newSingleThreadExecutor(named);
```

## Futures

- `CompletableFuture` (API 24+) chains with explicit executors:

```java
CompletableFuture
    .supplyAsync(repo::loadConfig, io)
    .thenApplyAsync(ConfigMapper::toDomain, io)
    .whenComplete((config, error) -> state.postValue(error == null ? UiState.ready(config) : UiState.error()));
```

- Libraries that expect `ListenableFuture` (WorkManager, CameraX) can be bridged with
  `CallbackToFutureAdapter` from `androidx.concurrent:concurrent-futures`.

## Main thread and Handlers

```java
// BAD: inner class Handler keeps the Activity alive while messages are queued
private final Handler handler = new Handler() {
    @Override public void handleMessage(Message msg) { title.setText("done"); }
};

// GOOD
private final Handler main = new Handler(Looper.getMainLooper());
private final Runnable refresh = this::refresh; // field, so it can be removed

@Override protected void onStart() {
    super.onStart();
    main.postDelayed(refresh, 1_000);
}

@Override protected void onStop() {
    main.removeCallbacks(refresh);
    super.onStop();
}
```

- Annotate methods with `@MainThread`, `@WorkerThread` or `@AnyThread` (`androidx.annotation`); lint checks calls
  between them.

## Shared state

- Immutable snapshots shared between threads are safe without locks. Prefer replacing a reference over
  mutating shared collections.
- `volatile` for a single flag or reference written by one thread and read by others.
- `AtomicInteger`, `AtomicReference` for counters and compare-and-set updates.
- `synchronized` blocks for invariants spanning several fields. Never call out to unknown code while holding a lock.

```java
// BAD: two threads both miss and both create
if (!cache.containsKey(id)) cache.put(id, load(id));

// GOOD
Session session = sessions.computeIfAbsent(id, this::open); // ConcurrentHashMap
```

## System callbacks (Bluetooth, location, sensors)

- `BluetoothGattCallback` methods run on binder threads, not the main thread. Do not block them, and do not
  touch views or call `setValue` from them.
- Hand each callback to one single-thread executor, so state updates and the next GATT operation are
  serialized in callback order.
- Android GATT allows one outstanding operation per connection. Queue reads and writes; issue the next one
  only after the previous callback.
- Copy byte arrays received in callbacks before handing them to another thread if the source may be reused.

```java
private final ExecutorService gattThread = Executors.newSingleThreadExecutor();

@Override
public void onCharacteristicChanged(@NonNull BluetoothGatt gatt,
                                    @NonNull BluetoothGattCharacteristic characteristic,
                                    @NonNull byte[] value) {
    byte[] copy = value.clone();
    gattThread.execute(() -> frames.onFrame(copy)); // CRC check and parsing happen off the binder thread
}
```

The `value` parameter variant of `onCharacteristicChanged` is the API 33+ callback; older devices call the
deprecated variant, so implement both when `minSdk` is below 33.

## Background work that must survive the screen

- Deferrable or guaranteed work: WorkManager. A Java `Worker.doWork()` runs synchronously on WorkManager's
  background executor; return `Result.retry()` for transient failures.
- Long-running user-visible work: a foreground service with the correct `foregroundServiceType`
  (required when targeting Android 14+).

## Debug checks

```java
if (BuildConfig.DEBUG) {
    StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder().detectAll().penaltyLog().build());
    StrictMode.setVmPolicy(new StrictMode.VmPolicy.Builder().detectAll().penaltyLog().build());
}
```

StrictMode flags disk and network access on the main thread and leaked closeables. LeakCanary in debug
builds catches retained Activities and Fragments.
