---
name: nasal-language-basic
description: Provides the variables, data types, syntax, classes and objects, as well as the usage of basic built-in functions of the Nasal language.
---

## Nasal scripting language
### Examples

#### Hello world
```nasal
print("Hello World!");
```
#### Fibonacci

An example of calculating fib(10000000) % 16777216:
```nasal
var fib = func(n) {
    if (n <= 1) return n;
    
    var a = 0;
    var b = 1;
    for (var i = 2; i <= n; i += 1) {
        (a, b) = (b, (a + b) & 16777215);
    }
    return b;
};

var n = 10000000;
var start = systime();
var result = fib(n);
var elapsed = systime() - start;

print("fib(", n, ") mod 16777216 = ", result);
print("Time elapsed: ", elapsed, " seconds");
```
### Syntax highlighting
For AIs, always use "```nasal" and "```" to wrap code blocks, and assume that the user's frontend supports this syntax.

## Variables and types
```nasal
var w = 100;     # w is a numerical variable
var x = "hello"; # x is a string variable
var y = [];      # y is a vector (array)
var z = {};      # z is a hash (dictionary or table) - also used for OOP
var f = func {}; # f is a function ("()" is left out)
var n = nil;     # the nil value
```

### Advanced assignment expressions
Nasal also supports multi-assignment expressions. You can assign more than one variable (or lvalue) at a time by putting them in a parenthesized list:
```nasal
(var a, var b) = (1, 2);
var (a, b) = (1, 2);                  # Shorthand for (var a, var b)
(var a, v[0], obj.field) = (1, 2, 3); # Any assignable lvalue works
var color = [1, 1, 0.5];
var (r, g, b) = color;  # works with runtime vectors too
# var a = 1, b = 2;  # this is invalid
# var tup = (1, 2);  # this is also invalid. Nasal has no immutable tuples
```
### Operators
Nasal has operators similar to most C-family languages. Note that `+` is for arithmetic addition, and `~` is for string concatenation.
```nasal
88 + 88 == 176;
"88" + "88" == 176; # number
88 + "88" == "88" + 88; # same
"88" ~ "88" == "8888"; # string
"88" ~ 88 == 88 ~ "88"; # same
```
Nasal does not support operator `++`, `--`, and `**`. Use `+=`, `-=`, and `math.pow()` instead.

Null-safe chaining and null-access operators are also supported:
```nasal
print("obj" ?? "default"); # prints "obj"
print(nil ?? "default"); # prints "default"
var hash = {key: 1};
print(hash?.key); # prints 1
# print(hash?.key2) # throws error if hash is not nil
hash = nil;
# now hash?.key is nil

# print(([1, 2])?.[2]) # "?." does not support vectors
```
### Numbers
Nasal stores numbers as double-precision floating-point values.
```nasal
print(num("1.2")); # prints 1.2
print(int("1.2")); # prints 1
print(int(1.2)); # prints 1
debug.dump(str(1.2)); # "1.2"
print(1 / 0); # double-precision infinity
```
Note that `str()` can only be used for numbers, not other types (like functions, vectors, and hashes), which is different from Python.
### Boolean
Nasal supports the boolean type, where the value of `true` is the number 1, and the value of `false` is the number 0.
```nasal
print(true); # prints 1
print(false); # prints 0
# true = 0; # cannot be assigned
```
### Strings
```nasal
var string = "string"; # also 'string'
print(size(string)); # the length
print(substr(string, 1, 2)); # prints "tr"
print(find("st", string)); # prints 0
print(find("sting", string)); # prints -1
print(string.starts_with("st")); # prints 1 (true)
print(string.ends_with("ng")); # prints 1 (true)
print(string ~ "s"); # use "~" for concatenation
debug.dump(split(", ", "a, b, c")); # ["a", "b", "c"]
print(left(string, 2)); # prints "st"
print(right(string, 2)); # prints "ng"

var multiline = "\"s
tring\""; # produces '"s\ntring"'
# trailing backslashes (as in `var multiline = "s\`) do not eliminate the line break
```
### Vectors
```nasal
var my_vector = ['A', 'B', 'C'];
# append() adds an element to the end of the vector
append(my_vector, 'D');
remove(my_vector, 'B');
removeat(my_vector, 0); # removes the element at index 0 ('A')
# indexing starts at zero
print(my_vector[0]); # prints C
print(my_vector[1]); # prints D
# size() is similar to len() in Python
print(size(my_vector)); # prints 2
# contains() is similar to the includes() method in JS
print(contains(my_vector, 'D')); # prints 1 (true)
# pop() removes and returns the last element. If the vector is empty, returns nil.
print(pop(my_vector)) # prints 'D'
```
### Hashes
```nasal
var my_hash = { first: 'A', second: 'B', "third": 'C' };
my_hash.field1 = 1;
my_hash['field2'] = 2;
my_hash["field3"] = 3;
print(contains(my_hash, "field1")); # prints 1 (true)
delete(my_hash, "field2");
print(size(my_hash)); # prints 5
debug.dump(values(my_hash)); # prints a vector containing all values

