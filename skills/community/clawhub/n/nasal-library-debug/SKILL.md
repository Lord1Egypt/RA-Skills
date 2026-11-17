---
name: nasal-library-debug
description: Provides the usage of the debug library of the Nasal language.
---

## Debugging Library (`debug.*`)

The `debug` library provides comprehensive mechanisms to inspect data structures, handle non-fatal exceptions, trace property modifications, profile execution speed, and monitor real-time code execution via the FlightGear property tree.

### Environment & Node Inspection

#### debug.dump(arg1, arg2, ...)

Dumps the target arguments directly to the console. If no arguments are given, it dumps the entire **local namespace** (current variables). When handling multiple arguments, each is formatted sequentially with an index (`#0`, `#1`, etc.). Unlike `print()` which does not support vectors and hashes, `debug.dump()` can output any object.

```nasal
var x = nil;
debug.dump(); # prints local scope: "{ x: nil, arg: [] }"

debug.dump(["a", "b"], { k: 1 });
# prints:
# #0 ['a', 'b']
# #1 { k: 1 }

```

#### debug.string(obj[, color])

Convert any data type (including vectors, hashes, internal C++ `ghost` nodes, and functions) into a readable string representation, similar to `repr()` in Python. Setting `color` to `1` (true) wraps the output string in standard ANSI color codes.

#### debug.attributes(node[, verbose[, color]])

Inspects structural flags of a mandatory `props.Node` instance. Returns a string layout matching `(type[, attr[, Lnum[, #refs]])`.

* **Attributes (`attr`):** `r` (read-protected), `w` (write-protected), `R` (trace read), `W` (trace write), `A` (archive), `U` (user-archive), `P` (preserve), `T` (tied).
* **Listeners (`Lnum`):** Preceded by `L`, indicates the active runtime listener count.
* **References (`#refs`):** Displays extra handles tracking the node beyond its core implicit definitions (shown only when `verbose` defaults to `1`).

```nasal
var node = props.globals.getNode("/sim/signals/fdm-initialized");
print(debug.attributes(node)); # Output example: "(BOOL, L6, #16)"

```

#### debug.propify(p[, create])

Attempts to cast a raw argument `p` (which can be a `props.Node` instance, a raw property `ghost` pointer, or a path string) into a formal `props.Node` object. If `p` is a string path and `create` is `1`, it creates the target property node dynamically if it doesn't exist. Returns `nil` if the conversion fails.

#### debug.tree([node[, graph]])

Recursively outputs the tree hierarchy starting from the target `node` path or reference down to console layout. The boolean `graph` parameter defaults to `1` (indents nodes using empty spacing); setting it to `0` flattens the output layout format.


### Stack Tracing & Runtime Controls

#### debug.backtrace([desc]) / debug.bt([desc])

Prints the current execution stack call layout down to the console window. It automatically expands and displays all active local namespace variables associated with every single execution layer depth. `desc` is an optional descriptive header string.

#### debug.local([frame])

Prints and immediately returns a hash structure wrapping the entire active local namespace context. Passing an integer target `frame` index allows extraction of ancestor variable tables up the stack context (analogous to indices inside `caller()`).

#### debug.isnan(num)

Validates numeric integrity. Returns `1` (true) if the float evaluation yields an illegal `NaN` state (e.g., math exceptions like computing `1/0`), otherwise returns `0`.

#### debug.printerror(err)

Accepts a structured error vector trapped via the fifth slot of a formal `call()` invocation and formats the target exception traceback explicitly out to console stdout without dropping execution flow.

```nasal
call(func { print(math.invalid_member); }, [], nil, nil, var err = []);
debug.printerror(err); # Formats exception safely; thread continues intact

```

#### debug.warn(msg[, level])

Triggers an immediate diagnostics print flag inside execution context similar to `die()`, but **does not halt the application thread**. The integer `level` parameter configures how many internal active calling frame contexts are excluded from the output log line header trace tracking.

---

### Profiling & Benchmarking

#### debug.benchmark(label, fn[, repeat[, output]])

Executes a target function wrapper `fn` while computing processing runtime footprints.

* If `repeat` is omitted, `fn` is invoked once, printing execution speed metrics.
* If `repeat` is designated but `output` is omitted, it prints the aggregated time duration metric spanning across the total execution loops block.
* If a target vector array is passed to `output`, the execution loop stores the sequential return outputs yielded from each function cycle directly inside the vector, returning it upon completion.

```nasal
var task = func { return getprop("/sim/time/gmt"); };
var results = debug.benchmark("Time Check", task, 100, []);

```

#### debug.benchmark_time(fn[, repeat[, output]])

