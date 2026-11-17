## 🚨 CRITICAL — API Quirks & Pitfalls

### 🔤 AngelScript Language Quirks

These bite everyone. AngelScript ≠ C++, ≠ C#, ≠ Java.

#### 🔢 Integer literal suffixes

`u`, `l`, `ul`, `ull` suffixes are **not supported**.

```angelscript
// ❌ ERR: Unexpected token '<identifier>'
const uint64 MASK = 0x3FFFFFFu;
const int BIG = 1ul;

// ✅ OK: bare literal; compiler picks the type
const uint64 MASK = 0x3FFFFFF;
const int BIG = 1;
const uint64 KEY = uint64(0x123);     // explicit cast
```

#### 📐 `const` on value-type arrays

`const` works for primitives, but **NOT for fixed-size arrays of value types** like `int2[]` or `vec3[]`.

```angelscript
// ❌ ERR: Expected '('
const int2 EDGES[12] = { int2(0,1), ... };
const vec3 CORNERS[8] = { ... };

// ✅ OK: dynamic, no const
int2[] g_Edges = { int2(0,1), ... };
```

Also: `const` on `array<T>` is unreliable — keep globals un-`const` and use a `g_` prefix instead.

#### 📏 Fixed-size local arrays

**Local fixed-size arrays are not supported**:

```angelscript
void Foo() {
    // ❌ ERR: Expected ';' Instead found identifier 'pts'
    vec2 pts[8];
    float depth[8];
}

// ✅ WORKAROUND: individual variables
void Foo() {
    vec2 p0, p1, p2, p3, p4, p5, p6, p7;
    // compiler will register-allocate them
}
```

Or use dynamic arrays:

```angelscript
vec2[] GetCorners() {
    vec2[] cs = { vec2(0,0), vec2(1,0), ... };
    return cs;
}
```

#### 🗝️ `dictionary` key types

**Most surprising limitation**: `dictionary` only accepts `const string&in` keys.

```angelscript
dictionary d;

// ❌ ERR: No matching signatures to 'dictionary::Exists(uint64)'
d[uint64(123)] = true;
d[int(456)]    = true;

// ✅ OK: build a string key
d["123"] = true;
d[gx + "," + gy + "," + gz] = true;
```

If you need a fast non-string key, roll your own hash table (parallel arrays + linear scan, or small open-addressed probe table). For most plugins, `string` keys are fine.

#### 🔀 `uint` vs `int` in comparisons

`array<T>.Length` returns `uint`. Comparing a signed `int` loop counter produces a warning treated as error in strict mode:

```angelscript
// ⚠️ WARN: Signed/Unsigned mismatch
for (int e = 0; e < arr.Length; e++) { ... }

// ✅ CLEAN:
for (uint e = 0; e < arr.Length; e++) { ... }
```

#### 📤 `out` parameter naming

Match the parameter name **exactly**:

```angelscript
// ❌ ERR: No matching symbol 'outDepth'
bool Project(vec3 &in p, vec2 &out screen, float &out depth) {
    outDepth = 0.0f;
}

// ✅ OK:
bool Project(vec3 &in p, vec2 &out screen, float &out depth) {
    depth = 0.0f;
}
```

#### 🎨 `int2`, `vec2`, `vec3`, `vec4` constructors

```angelscript
int2 a = int2(1, 2);
vec3 v = vec3(1.0f, 2.0f, 3.0f);
vec4 red = vec4(1.0f, 0.0f, 0.0f, 0.5f);
```

They are value types — no `@` needed for storage.

#### 🔄 `&inout` on primitive types is NOT allowed

```angelscript
// ❌ ERR:
void ConfigRow(const string &in label, bool &inout value) { }

// ✅ OK:
void ConfigRow(const string &in label, bool value) { }
```

#### 📊 Array initialization — inline `int t[] = {...}` fails inside functions

```angelscript
// ❌ ERR inside functions:
// int t[] = {0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4};

// ✅ OK: use array<T> with InsertLast
array<int64> items;
items.InsertLast(123);

// ✅ OK: pre-allocate at global scope
int[] g_Array;
void Main() { g_Array.Resize(16); }

// ✅ OK: inline array init works at global scope
int[] monthDays = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
```

#### 🔍 `string::IndexOf` — takes exactly ONE parameter

```angelscript
// ❌ ERR:
int idx = text.IndexOf("[", startPos);

// ✅ OK:
int idx = text.IndexOf("[");
// For offset: use SubStr first
int idx = text.SubStr(startPos).IndexOf("[");
```

#### 📝 `Text::Format` takes exactly ONE value argument

```angelscript
// ❌ ERR:
Text::Format("%.6f (%.2f%%)", sidereal, sidereal * 100.0);

// ✅ OK:
Text::Format("%.6f", sidereal) + " (" + Text::Format("%.2f%%", sidereal * 100.0) + ")";
```

