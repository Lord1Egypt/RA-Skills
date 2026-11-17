# Java (Android) review reference

Load this when the change contains `.java` files. Java on Android is usually legacy code, so focus on leaks,
threading and Kotlin interop rather than asking for a rewrite.

## Quick scan

| Pattern | Why | Usual severity |
|---|---|---|
| `static Context`, `static Activity`, `static View` | Leaks the Activity for the process lifetime | Major |
| Non-static inner `Handler`, `Runnable`, `AsyncTask`, listener in an Activity | Implicit outer reference leaks the Activity | Major |
| `new Handler()` with no Looper | Deprecated, binds to whatever thread calls it | Minor |
| `AsyncTask` | Deprecated since API 30, leaks and loses results on rotation | Major in new code |
| `Executors.new...` with no `shutdown()` | Thread leak | Major |
| `catch (InterruptedException e) {}` | Interrupt status lost | Major |
| `catch (Exception e) {}` / `e.printStackTrace()` | Swallowed error | Major |
| `notifyDataSetChanged()` | Full rebind, no animations | Minor |
| `observe(this, ...)` in a Fragment | Duplicate observers after view recreation | Major |
| `equals` without `hashCode` (or the reverse) | Broken in sets, maps, DiffUtil | Major |
| `Stream`, `Cursor` or `InputStream` not closed | Resource leak | Major |

## Leaks and lifecycle

```java
// BAD: inner class holds MainActivity, message queue holds the Handler
private final Handler handler = new Handler() {
    @Override public void handleMessage(Message msg) { textView.setText("done"); }
};

// GOOD: no outer reference, explicit Looper, callbacks removed in onDestroy
private final Handler handler = new Handler(Looper.getMainLooper());

@Override protected void onDestroy() {
    handler.removeCallbacksAndMessages(null);
    super.onDestroy();
}
```

- Fragments observe with `getViewLifecycleOwner()` and null the binding in `onDestroyView()`.
- Listeners registered in `onStart` / `onResume` are removed in the matching `onStop` / `onPause`.

## Threading

- Background work belongs in a ViewModel or repository using an `ExecutorService` that is shut down in
  `onCleared()`, not in the Activity.
- `LiveData.setValue` on the main thread only; `postValue` from background threads. `postValue` coalesces:
  if called twice quickly only the last value is delivered. Flag it when every value matters.
- Shared mutable fields accessed from multiple threads are `volatile`, guarded by `synchronized`, or use
  `java.util.concurrent.atomic` types. Check-then-act on a `ConcurrentHashMap` still needs `computeIfAbsent`
  or similar.

```java
// BAD: interrupt swallowed, thread cannot be stopped cleanly
try { Thread.sleep(1000); } catch (InterruptedException e) { }

// GOOD
try {
    Thread.sleep(1000);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    return;
}
```

## Resources

```java
// BAD
Cursor c = db.query(...);
while (c.moveToNext()) { ... }

// GOOD
try (Cursor c = db.query(...)) {
    while (c.moveToNext()) { ... }
}
```

## Value objects and collections

- `equals` and `hashCode` are overridden together, over the same fields.
- `DiffUtil.ItemCallback.areItemsTheSame` compares ids; `areContentsTheSame` compares content
  (usually via `equals`).
- Getters do not expose internal mutable collections:

```java
// BAD
public List<Item> getItems() { return items; }

// GOOD
public List<Item> getItems() { return Collections.unmodifiableList(items); }
```

## Kotlin interop

- Public API used from Kotlin carries nullability annotations. Prefer JSpecify
  (`org.jspecify.annotations.Nullable`, `@NullMarked` on the package) or AndroidX `@Nullable` / `@NonNull`.
  Without them Kotlin sees platform types and null checks disappear.
- Static utilities that Kotlin callers use often are candidates for migration, but migration is out of scope
  for a review unless the MR is about it.

## Testing

- JUnit 4 or 5 with Mockito for unit tests; `InstantTaskExecutorRule` when LiveData is involved.
- Espresso tests use `IdlingResource` or test executors, never `Thread.sleep`.
