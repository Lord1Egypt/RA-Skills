---
name: nasal-library-base
description: Explains the Nasal base libraries, including `clipboard`, `math`, `string`, `utf8` and some built-in functions.
---

## Base Libraries (`clipboard`, `math`, `string`, `utf8`)

Nasal provides robust, low-level libraries to interact with system buffers, compute complex mathematical and trigonometric equations, analyze character attributes, and handle byte-level or UTF-8 multi-byte string manipulations.

### Part 1: Clipboard Access (`clipboard`)

The `clipboard` library facilitates interacting with the host system's primary copy-paste buffers.

#### Buffer Selection Constants

* `clipboard.CLIPBOARD`: The standard, system-wide copy-paste buffer.
* `clipboard.SELECTION`: The X11 system selection buffer (typically populated by highlighting text in Linux/Unix environments).

#### Functions

* `clipboard.getText([type])`: Retrieves the current string content of the specified buffer type (defaults to `clipboard.CLIPBOARD`).
* `clipboard.setText(text[, type])`: Places a string into the designated clipboard buffer. Returns `1` on success, or `0` if the operation fails.

```nasal
# Copy text to the primary clipboard
clipboard.setText("FlightGear Autopilot Active");

# Retrieve text from the clipboard
var content = clipboard.getText();
print("Clipboard contains: " ~ content); # "FlightGear Autopilot Active"

```

### Part 2: Mathematics & Trigonometry (`math`)

The `math` library wraps standard C mathematical utilities, adding array-processing helpers and normalization tools.

#### Constants

* `math.pi`: Value of $\pi$ ($\approx 3.141592653589793$)
* `math.e`: Value of $e$ ($\approx 2.718281828459045$)

#### Core Arithmetic & Rounding

* `math.abs(x)`: Returns the absolute value $\vert{}x\vert{}$.
* `math.sgn(x)`: Signum function. Returns `-1` if $x < 0$, `0` if $x = 0$, or `1` if $x > 0$.
* `math.ceil(x)`: Returns the ceiling of $x$ (smallest integer $\ge x$).
* `math.floor(x)`: Returns the floor of $x$ (largest integer $\le x$).
* `math.round(x[, p])`: Rounds $x$ to the nearest precision step $p$ (defaults to `1`). If the fractional part is exactly `0.5`, it rounds up.
* `math.clamp(x, min, max)`: Restricts $x$ to be within the inclusive range $[\text{min}, \text{max}]$.
* `math.periodic(min, max, x)`: Normalizes $x$ to fit within a continuous periodic domain defined by $[\text{min}, \text{max})$. Excellent for heading/bearing loops.

```nasal
# Compass heading wrap-around (0 to 360)
var raw_heading = -45;
var norm_heading = math.periodic(0, 360, raw_heading); # 315

# Rounding to nearest step
print(math.round(127, 10)); # 130
print(math.round(4.5));     # 5

```

#### Trigonometry (Angles in Radians)

* `math.sin(x)`: Sine of $x$.
* `math.cos(x)`: Cosine of $x$.
* `math.tan(x)`: Tangent of $x$.
* `math.asin(x)`: Arcsine of $x$, returns angle in $[-\frac{\pi}{2}, \frac{\pi}{2}]$.
* `math.acos(x)`: Arccosine of $x$, returns angle in $[0, \pi]$.
* `math.atan2(y, x)`: Two-argument arctangent returning the quadrant-accurate angle in radians $[-\pi, \pi]$.

```nasal
# Convert 45 degrees to radians and get its tangent
var rad = 45 * D2R; 
print("Tan(45 deg): " ~ math.tan(rad)); # 1

```

#### Exponents, Logarithms & Roots

* `math.pow(b, n)`: Returns base $b$ raised to the power of $n$ ($b^n$).
* `math.sqrt(x)`: Returns the square root of $x$ ($\sqrt{x}$).
* `math.exp(x)`: Returns $e^x$.
* `math.ln(x)`: Returns the natural logarithm of $x$ ($\ln x$).
* `math.log10(x)`: Base-10 logarithm of $x$ ($\log_{10} x$).