---

### ⏰ Time API Quirks

#### 🅰️ Time::Info uses PascalCase, NOT lowercase

`'year' is not a member of 'Time::Info'`

```angelscript
// ❌ ERR:
info.year, info.month, info.day, info.hour, info.minute, info.second

// ✅ OK:
info.Year, info.Month, info.Day, info.Hour, info.Minute, info.Second
```

#### 📅 Weekday is NOT a member of Time::Info

`info.Weekday` will fail. Use **Zeller's formula** (0=Sun..6=Sat):

```angelscript
int GetDayOfWeek(int y, int m, int d) {
    if (m < 3) { m += 12; y -= 1; }
    int K = y % 100;
    int J = y / 100;
    int h = (d + (13 * (m + 1)) / 5 + K + K / 4 + J / 4 + 5 * J) % 7;
    return (h + 6) % 7; // 0=Sun
}
```

#### 🕐 Time functions

```angelscript
int64 now = Time::Stamp;                          // Epoch seconds
uint64 gameTime = Time::Now;                      // ms since game start
string formatted = Time::FormatString("%H:%M", now);  // strftime format
Time::Info info = Time::Parse(now);               // Local time
```

---

### 🖥️ UI API Quirks

#### 🔤 No UI::Font enum — use PushFontSize

```angelscript
// ✅ OK:
UI::PushFontSize(22.0);
UI::Text("Big text");
UI::PopFontSize();

// ❌ ERR (does not exist):
UI::PushFont(UI::Font::OpenSansBold);
```

#### 🎨 No UI::TextColored — use PushStyleColor

```angelscript
// ✅ OK:
UI::PushStyleColor(UI::Col::Text, vec4(0.3f, 1.0f, 0.5f, 1.0f));
UI::Text("Green text");
UI::PopStyleColor();

// ❌ ERR:
UI::TextColored(color, "text");
```

#### 📍 Window position uses int coords

```angelscript
// ✅ OK (cast floats to int):
UI::SetNextWindowPos(int(posX), int(posY), UI::Cond::Appearing);
```

#### 🪟 UI::Begin takes a bool reference

```angelscript
bool S_WindowOpen = false;
if (!UI::Begin("My Window", S_WindowOpen, UI::WindowFlags::NoSavedSettings)) {
    UI::End();
    return;
}
```

#### ⌨️ UI::InputText — return type vs. bool&out

```angelscript
// ❌ ERR — InputText ALWAYS returns string, can't use in if():
if (UI::InputText("##Input", g_Text, changed, flags)) { }

// ✅ OK:
bool changed = false;
UI::InputText("##Input", g_Text, changed, flags);
if (changed) { /* Enter was pressed */ }
```

---

### 🖌️ NanoVG Essentials

The drawing API is per-frame immediate-mode. State persists until changed.

```angelscript
nvg::BeginPath();
nvg::MoveTo(p1);
nvg::LineTo(p2);
nvg::Stroke();          // ← actually draws the path

nvg::FontSize(13.0f);
nvg::FillColor(vec4(1.0f, 1.0f, 1.0f, 0.9f));
nvg::TextAlign(nvg::Align::Middle | nvg::Align::Center);
nvg::Text(p, "label");
```

- `nvg::BeginPath()` is **required** for `LineTo`/`Rect`/`Circle`/etc.
- `nvg::Text()` does **NOT** need `BeginPath`.
- For minimum state changes, batch draws that share a state.

---

### 📷 Camera API

#### 🎯 Camera::ToScreenSpace returns `vec2`, not `vec3`

```angelscript
vec2 screenPos = Camera::ToScreenSpace(worldPos);   // 2D only
// NO z/depth component!
```

For behind-camera test:

```angelscript
if (Camera::IsBehind(worldPos)) {
    // skip this point
}
```

⚠️ Don't assume a `vec3` overload exists. The `vec2` return is the only signature.

#### 🚗 VehicleState::ViewingPlayerState() returns CSmPlayer

```angelscript
auto state = VehicleState::ViewingPlayerState();
if (state is null) return;       // null when not in a vehicle / not in a map
vec3 pos = state.Position;        // world-space player position
```

Use `is null` — AngelScript's null-comparison operator for handles.

---

### 🧱 Trackmania Block Dimensions

Standard blocks are **32 × 32 × 8** (X × Z × Y) in world units.

```angelscript
const float BLOCK_XZ = 32.0f;
const float BLOCK_Y  = 8.0f;

int gx = int(Math::Floor(worldPos.x / BLOCK_XZ));
int gy = int(Math::Floor(worldPos.y / BLOCK_Y));
int gz = int(Math::Floor(worldPos.z / BLOCK_XZ));
```

---

