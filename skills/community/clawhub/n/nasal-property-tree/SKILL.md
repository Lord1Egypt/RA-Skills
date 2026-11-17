---
name: nasal-property-tree
description: Explains the components of the property tree, introduces the Nasal `props` library for property-tree access, and covers saving and loading PropertyList XML files.
---

## Components of the Property Tree

- **Nodes**: A node can hold a typed value as well as child nodes, and both can coexist at the same time.
* **Indices**: Sibling nodes sharing an identical identifier are organized as an indexed array using zero-based numerical offsets. Omitting brackets defaults to index `0` (e.g., `/sim/view` = `/sim/view[0]`). Deleting an indexed node does not re-index or shift subsequent elements, leaving the vacated slot available for reuse.
* **Aliases**: Allows a node to dynamically mirror another target node path, routing all read and write operations directly to the destination.
* **Node attributes**: Flags defining internal engine behaviors, including read/write permissions, runtime state preservation, logging triggers, and persistent serialization.

Besides the lossless XML format, properties can also be represented as a Nasal hash. If a node contains both a value and child nodes, only the child nodes are preserved when converted to a Nasal hash.


## Property Tree Manipulation (`props`)

Nasal interacts with the FlightGear hierarchical Property Tree through the `props` module. The core wrapper class is `props.Node`, which wraps internal C++ property ghosts (`prop`) and exposes a complete API for tree navigation, type-safe modifications, structural node duplication, and evaluation.

### Part 1: Node Instantiation & Navigation

#### Constructors & Accessors

* `props.Node.new([structure_hash])`: Instantiates a standalone property node. If an optional Nasal hash is passed, its nested keys, values, and arrays will automatically initialize equivalent node paths inside the new instance.
* `props.getNode(path[, create])`: Global alias returning a path node from the root system property tree. If `create` is true, create the node when it does not exist.
* `props.globals`: Global property tree root wrapper of type `props.Node`.
* `.getNode(rel_path[, create])`: Evaluates a relative path string. Returns `nil` if not found and `create` is `0`.
* `.getChild(name[, index[, create]])`: Finds or instantiates a direct child element using a specific name and numerical array offset index.
* `.getChildren([name])`: Returns a Nasal vector of `props.Node` child instances. If `name` is specified, it filters results to nodes matching that identifier.
* `.getParent()`: Returns the parent `props.Node` wrapper or `nil` if executed at root.
* `.getPath()`: Returns the absolute string path representing the location within the Property Tree.
* `.getName()`: Returns the name string of the specific node.
* `.getIndex()`: Returns the node's numerical index integer.

```nasal
# Create an isolated mock tree
var local_root = props.Node.new({
    "instruments": {
        "altimeter": [
            { "indicated-ft": 5500 },
            { "indicated-ft": 12000 }
        ]
    }
});

# Navigate nested levels
var alt2 = local_root.getNode("instruments/altimeter[1]");
print("Target node path: " ~ alt2.getPath()); # /instruments/altimeter[1]
print("Altitude: " ~ alt2.getValue());       # 12000

```

#### Node Lifetime & Structural Mutation

* `.addChild(name[, min_idx[, append]])`: Explicitly creates a single empty node child.
* `min_idx` (default `0`): Forces the index space to start at or above this value.
* `append` (default `1`): Adds the child immediately above the highest existing index for that name. If `0`, fills the lowest available index starting at `min_idx`.


* `.addChildren(name, count[, min_idx[, append]])`: Creates multiple sequential child elements with a single call.
* `.remove()`: Safely destroys the calling node, detaching it from the tree hierarchy.
* `.removeChild(name, index)`: Destroys a targeted child node by its specific index.
* `.removeChildren([name])`: Removes all child nodes matching a specific identifier name. If no argument is provided, it empties all child nodes.
* `.removeAllChildren()`: Empties the node completely.

---

### Part 2: Type-Safe Values & Data Mutations

Nodes have strict internal types (e.g., `BOOL`, `INT`, `DOUBLE`, `STRING`, `VEC3D`, `VEC4D`).

#### Getting and Checking Types

