# Managed-language leaks: translating Power of 10 Rule 3

Rule 3 says do not allocate after initialisation. That is a C rule, and applying it
literally to Dart, Kotlin, Swift, TypeScript or Python is nonsense: every string is
an allocation. The *intent* transfers exactly: **every allocation has one owner and
a provable release point.**

## Where the leak actually lives

| Language | A leak is | Detect with |
|---|---|---|
| C / C++ | unfreed pointer, mismatched `free`, lost handle | Valgrind, ASan + LSan |
| Rust | `mem::forget`, `Rc`/`Arc` cycle, `Box::leak` | Miri, `cargo clippy` |
| Swift | retain cycle, observer never removed, `Task` never cancelled | Instruments Leaks, Memory Graph |
| Kotlin / Java | listener not unregistered, `static` collection, coroutine scope never cancelled | LeakCanary, heap dump |
| Dart / Flutter | undisposed `StreamSubscription`, controller, listener, timer | Flutter DevTools Memory, `dispose()` tests |
| TypeScript / JS | listener not removed, `setInterval` never cleared, module-level `Map` | heap snapshot diff |
| Python | module-level cache, `lru_cache` unbounded, circular refs with `__del__` | `tracemalloc`, `gc.get_referrers` |

## The five checks that catch almost all of it

1. **Ownership is single.** Every subscription, listener, timer, controller,
   animation and stream is disposed in the matching teardown, and a test asserts it.
2. **No capture across an async gap.** No `BuildContext`, `this`, or controller
   reference held across an `await`. Check mounted, or pass the dependency in.
3. **No unbounded cache.** If a cache must exist it has a maximum size and an
   eviction policy, both stated.
4. **Structured concurrency only.** Every spawned task is owned by a scope that
   cannot outlive its parent. No fire-and-forget. Swift task groups, Kotlin
   `coroutineScope`, Dart `Future.wait` with owned futures, Python `TaskGroup`.
5. **Every handle is closed.** Files, sockets, database connections and clients are
   closed by a scope guard (`with`, `use`, `defer`, `try`-with-resources), not by a
   human remembering.

The reason structured concurrency belongs in a memory document is that the classic
leak is an orphan: a task whose parent returned long ago, still holding references
and still scheduled. Nathaniel J. Smith's argument is the argument against
`go`-style fire-and-forget: if a task's lifetime is not nested inside its caller's,
no one can prove when its resources are released.

## Per-language idioms

**Dart / Flutter**

```dart
@override
void initState() {
  super.initState();
  _subscription = stream.listen(_onEvent);
}

@override
void dispose() {
  _subscription.cancel();
  _controller.dispose();
  super.dispose();
}
```

**Rust** — prefer ownership to reference counting; where `Rc` is unavoidable, break
cycles with `Weak`.

**Swift** — `[weak self]` in escaping closures; `defer` for teardown; never keep a
`Timer` without invalidating it.

**Kotlin** — `coroutineScope { }` over `GlobalScope`; `DisposableEffect` to pair
registration with disposal.

**Python** — context managers over manual close; `functools.lru_cache(maxsize=...)`
never unbounded; no module-level mutable caches.

## The rule for an agent

Before finishing, answer four questions in the report:

1. What did I allocate or subscribe to?
2. Where is it released?
3. Which test proves it is released?
4. What happens if the release path itself fails?
