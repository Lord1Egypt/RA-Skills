---
name: nasal-doc
description: Generates and verifies inline documentation and type annotations for Nasal, enhancing code readability and developer accuracy.
---

## Nasal doc
Nasal-doc is a skill designed to generate documentation and type annotations for Nasal code.

Although FlightGear's native Nasal interpreter does not support static typing, we can leverage AI tools to insert descriptive comments and type annotations directly into the codebase.

## How to use this skill
|Invocation|What it does|
|------|------|
|`nasal-doc add-doc file.nas ...`|Append brief documentation and type annotations to the variables, functions, and classes within file.nas, leaving the original program logic and comments completely untouched. Multiple files are supported.|
|`nasal-doc remove-doc file.nas ...`|Strip away the added type annotations and generated documentation, leaving the original comments and program logic untouched.|
|`nasal-doc check file.nas ...`|Inspect the documentation and type annotations for correctness and do not generate the complete fix code.|

## Format of the documentation

### Functions / Methods
The documentation for a function includes parameters, returns, throws, and side effects. The "throws" section is used for functions that call `die()`. Side effects include mutating external variables and global state, modifying the property tree, and performing I/O operations (such as reading/writing files or making network requests), but exclude writing to logs.

If a function accepts no arguments, the "args" section can be omitted. For rest parameters (e.g., `func (nums...) {}`), append `[]` to the type. If a function does not return a value, use "Returns: void" instead of "Returns: nil". If a function never returns (such as an infinite loop or one that always calls `die()` or `abort()`), use "Returns: Never".

Example:
```nasal
# Calculates fib(n) % 16777216.
# Args:
#     n (int): The number to be calculated.
# Returns:
#     int: The Fibonacci number at position n.
# Throws: No
# Side effects: No
var fib = func(n) {
    if (n <= 1) return n;
    
    var a = 0;
    var b = 1;
    for (var i = 2; i <= n; i += 1) {
        (a, b) = (b, (a + b) & 16777215);
    }
    return b;
};

# Logs an error object and terminates the whole simulator. Used when encountering a fatal error.
# Args:
#     error (any): The error representation or exception object to be dumped.
# Returns: void
# Throws: No
# Side effects: Writes telemetry data to /path/to/file and halts program execution.
var dump_error_and_stop = func(error) {
    dump_error(error);
    abort();
}
```
### Classes
For classes, specify the type and purpose of each property. If a property is static, mark it as "static".

For small methods or functions, unnecessary parts of the documentation can be omitted, keeping only what is essential. For example, for the new() method, there is no need to specify the return value, as it always returns an instance of the class itself. Also mark static methods that do not use `me`.

Example:
```nasal
# Define a 3D position.
# static _className (string): For runtime lookup.
# static dimensions (int): Number of dimensions.
# x (double): The x-coordinate.
# y (double): The y-coordinate.
# z (double): The z-coordinate.
var Position3D = {
    _className: "Position3D", # for runtime lookup
    dimensions: 3,
    # Args:
    #     x, y, z (double): XYZ coordinates
    new: func(x, y, z) {
        var inst = { parents: [Position3D] }; # the parents vector is like prototypes in JS
        inst.x = x;
        inst.y = y;
        inst.z = z;
        return inst;
    },
    # Returns: string
    toString: func {
        return sprintf("%s(%g, %g, %g)", me._className, me.x, me.y, me.z);
    }
    # Returns: Position3D
    # Static
    fromxy: func(x, y) {
        return Position3D.new(x, y, 0);
    }
};
```
### Variables
Only global variables that are frequently modified need type annotations. Almost all local variables and global constants do not need them, as their types can be inferred.

Example:
```nasal
# type: timer[]
var timers_need_cleanup = []; # timers that get cleaned up upon exit

# or
# timers that get cleaned up upon exit
var timers_need_cleanup = []; # type: timer[]

# Most constants do not need type annotations
# var ALT_THRESHOLD = 30000.0;
```

## Type annotations
Type annotations are not checked by automated tools; they are intended solely for humans (and AIs) to read in order to improve coding accuracy.

Available types are:
- `int` : integer numbers (e.g., indices, counts)
- `double` : floating-point numbers (e.g., coordinates, angles)
- `number`: equivalent to `int | double`.
- `string`
- `boolean`: equivalent to `0 | 1`. If a function is known to return only 0 or 1 and is used for conditional checks, use `boolean` instead of `int`.
- `nil`
- `scalar` : shorthand for `int | double | string` (use when the function accepts any primitive value)
- `type[]` (can be nested. For example, `(type[])[]` represents a two-dimensional array.)
- `[type1, type2, ...]` (used when a function returns a list with a fixed sequence of specific types, such as `[string, int]`.)
- `{ key: type }` (e.g., `{a: int, b: double[], c: double | nil}`. If the key names of a hash are unknown, use `hash<key_type, value_type>`, such as `hash<int, string>`.)
- class names (e.g, `MyCls` and `props.Node`)
- types of native objects (e.g., `timer` for the return type of `maketimer()`)
- functions (e.g., `(string) => string` and `(int, int[]...) => void`)
- literals (e.g., `"airliner" | "light_civilian"`)

Types can be nested, and `|` is used to denote union types. In addition, `any` and `unknown` are also available as valid types. `void` and `Never` are purely constraints and do not serve as types.

Types can also be aliased. For example:
```nasal
# type alias: terrainMaterial = {light_coverage: double, bumpiness: double, load_resistance: double, solid: boolean, names: string[], friction_factor: double, rolling_friction: double}
# type alias: geodinfoResult = [double, terrainMaterial | nil] | nil
```