* `.getValue([rel_path])`: Reads the node value. Optionally takes a relative path to target a child node.
* `.getBoolValue()`: Returns the value interpreted as a Nasal boolean (`1` or `0`). Strings like `"false"` resolve to `0`.
* `.getType()`: Returns the string type representation: `"NONE"`, `"BOOL"`, `"INT"`, `"LONG"`, `"FLOAT"`, `"DOUBLE"`, `"STRING"`, `"VEC3D"`, `"VEC4D"`, `"ALIAS"`, or `"UNSPECIFIED"`.
* `.isInt()`: Returns `1` if the node holds an integer or long integer, `0` otherwise.
* `.isNumeric()`: Returns `1` if the node is numeric (`INT`, `LONG`, `FLOAT`, `DOUBLE`), `0` otherwise.

#### Writing Values

* `.setValue([rel_path, ]value)`: Resolves and commits a value to the node. Handles conversions automatically based on the input type. Passing a 3-element or 4-element vector of numbers converts the node type to `VEC3D` or `VEC4D` respectively.
* `.setBoolValue([rel_path, ]bool)`: Forces the node to a boolean format (`1` or `0`).
* `.setIntValue([rel_path, ]int)`: Converts and truncates the input value to an integer.
* `.setDoubleValue([rel_path, ]double)`: Commits a floating-point number.
* `.getValues()`: Exports the entire local hierarchy starting from this node as a structured Nasal hash.
* `.setValues(hash)`: Populates the node's local hierarchy recursively from a Nasal hash.
* `.clearValue()`: Wipes the current value, returning the internal type back to `"NONE"`.

#### Mathematical Shortcuts

* `.adjustValue(delta)`: Adds `delta` (numerical) to the current node value while preserving the node's internal data type.
* `.increment(n)`: Safely increments an integer-type property by `n` (defaults to `1`).
* `.decrement(n)`: Safely decrements an integer-type property by `n` (defaults to `1`).
* `.toggleBoolValue()`: Inverts a boolean node's state (`0` $\leftrightarrow$ `1`). The target node must be initialized to the `BOOL` type first.

```nasal
var fuel_node = props.globals.getNode("/consumables/fuel/tank[0]/level-gal_us", 1);
fuel_node.setDoubleValue(120.0);

# Mathematical adjustment
fuel_node.adjustValue(-15.5);
print("New fuel level: " ~ fuel_node.getValue()); # 104.5

var master_sw = props.globals.getNode("/controls/electric/battery-switch", 1);
master_sw.setBoolValue(1);
master_sw.toggleBoolValue(); # Now 0

```

#### Node Aliasing & Identity

* `.alias(target_node_or_path[, chainListener])`: Dynamically points the node to resolve all reads/writes directly to a separate target property node (essentially creating a pointer alias). Returns 1 on success and 0 on failure. `chainListener` is a boolean value.
* `.unalias()`: Removes an existing alias association, resetting the node to an empty, blank local state.
* `.getAliasTarget()`: Returns a `props.Node` instance pointing to the target node of an active alias.
* `.equals(other_node)`: Returns `1` if both objects wrap the exact same underlying Property Tree coordinate.

```nasal
var virtual_alt = props.Node.new();
virtual_alt.alias("/position/altitude-ft");

# Any reads to virtual_alt will fetch from the real aircraft altitude property
print("Altitude: " ~ virtual_alt.getValue());

```

---

### Part 3: Node Attributes

Nodes carry internal binary flags that control permission and engine processing behaviors:

| Attribute | String Identifier | Purpose |
| --- | --- | --- |
| `READ` | `"readable"` | Determines if Nasal or systems can query the node's data. |
| `WRITE` | `"writable"` | Determines if values can be written to the node. |
| `ARCHIVE` | `"archive"` | Includes the property in basic `"save"` engine dumps. |
| `TRACE_READ` | `"trace-read"` | Generates terminal logger inputs whenever the node is read. |
| `TRACE_WRITE` | `"trace-write"` | Generates terminal logger inputs whenever the node is updated. |
| `USERARCHIVE` | `"userarchive"` | Saves the node configuration directly into the user's flight history file (`autosave.xml`). |
| `PRESERVE` | `"preserve"` | Prevents values from being wiped or reset during aircraft state resets. |

* `.getAttribute([rel_path, ]name)`: Reads specific attribute configurations. If called with zero parameters, it returns the raw integer bitmask representation of all set attributes.
* `.setAttribute([rel_path, ]name, value)`: Sets a specific attribute flag to `1` or `0`. Passing a single combined integer bitmask argument allows configuring multiple attributes simultaneously.