#### Multi-Argument Utilities

* `math.min(x, y, ...)`: Returns the lowest numeric argument.
* `math.max(x, y, ...)`: Returns the highest numeric argument.
* `math.avg(x, y, ...)`: Returns the mathematical average of all provided numbers.
* `math.fmod(x, y)`: Remainder of $x/y$ preserving mathematical correctness for negative dividends using C’s standard `fmod`.
* `math.mod(x, y)`: Simpler modulo calculation. *Note: Yields mathematically incorrect values when handling negative operands.*

---

### Part 3: Character & String Manipulation (`string`)

The `string` library divides its capabilities between byte-level character classification and high-level string formatters.

#### Character Type Classifiers (Evaluates Character Codes)

These functions analyze a single ASCII character code (number representing a byte) and return boolean $1$ or $0$:

| Function | Checks If ASCII Character Is... |
| --- | --- |
| `string.isalnum()` | Alphanumeric (`A-Z`, `a-z`, `0-9`) |
| `string.isalpha()` | Alphabetic (`A-Z`, `a-z`) |
| `string.isascii()` | Valid ASCII value ($0$ to $127$) |
| `string.isblank()` | Space or horizontal tab (`\t`) |
| `string.iscntrl()` | Control character ($1$ to $31$, or $127$) |
| `string.isdigit()` | Decimal digit (`0-9`) |
| `string.isgraph()` | Visible alphanumeric or punctuation (excludes whitespace) |
| `string.islower()` | Lowercase letter (`a-z`) |
| `string.isupper()` | Uppercase letter (`A-Z`) |
| `string.isprint()` | Printable (visible graphical character or space) |
| `string.ispunct()` | Punctuation character |
| `string.isspace()` | Standard whitespace (`\t`, `\n`, `\v`, `\f`, `\r`, space) |
| `string.isxspace()` | Extended whitespace (adds unique newline bounds to `isspace`) |
| `string.isxdigit()` | Hexadecimal digit (`0-9`, `a-f`, `A-F`) |

```nasal
var char_code = `A`; # Ascii 65
print(string.isupper(char_code)); # 1
print(string.isdigit(char_code)); # 0

```

#### Case Conversions

* `string.toupper(code)`: Converts a single lowercase ASCII character code to its uppercase equivalent.
* `string.tolower(code)`: Converts a single uppercase ASCII character code to its lowercase equivalent.
* `string.uc(str)`: Converts an entire string to uppercase.
* `string.lc(str)`: Converts an entire string to lowercase.

#### String Comparison, Matching & Search

* `cmp(a, b)`: Compare two strings (string type only). Return 0 if they are equal, -1 if `a` is less than `b`, and 1 otherwise.
* `streq(a, b)`: Tests the string values for equality. This is used for pure-numeric strings because the `==` operator tests for numeric equality first.
* `string.icmp(a, b)`: Case-insensitive string comparison. Returns `0` if equal.
* `string.imatch(a, b)`: Case-insensitive matching shortcut. Returns `1` if they match, `0` otherwise.
* `string.match(str, patt)`: Checks if `str` matches shell-style glob pattern `patt`.
* `?` matches any single character.
* `*` matches zero or more arbitrary characters.
* `\` escapes wildcards.
* `[...]` matches any single character in a set (e.g., `[a-z]` or `[^0-9]` for inversion).

```nasal
if (string.match("aircraft-f16.xml", "*[0-9].xml")) {
    print("Matches flight model pattern.");
}

