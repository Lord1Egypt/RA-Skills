# Multi-Threading

## Overview

`perry/thread` provides real OS threads (not green threads or workers). Each thread has its own arena + GC. Values cross threads via deep-copy (`SerializedValue`).

```typescript
import { parallelMap, parallelFilter, spawn } from 'perry/thread'
```

## parallelMap

Data-parallel transformation across all CPU cores. Preserves input order.

```typescript
const doubled = parallelMap([1, 2, 3, 4], n => n * 2)
// [2, 4, 6, 8]

const results = parallelMap(urls, url => fetch(url).then(r => r.json()))
```

### Capture Rules

Compile-time enforcement — these cause build errors:
- Mutable `let` variables
- Objects/arrays with mutations after capture
- Class instances with internal state
- Closures that reference `this`

OK to capture: `const` primitives, immutable `const` objects/arrays, pure functions.

## parallelFilter

Data-parallel filtering. Preserves input order.

```typescript
const evens = parallelFilter([1, 2, 3, 4, 5, 6], n => n % 2 === 0)
// [2, 4, 6]
```

## spawn

Spawn a background OS thread. Returns a `Promise<T>`.

```typescript
const result = await spawn(() => {
  // runs on a real OS thread
  return heavyComputation(42)
})
```

Multiple concurrent spawns:
```typescript
const [a, b, c] = await Promise.all([
  spawn(() => computeA()),
  spawn(() => computeB()),
  spawn(() => computeC()),
])
```

## Safety Model

- **No shared mutable state**: No `SharedArrayBuffer` or `Atomics`
- **Deep copy at boundary**: All values are serialized when crossing threads
- **Independent GC**: Each thread has its own arena and garbage collector
- **Results via queue**: `spawn` results flow back through `PENDING_THREAD_RESULTS` queue, drained during `js_promise_run_microtasks()`

## Architecture

| Feature | Implementation |
|---------|---------------|
| Thread type | Real OS thread (pthread) |
| Memory | Independent arena per thread |
| GC | Per-thread generational mark-sweep |
| Data transfer | SerializedValue deep-copy |
| Result delivery | PENDING_THREAD_RESULTS queue |
| Max threads | All available CPU cores |
