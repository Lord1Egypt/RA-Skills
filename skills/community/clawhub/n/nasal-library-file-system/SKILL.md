---
name: nasal-language-file-system
description: Explains the input/output (IO) file handling, property serialization, and directory-path manipulation methods in Nasal, combining raw stream operations ('io') with high-level path parsing wrappers ('os.path').
---

## File System & Path Manipulation (`io` and `os.path`)

Nasal processes files via two distinct systems: the procedural raw byte/line file operations module (`io`) and the high-level object-oriented path utility wrapper (`os.path`).

**Security Note**: All file operations in FlightGear are constrained by security rules. Writing/deleting is normally permitted only within the `$FG_HOME/Export/` directory.

### Part 1: Raw File Operations (`io`)

#### File Streams: Open, Close, and Flush

* `io.open(path[, mode])`: Opens a file stream at `path`. Returns an `iofile` ghost object. `mode` defaults to `"rb"` (read binary).
* `io.close(file)`: Flushes the stream buffer and closes the file pointer. Returns `nil`.
* `io.flush(file)`: Commits volatile cache buffers directly to the hard disk storage immediately without closing the stream descriptor.

| Mode | Purpose | Mode | Purpose (Binary) |
| --- | --- | --- | --- |
| `"r"` | Read-only (must exist) | `"rb"` | Read-only binary |
| `"w"` | Write (truncates existing) | `"wb"` | Write binary |
| `"a"` | Append (creates if missing) | `"ab"` | Append binary |
| `"r+"` | Read/write (must exist) | `"r+b"` | Read/write binary |
| `"w+"` | Read/write (truncates) | `"w+b"` | Read/write binary |
| `"a+"` | Read/write append | `"a+b"` | Read/write append binary |

#### Reading and Writing Data

* `io.readfile(path)`: Loads and returns an entire file as a single string. Throws a runtime exception on failure.
* `io.readln(file)`: Reads a single line, automatically stripping trailing `LF`, `CR`, or `CR+LF` terminators. Returns `nil` at EOF.
* `io.read(file, buf, len)`: Reads exactly `len` bytes into a pre-allocated byte-buffer object (initialized via `bits.buf(size)`). Returns the count of bytes successfully loaded.
* `io.write(file, string)`: Writes raw string data to the stream buffer. Returns the count of bytes written.

```nasal
var path = getprop("/sim/fg-home") ~ "/Export/output.txt";

# Writing data
var out = io.open(path, "w");
io.write(out, "Line 1\nLine 2\n");
io.close(out);

# Reading line-by-line
var instream = io.open(path, "r");
while ((var line = io.readln(instream)) != nil) {
    print("Read: " ~ line);
}
io.close(instream);

```

#### File Location & Pointers

* `io.seek(file, offset, whence)`: Repositions the active cursor inside a stream relative to `whence`:
* `io.SEEK_SET`: Offset relative to file beginning (non-negative).
* `io.SEEK_CUR`: Offset relative to current cursor index.
* `io.SEEK_END`: Offset relative to end of file.


* `io.tell(file)`: Returns the current cursor index position inside the stream.

#### Metadata & Path Utils

* `io.basename(path)`: Returns the final element of a path (e.g., `/a/b.xml` $\rightarrow$ `"b.xml"`).
* `io.dirname(path)`: Returns the parent directory container path containing a trailing slash.
* `io.stat(path)`: Returns a 12-element file metadata vector (`nil` if missing). Indices: `[7]` is total size in bytes, `[9]` is modified timestamp, `[11]` is file type (`"reg"`, `"dir"`, `"lnk"`, etc.).

### Part 2: Property Tree Serialization

Nasal allows fast saving and loading of the FlightGear Property Tree using XML formats:

* `io.read_properties(path[, target])`: Parses a PropertyList XML directly into a `props.Node` container. If `target` is provided (node pointer or path string), the property hierarchy is integrated into that destination.
* `io.write_properties(path, prop_node_or_path)`: Serializes a subset of the Property Tree directly to an XML file.
* `io.readxml(path[, prefix])`: Imports raw XML nodes (not strictly PropertyList format) where attributes map to subnodes named with the given `prefix` (defaults to `"___"`).
* `io.writexml(path, node[, indent[, prefix]])`: Serializes an arbitrary tree structure to raw XML.

```nasal
# Export active position state directly to file
var path = getprop("/sim/fg-home") ~ "/Export/position-dump.xml";
io.write_properties(path, "/position");

```

### Part 3: High-Level Path Object (`os.path`)

The `os.path` utility manages path evaluations, file permissions, structural queries, and physical directory mutation operations.

#### Constructors & Mutation

* `os.path.new([path])`: Instantiates a path object. Defaults to `$FG_ROOT`.
* `os.path.desktop()`: Returns a path object pointing directly to the active system desktop directory.
* `.set(path)`: Updates the underlying string path pointing context.
* `.append(part)`: Joins a directory element (ensuring correct platform directory separators are used).
* `.concat(str)`: Merges raw characters to the end of the string without directory separators.

#### Status Flags & Properties

```nasal
var p = os.path.new(getprop("/sim/fg-home") ~ "/Export/data.txt");

# Booleans
p.exists();     # 1 if physical file exists
p.canRead();    # 1 if read access complies with security limits
p.canWrite();   # 1 if write access complies with security limits
p.isFile();     # 1 if it is a file
p.isDir();      # 1 if it is a directory
p.isAbsolute(); # 1 if it is an absolute path

# String metadata attributes
print(p.realpath);                 # Complete absolute directory path
print(p.file);                     # Filename component ("data.txt")
print(p.dir);                      # Directory folder hierarchy (".../Export")
print(p.base);                     # Absolute path minus final extension (".../data")
print(p.file_base);                # Base filename without extension ("data")
print(p.extension);                # Suffix format ("txt")
print(p.complete_lower_extension); # Full lowercase multi-extension format (e.g. "tar.gz")
print(p.mtime);                    # Modification Unix timestamp integer

```

#### Physical Operations

* `.create_dir()`: Recursively creates the parent directories of the path.
* `.remove()`: Deletes the target file or empty directory from the disk storage.
* `.rename(new_absolute_path)`: Renames or relocates the target element.

```nasal
var folder = os.path.new(getprop("/sim/fg-home") ~ "/Export/archive/log.txt");
folder.create_dir(); # Recursively generates ".../Export/archive" directory

var stream = io.open(folder.realpath, "w");
io.write(stream, "Snapshot data\n");
io.close(stream);

folder.rename(getprop("/sim/fg-home") ~ "/Export/archive/backup.txt");

```