```

#### Splitting, Joining & Trimming

* `split(sep, string)`: Splits a string and returns a vector.
* `string.join(sep, list)`: Joins elements of a vector into a single string using separator `sep`.
* `string.trim(str[, lr[, func]])`: Removes padding characters.
* `lr`: Trim direction ($< 0$ left, $> 0$ right, $0$ or omitted for both).
* `func`: Optional classification function determining what characters to trim (defaults to trimming spaces).


* `string.squeeze(str, length)`: Truncates a string to a target `length` (must be $\ge 7$) by injecting `...` in the middle.
* `string.replace(str, old, new)`: Substitutes all occurrences of `old` substring with `new` inside `str`.
* `string.normpath(path)`: Cleans a file path by eliminating redundant slashes, navigating `.` and `..` levels, and normalizing backslashes `\` to forward slashes `/`.

```nasal
# Trimming digits from the right
var raw_id = "APC-9948";
var clean_id = string.trim(raw_id, 1, string.isdigit); # "APC-"

# Truncating a path string
print(string.squeeze("/usr/share/flightgear/data/aircraft", 15)); # "/us...aircraft"

```

#### Data Parsing & Templating

* `string.scanf(str, format, result_vector)`: Parses values from `str` using a format schema and appends them to a result vector.
* Returns `-1` on structural end mismatch, `0` on outright failure, `1` on partial match, and `2` on exact matches.


* `string.compileTemplate(template)`: Compiles a parameter placeholder string into a callable function. Enables rapid insertions of dynamic hashes into boilerplate strings.

```nasal
# Parsing strings using scanf
var out = [];
string.scanf("comm3freq123.45", "comm%ufreq%f", out);
# out is now [3, 123.45]

# Using templates
var renderUrl = string.compileTemplate("http://map.org/{zoom}/{x}/{y}.png");
var tile_path = renderUrl({ zoom: 12, x: 1200, y: 840 });
# tile_path = "http://map.org/12/1200/840.png"

```

---

### Part 4: Multi-Byte Safe Strings (`utf8`)

When text contains multi-byte Unicode/UTF-8 characters, standard Nasal functions (like `size()` or slicing subscripts) fail because they evaluate raw byte arrays rather than whole characters. The `utf8` library provides safe alternatives.

* `utf8.size(str)`: Returns the true number of UTF-8 unicode characters in `str`, rather than raw bytes.
* `utf8.substr(str, start, len)`: Extracts a substring based on UTF-8 character indices instead of byte coordinates.
* `utf8.strc(str, char_index)`: Returns the numerical unicode point value of the character at `char_index`.
* `utf8.chstr(unicode_val)`: Converts a numerical unicode point value into its UTF-8 string equivalent.
* `utf8.validate(str[, replace_code])`: Tests a string for valid UTF-8 structures. Malformed byte patterns are replaced by the specified replacement character (passed as an ASCII number, defaults to `?` / `63`).

```nasal
var unicode_str = "🛩️ Fly"; # Combines multi-byte characters and standard ASCII

# Standard byte evaluation vs. UTF-8 character count
print("Byte length: ", size(unicode_str));       # Evaluates total raw bytes
print("UTF-8 length: ", utf8.size(unicode_str));  # Correctly identifies character count

# Safe substring extraction
var icon = utf8.substr(unicode_str, 0, 1);

```

---

### Part 5: Other Built-in Functions

#### assert(condition[, message])
Returns either true if the condition evaluates as true, or aborts with a `die()` call.

#### srand()
Initializes the internal random number generator with the current time. No return value.

#### rand()
Returns a random number in the range `[0, 1)`.

#### systime()
Returns the current time with high resolution, which is useful for benchmarking purposes.

#### compile(code[, filename])
Compiles the specified code string and returns a function object bound to the current lexical context. `filename` is used for error messages/logging.

#### closure(func[, level])
Returns the hash table containing the lexical namespace of the given function. The `level` starts at 0 being the namespace of `func`.

#### id(obj)
Returns a string representing the identity of an object.

#### cmdarg()
Returns the property root of certain types of XML files. These could be nodes in the property tree, or temporary and/or non-public nodes outside the property tree. Useful for Nasal embedded in XML files.