Behaves identically to `debug.benchmark()`, except it suppresses auto-printing metrics to console stdout and instead **returns** the raw execution time duration tracking variable back directly.

#### debug.rank(list[, repeat])

Benchmarks an array vector populated with multiple distinct target execution functions. Evaluates them concurrently using the loop iterations count configured via `repeat` and returns a sorted processing performance vector organized from **fastest execution to slowest**, structured exactly as `[[func_ptr, duration_ms], ...]`.

#### debug.print_rank(label, list, names)

Accepts a structural metrics output matrix array yielded by `debug.rank()` along with a mapping database `names` (can be an association array hash matching `{ name: func }` or a nested structural array pairing layout like `[[name, func], ...]`), printing out an organized overview detailing relative processing speeds in milliseconds alongside relative execution ratios.

### Advanced Instrumentation Classes

#### debug.Probe

Monitors code execution and hotspots by mirroring statistics directly into the active flight simulator property tree path location: `/_debug/nas/probe-<label>/*`.

* `debug.Probe.new(label[, class])`: Standard constructor initializing the property node path.
* `.enable()` / `.disable()`: Toggles metrics evaluation loops on and off.
* `.reset()`: Flushes structural hit frequencies indices back down to zero.
* `.addCounter()`: Appends an alternate tracked subunit pointer returning an assigned identification token index integer.
* `.hit([counter_id[, callback]])`: Increments performance trace tracking hits inside hot code loops. Can option a functional execution hook callback taking `(hit_count)`.
* `.setTimeout(seconds)`: Automates a safety window flag; the next subsequent `.hit()` matching past the expiration timeout value calls `.disable()` natively to prevent flooding nodes.
* `.enableTracing()` / `.disableTracing()`: Toggles deep trace tracking support to snapshot stack filenames and lines into property tree nodes.

#### debug.Breakpoint

Inherits directly from `debug.Probe` to offer selective runtime backtrace interventions monitored via `/_debug/nas/bp-<label>/*`. Uses a token consumption design to ensure diagnostics don't flood system logs. Each recorded hit consumes one token; when tokens drop below 1, trace outputs pause completely until replenished via script or the runtime property tree browser UI.

* `debug.Breakpoint.new(label[, dump_locals[, skip_level]])`: Standard constructor setting the identifier. Set `dump_locals` to `0` if dumping massive scopes runs the risk of generating a memory stack overflow crash.
* `.enable([tokens])`: Activates execution tracking boundaries by provisioning a starting pool of active backtrace operations tokens (defaults to `1`).
* `.hit([callback])`: Evaluates state inline. Consumes a tracking token and triggers an implicit stack dump unless overridden by custom functionality targeting `callback(hit_count, remaining_tokens)`.

### Example
```nasal
# 1. Initialize a performance profiling probe
var sensorProbe = debug.Probe.new("AltSensor");
sensorProbe.enableTracing();
sensorProbe.enable();

# 2. Define a simulated property reader function that occasionally throws errors
var fetchAltitude = func() {
    # Record a probe hit (statistics can be viewed in the property tree under /_debug/nas/probe-AltSensor/)
    sensorProbe.hit();

    # Intentionally trigger an occasional error: randomly generate a NaN or read a non-existent member
    if (rand() > 0.85) {
        die("GPS Signal Lost!"); 
    }
    
    # When operating normally, resolve the path to a props.Node and read it safely
    var path = "/position/altitude-ft";
    var node = debug.propify(path, 1); # Create it if it does not exist
    
    # Print the node's attribute status, e.g., (DOUBLE, A, #1)
    if (rand() > 0.95) {
        print("Node Attribute: ", debug.attributes(node));
    }
    
    return node.getValue() ?? 0.0;
};

# 3. Core task execution: Use call() to catch exceptions and diagnose them using the debug library
var updateAvionics = func() {
    var err = [];
    var result = nil;
    
    # Safe call: Even if fetchAltitude crashes, the main thread will not be interrupted
    call(fetchAltitude, [], nil, nil, err);
    
    if (size(err) > 0) {
        # Catch and pretty-print the exception stack trace
        debug.warn("Avionics update failed temporarily!");
        debug.printerror(err);
        
        # Dump a snapshot of the local variables in the current frame
        debug.dump(debug.local());
    }
};

# 4. Stress testing: Use the benchmark utility to evaluate performance over 100 iterations
print("--- Starting Avionics Benchmark ---");
var timeTaken = debug.benchmark_time(updateAvionics, 100);
print("100 cycles took: ", timeTaken, " seconds.");

# 5. Disable the probe
sensorProbe.disable();
```