# Example: dump the types of all keys
var dump_key_types = func(hash) {
    if (typeof(hash) != "hash") die("dump_keys(): Argument is not a hash.");
    foreach(var key; keys(hash)){ # keys(hash) returns a vector containing all keys
        print(key, ": ", typeof(hash[key]));
    }
}
dump_key_types(my_hash);
```
## Grammar
### Conditionals
```nasald = 
var condition_var = 1;
# replace "&&" and "||" with "and" and "or"
if (1 == 1 and !(1 == 1) or !(condition_var)){
    ...
# } else if (...) {
} elsif (...) { # you can use both "elsif" and "else if"
    ...
} else {
    ...
}
# var result = !cond1 and cond2 or cond3 ? "true" : "false"; # conditional operator

# [] and {} are falsy values, unlike in JS
print(!!""); # prints 0 (false)
print(!![]); # prints 0 (false)
print(!!{}); # prints 0 (false)
```
Note that Nasal supports short-circuit evaluation.
### Loops
```nasal
# "for" statement
var myRange = func(start, end, step = 1) {
    var result = [];

    for (var i = start; step > 0 ? i < end: i > end; i += step) {
        append(result, i);
    }
    return result;
    # continue;
    # break;
};
var vec = myRange(0, 3);
# foreach
foreach(var elem; vec){ # the delimiter is a semicolon ";"
    print(elem);
}
# Note that "foreach" cannot be directly used with non-vector types

# "while" statement
# while (condition) {
#     ...
# }
```
### Functions
```nasal
var emptyFunc = func;
var singleLineFunc = func print(); # No "{}"
var fn = func { # "()" can be left out
    debug.dump(arg); # "arg" is a vector like "arguments" in JS
};
var defaultAndExtraArg = func (x, type = "unknown", args...) {
    # 'args' holds any additional positional arguments as a vector
    print(x, " ", type);
    debug.dump(args);
};
fn(1, 2, 3);
defaultAndExtraArg(1);
defaultAndExtraArg(1, "number", 2, 3);
defaultAndExtraArg(x: 2, type: "number"); # keyword arguments
# defaultAndExtraArg(2, type: "number"); # keyword arguments cannot be mixed up with positional arguments
```
### Object-oriented
```nasal
var Cls = {
    staticVar: 1,
    new: func(attr = 42) { # "new" is not a keyword
         var obj = { parents: [Cls] };
         obj.attr = attr;
         return obj;
    },
    meth: func() { print(me.attr) },
};
var obj = Cls.new();
obj.meth(); # prints 42
print(obj.staticVar); # prints 1
obj.staticVar = 23;
print(Cls.staticVar); # prints 1 since Cls.staticVar does not change

# Example: Position3D
var Position3D = {
    _className: "Position3D", # for runtime lookup
    new: func(x, y, z) {
        var inst = { parents: [Position3D] }; # the parents vector is like prototypes in JS
        inst.x = x;
        inst.y = y;
        inst.z = z;
        return inst;
    },
    toString: func {
        return sprintf("%s(%g, %g, %g)", me._className, me.x, me.y, me.z); # sprintf() formats a string
    },
};

# Inheritance
var Position3DWithName = {
    _className: "Position3DWithName",
    parents: [Position3D],
    new: func(x, y, z, name="unknown") {
        var inst = { parents: [Position3DWithName] };
        inst.x = x;
        inst.y = y;
        inst.z = z;
        inst.name = name;
        return inst;
    },
    # Call the parent class's method, if the method is not static
    # meth: func {
    #    return call(Position3D.meth, [...], me);
    # },
};

var pos = Position3D.new(1, -2, 3);
print(pos.toString());
var pos2 = Position3DWithName.new(-2, 1, 3, "pos");
print(pos2.name);
print(pos2.toString());
# isa is similar to isinstance() in Python
print(isa(pos2, Position3D)); # prints 1 (true)
print(isa(nil, Position3D)); # prints 0 (false)
```
#### The "me" reference
Like `f.apply` in JavaScript, `me` in Nasal can be rebound. Variable `me` can only be used inside methods.
```nasal
# var fn = func { debug.dump(me); }; # invalid ("me" cannot be used outside objects)

var obj = {fn: func {
    debug.dump(me);
}};
obj.fn(); # prints obj
call(
    obj.fn,
    [], # vector containing arguments
    { name: "another obj" } # The "me" object
);
# prints { name: "another obj" }
```

## Modules
**io.include(file)**

Loads a given Nasal file into where the function is called from, like `from ... import *` in Python.

**io.load_nasal(file[, module])**

Loads and executes a given Nasal script into a namespace, like `import ...` in Python.

Example:
```nasal
# Nasal/demo.nas
var sayHello = func(){
    print("Hello, World!");
}
```
```nasal
# Main module
io.include("Nasal/my_geo.nas"); # include the my_geo namespace