```nasal
var secure_node = props.globals.getNode("/systems/autopilot/internal-gain", 1);

# Lock writing permissions on this node
secure_node.setAttribute("writable", 0);
secure_node.setAttribute("trace-write", 1); # Log write attempts

```

### Part 4: Library Level Utilities

* `props.copy(src_node, dest_node[, copy_attributes])`: Duplicates a source tree hierarchy directly over a destination node. Aliased properties are skipped during copy operations. If `copy_attributes` is set to true, attributes will also be copied. It defaults to false.
* `props.dump(node)`: Recursively prints the entire subnode hierarchy structure, values, and types to the terminal console. Highly intensive; run with caution on large nodes like `props.globals`.
* `props.setAll(base_path, child_path, value)`: Finds all indexed subnodes matching `base_path` and updates the matching relative `child_path` of each to `value` (e.g., setting multi-engine throttle levels).
* `props.nodeList(list_or_nodes)`: Helper that parses arguments (strings, hashes, raw ghosts, functions) and normalizes them into a single linear Nasal vector containing standard `props.Node` references.
* `props.wrap(ghost)` / `props.wrapNode(ghost)`: Standardizes a raw internal C++ `prop` ghost object into a safe, object-oriented `props.Node` instance.

```nasal
# Set 100% throttle across all active engines in FlightGear
props.setAll("/controls/engines/engine", "throttle", 1.0);

```

### Part 5: Condition & Command Engine Bindings

The properties library acts as an bridge to FlightGear's core condition and command systems.

#### Property Conditions

Properties containing nested conditions (e.g., matching `<equals>`, `<and>`, `<greater-than>`) can be parsed and executed directly inside Nasal code:

* `props.compileCondition(node_or_path)`: Pre-compiles an XML structural logic branch. Returns a compiler condition ghost. Execute using `.test()` to get a `1` or `0` result.
* `props.condition(node_or_path)`: Performs a quick, one-time structural condition evaluation. Returns `1` or `0` immediately.

```nasal
# Define a conditional structure matching target criteria
var flight_condition = props.Node.new({
    "and": {
        "greater-than": {
            "property": "/position/altitude-ft",
            "value": 10000
        },
        "equals": {
            "property": "/controls/gear/gear-down",
            "value": 0
        }
    }
});

# Quick evaluation
if (props.condition(flight_condition)) {
    print("Safe cruise configuration verified.");
}

```

#### Run-Time Command Bindings

Action bindings mapped using the `<binding>` block model can be executed programmatically via script:

* `props.runBinding(binding_node[, nasal_module])`: Executes standard flightgear actions (e.g., execution commands like `nasal` or UI controls like `dialog-show`) by pointing to an active property tree representation node.

```nasal
# Trigger UI Map display window directly through property bindings
var map_action = props.Node.new({
    "command": "dialog-show",
    "dialog-name": "map"
});
props.runBinding(map_action);

# Example usage of nasal_module
var tree = {
    "command": "nasal",
    "script": 'print(pi)' # prints value of math.pi
};
var binding = props.Node.new(tree);
props.runBinding(binding, "math");
``` 


### Part 6: Saving & loading PropertyList XML files

PropertyList XML files can be loaded using `io.read_properties` and saved using `io.write_properties`.

**`io.read_properties(path, target = nil, quiet = 0)`**

Load XML file in PropertyList format. Returns the data as a `props.Node` on success or `nil` on error.

If the second, optional `target` parameter is set, then the properties are loaded to this node in the global property tree. Otherwise they are returned as a separate `props.Node` tree. 

Examples:

```nasal
var target = props.globals.getNode("/sim/model");
io.read_properties("/tmp/foo.xml", target);

var data = io.read_properties("/tmp/foo.xml", "/sim/model");
var data = io.read_properties("/tmp/foo.xml");
```

**`io.write_properties(path, prop)`**

Write XML file in PropertyList format. Returns the filename on success or `nil` on error. If the source is a `props.Node` that refers to a node in the main tree, then the data are directly written from the tree, yielding a more accurate result. Otherwise the data need to be copied first, which may slightly change node types (FLOAT becomes DOUBLE etc.)

Examples:

```nasal
var data = props.Node.new({ a:1, b:2, c:{ d:3, e:4 } });
io.write_properties("/tmp/foo.xml", data);
io.write_properties("/tmp/foo.xml", "/sim/model");
```