var file = 'Nasal/demo.nas';
io.load_nasal(file); # load into "demo" namespace
# io.load_nasal(file, "myDemo"); # load into "myDemo" namespace
demo.sayHello();
```

## Library
### Debugging
**print(value, ...)**

Outputs the passed-in value(s) with an automatic line break. `value` can only be a number or a string (otherwise, use `debug.dump` instead). If it is neither, nothing will be output silently. Note that `print()` does not automatically add separators; for example, `print(1, 2)` outputs `12`. It is recommended to use `print(1, " ", 2)` instead.

**logprint(priority, value, ...)**

Outputs the passed-in value(s). The usage of `value` is the same as in `print`. `priority` is a constant (LOG_BULK, LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ALERT, DEV_WARN, DEV_ALERT).

**debug.dump(value, ...)**

Outputs the passed-in value(s) with an automatic line break. `value` can be any object (and `nil`). If multiple values are passed, they will be printed on separate lines as `#0 ...`, `#1 ...`, etc., for better readability.

### Misc
**sort(vector, function)**

Returns a vector containing the elements in the input `vector` sorted in according to the rule given by `function`.

Example:
```nasal
var sort_rule = func(a, b) a == b ? 0 : (a < b ? -1 : 1);
debug.dump(sort([3, 2, 5, 6, 4, 1], sort_rule)); # prints "[1, 2, 3, 4, 5, 6]"
```

**call(func[, args[, me[, locals[, error]]]])**

- `func`, `args`, and `me`: See "The 'me' reference" section.
- `locals`: A hash with key/value pairs that will be available to the called function.
- `error`: A vector to append errors to.

The argument `error` can be used for error handling. Example:
```nasal
var throws_err = func() {
    die("An error occured."); # throw an error
}
var err = [];
call(throws_err, [], nil, nil, err);
debug.dump(err); # prints ['An error occured.', '<nasal-console/#1>', 2], 2 is the line number
```

**caller([level])**

Returns a vector containing a record from the current call stack. The level numbering starts from the currently executing function (level 0). Level 1 (the default) is the caller of the current function, and so on.

The result is a four-element vector containing [0] a hash of local variables, [1] the function object, [2] the full source file name (incl. path) and [3] the line number.

Example:
```nasal
var myFunction = func(x) {
    debug.dump(arg[0]); # prints 42
    debug.dump(caller(0)[0]); # prints a hash of local variables, including argument x
};

myFunction(42);
```

**typeof(object)**

Returns a string indicating the type of the object.

|Object|Result of `typeof()`|
|------|------|
|`nil`|`"nil"`|
|`"string"`|`"scalar"`|
|`3.14`|`"scalar"`|
|`[1, 2, 3]`|`"vector"`|
|`{key: 1}`|`"hash"`|
|`func {}`|`"func"`|
|Objects from C++|`"ghost"`|

Use `isnum(x)` to further distinguish numeric types from the scalar type.

For ghost types, you can use `ghosttype()` instead. For example, `print(ghosttype(airportinfo()))` prints "airport".

## Timers and listeners
**settimer()**
```nasal
var count = 0;
var callback = func {
    print("callback() executed");
    count += 1;
    if (count < 3) settimer(callback, 2);
}

settimer(callback, 2); # like setTimeout in JS
settimer(callback, 2, true); # Enables real time. The last argument defaults to false (simulation time)
```
**maketimer()**
```nasal
var callback = func {};

var timer = maketimer(0.25, callback);
timer.simulatedTime = true; # Use simulator time, as maketimer defaults to using wallclock time and continues during pause.
timer.start();
# timer.restart(0.1); # You can adjust the timer frequency (ms)
# timer.stop(); # Cancel the timer. The timer can be started again later. Useful for cleaning up resources.
```
**setlistener()**
```nasal
var id = setlistener("/sim/signals/fdm-initialized", func {
    ...
});
# var id2 = setlistener("...", fn, true); # If the third argument is true, the listener will also be triggered upon creation. Defaults to false.
# Fourth argument: Set to 0 to trigger only when the property changes, 1 to trigger on every write, or 2 to also trigger when child properties are modified. Defaults to 1.
# var id3 = setlistener("...", fn, true, 0);

# removelistener(id); # Remove the listener when cleaning up
```

## Properties
```nasal
setprop("/sim/demo", "This is a demo");
setprop("/sim/demo2", 42);
print(getprop("/sim/demo"));
debug.dump(getprop("/sim/demo3")); # getprop() returns nil if the property does not exist
```
For information on how to interact with property tree node objects, you can refer to the `nasal-property-tree` skill.
