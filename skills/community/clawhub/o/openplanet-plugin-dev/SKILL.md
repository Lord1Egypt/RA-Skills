---
name: openplanet-plugin-dev
description: Create, debug, and structure Openplanet AngelScript plugins for Trackmania/Maniaplanet. Comprehensive guide with API quirks, AngelScript language pitfalls, performance patterns, and proven templates. Use when building, debugging, or reviewing Openplanet plugins.
version: 2.2.0
metadata:
  openclaw:
    tags: [openplanet, trackmania, angelscript, plugin, game-modding]
---

# 🎮 Openplanet Plugin Development

## 📋 Overview

Openplanet is a plugin/script development platform for Nadeo games (Trackmania 2020, Maniaplanet). Plugins are written in AngelScript (.as), a C++-like scripting language. This skill covers everything from project structure to deep API quirks, performance patterns, and debugging.

> 💡 Hard-won lessons from building: Grid Explorer & Tracker, Event Calendar, Vehicle Detector, Apeiron Galaxy, Competition Companion.

---

## 🏗️ Plugin Architecture (callback-style)

Openplanet plugins can be either:

- **Coroutine-style**: one `void Main()` that loops with `yield()`/`sleep(ms)`
- **Callback-style**: optional `Main()` + auto-called `void Update(float dt)` and `void Render()`

For most overlays, **callback-style is simpler and lower-latency** — you don't need a `Main()` at all. Just define `Update()` and/or `Render()`.

| Callback | When it fires |
|---|---|
| `void Main()` | Plugin load. Yieldable coroutine. |
| `void Update(float dt)` | Every frame. `dt` is delta in milliseconds. |
| `void Render()` | Every frame, even with overlay closed. |
| `void RenderInterface()` | Every frame, only when overlay is open. |
| `void RenderMenu()` | For Openplanet menu items. |
| `void OnEnabled/OnDisabled/OnDestroyed()` | Plugin lifecycle. |
| `void OnSettingsChanged()` | After user changes any `[Setting]` value. |

---

## 📁 Project Layout

### 📂 Folder-based (development) — PREFERRED

```
Openplanet4/Plugins/<plugin-name>/
├── info.toml          # Metadata (required)
├── Main.as            # Entry point (required)
├── src/               # Optional modules
│   ├── core/
│   ├── ui/
│   └── utils/
├── README.md
└── tests/             # Optional Python test scripts
```

All `.as` files in the folder are compiled together as a single module — no manual imports needed.

### 🗂️ Filesystem layout

```
Openplanet4/
├── docs/                  # API documentation
├── Plugins/               # Runtime plugins (what Openplanet loads)
├── Plugins-Developer/     # Source-of-truth development tree
├── PluginStorage/         # Per-plugin persistent data (IO::FromStorageFolder)
└── Openplanet.log         # Debug log — check for compilation errors
```

When iterating, edit `Plugins-Developer/`, then copy to `Plugins/` for live test.

### 📦 Packaged (.op) — distribution

`.op` files are ZIP archives. Do NOT edit them directly — extract, develop as folder, re-zip for release.

Build:

```bash
cd path/to/MyPlugin
7z a MyPlugin.zip info.toml Main.as src/
ren MyPlugin.zip MyPlugin.op  # rename to .op
```

---

## ⚙️ info.toml

```toml
[meta]
name        = "My Plugin"
author      = "yourname"
version     = "1.0.0"
category    = "Tools"

[script]
timeout         = 0
dependencies    = [ "VehicleState", "Camera" ]   # namespaces your code uses
defines         = []                              # Preprocessor defines for dev
```

### 🔗 Common namespaces and which plugin owns them

| Namespace/function | Plugin to add to `dependencies` |
|---|---|
| `VehicleState::ViewingPlayerState()` | `VehicleState` |
| `Camera::ToScreenSpace(vec3) -> vec2` | `Camera` |
| `Camera::IsBehind(vec3) -> bool` | `Camera` |
| `NadeoServices::AddAudience(...)` | `NadeoServices` |
| `Dashboard::ViewingPlayerState()` | `Dashboard` (optional) |

⚠️ **Symptom of missing dependency**: `ERR : No matching symbol 'X::Y'` at compile time.

---

## 🎚️ Settings

```angelscript
[Setting name="Display name" description="Tooltip"]
bool S_MySetting = true;

[Setting name="Slider value" min=0 max=100]
int S_Slider = 50;

[Setting hidden]
string S_InternalData = "";
```

---

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

## ⚡ Performance Patterns

### 🎨 Minimize NVG state changes

Batch draws by state — the single biggest FPS win:

```angelscript
// ❌ BAD: stroke state changes per block
for (each block) {
    nvg::StrokeColor(...);
    nvg::StrokeWidth(...);
    DrawEdgesOfBlock(...);
}

// ✅ GOOD: sort by state, then batch
nvg::StrokeColor(green);  // once per "visited" pass
for (each visited block) DrawEdgesOfBlock(...);
nvg::StrokeColor(red);    // once per "unvisited" pass
for (each unvisited block) DrawEdgesOfBlock(...);
```

State-change guard:

```angelscript
bool g_LastDrewVisited = false;
void ApplyStroke(bool visited) {
    if (visited == g_LastDrewVisited) return;
    g_LastDrewVisited = visited;
    nvg::StrokeColor(visited ? green : red);
    nvg::StrokeWidth(visited ? 3.0f : 2.0f);
}
```

### 🧠 Don't recompute in `Render()`

Anything that can be computed in `Update()` and cached as a global is one less per-frame allocation.

### 👁️ Spatial culling

For 3D grids:
1. **Per-block AABB cull**: project all 8 corners; if 0 in front of camera, skip block
2. **Edge-level cull**: only draw edges whose two endpoints were both visible

### 🔤 Avoid string concatenation in hot loops

`"a" + "b" + "c"` allocates 3 new strings. For cache keys hit thousands of times per frame, cache the per-frame key. For 4–8 char keys, the cost is acceptable — the lookup hash dominates.

---

## 📊 Diagnostic UI

The `UI::*` namespace is immediate-mode (like Dear ImGui):

```angelscript
UI::SetNextWindowSize(width, height, UI::Cond::FirstUseEver);
if (UI::Begin("My Diagnostics")) {
    UI::Text("Static label: " + value);
    if (UI::Button("Reset")) {
        // handle click
    }
    UI::Separator();
}
UI::End();
```

Window titles with icons: `UI::Begin(Icons::Eye + " Diagnostics")`

The `Icons::` namespace has 600+ Unicode glyphs (`Icons::Eye`, `Icons::Cog`, `Icons::Trash`, `Icons::Clock`, `Icons::Car`, `Icons::Info`, `Icons::Calendar`, `Icons::Star`, `Icons::QuestionCircle`, etc.).

### 🗂️ Config & Debug Window Pattern

```angelscript
void RenderDebugWindow() {
    UI::SetNextWindowSize(580, 520, UI::Cond::FirstUseEver);
    if (!UI::Begin("Config", g_ShowDebugWindow)) { UI::End(); return; }
    UI::BeginTabBar("Tabs");
    if (UI::BeginTabItem("Config")) { RenderConfigTab(); UI::EndTabItem(); }
    if (UI::BeginTabItem("Status")) { RenderStatusTab(); UI::EndTabItem(); }
    if (UI::BeginTabItem("History")) { RenderHistoryTab(); UI::EndTabItem(); }
    UI::EndTabBar(); UI::End();
}
```

| Tab | Content |
|---|---|
| ⚙️ Config | All `[Setting]` toggles in a table with ON/OFF |
| 📊 Status | Live values, cache queues, computed data |
| 📜 History | Data tables, map visits, recorded events |
| 📋 Reference | Static reference data (nodes, calibration tables) |

---

## 🌙 Lunar Calendar & Date Conversion

### 📅 Gregorian ↔ Day of Year

```angelscript
// Day of year from Gregorian (1-based)
int GetDayOfYear(int year, int month, int day) {
    int[] daysBefore = {0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334};
    int doy = daysBefore[month] + day;
    if (month > 2 && IsLeapYear(year)) doy++;
    return doy;
}

// Day of year back to Gregorian
void DayOfYearToGregorian(int year, int dayOfYear, int &out month, int &out day) {
    int[] mdays = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (IsLeapYear(year)) mdays[1] = 29;
    month = 1;
    int remaining = dayOfYear;
    for (int i = 0; i < 12; i++) {
        if (remaining <= mdays[i]) { month = i + 1; day = remaining; return; }
        remaining -= mdays[i];
    }
    month = 12; day = 31;
}

// Unix timestamp from Gregorian date (midnight UTC)
uint64 UnixFromGregorian(int year, int month, int day) {
    Time::Info info;
    info.Year = year;
    info.Month = month;
    info.Day = day;
    info.Hour = 0;
    info.Minute = 0;
    info.Second = 0;
    return Time::Unix(info);
}

// Gregorian from Unix timestamp
void GetGregorianFromUnix(uint64 unixTime, int &out year, int &out month, int &out day) {
    Time::Info info = Time::Parse(unixTime);
    year = info.Year;
    month = info.Month;
    day = info.Day;
}

bool IsLeapYear(int year) {
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}
```

### 🌓 Moon phase (synodic ~29.53 days)

```angelscript
// Returns 0.0 (new moon) to 1.0 (next new moon)
float GetMoonPhase(uint64 unixTime) {
    // Known new moon: 2000-01-06 18:14 UTC = 947182440
    const float SYNODIC = 29.53058867;
    double daysSince = double(unixTime - 947182440) / 86400.0;
    return float(fmod(daysSince, SYNODIC) / SYNODIC);
}

// Moon texture for current phase (requires Moon plugin textures)
auto@ GetMoonTexture(uint64 unixTime) {
    float phase = GetMoonPhase(unixTime);
    // 0.0=new, 0.25=first quarter, 0.5=full, 0.75=last quarter
    // Map to your texture array index
    int idx = int(phase * 8.0) % 8;
    return Moon::GetTexture(idx);
}
```

---

## 📆 Calendar Day Indicators

### 🟢 Event dots — mark days that have events

```angelscript
bool[] g_DaysWithEvents;

void Main() {
    g_DaysWithEvents.Resize(31);
    while (true) {
        RebuildEventDays();
        yield();
    }
}

void RebuildEventDays() {
    for (int i = 0; i < 31; i++) g_DaysWithEvents[i] = false;
    Time::Info now = Time::Parse(Time::Stamp);
    int curDOW = GetDayOfWeek(now.Year, now.Month, now.Day);
    // Convert Sun=0 to Mon=1..Sun=7 convention if needed
    curDOW = (curDOW == 0) ? 7 : curDOW;
    int curDay = now.Day;
    for (int i = 0; i < g_EventCount; i++) {
        int diff = g_WeekDay[i] - curDOW;
        int eventDay = curDay + diff;
        if (eventDay >= 1 && eventDay <= 31) g_DaysWithEvents[eventDay - 1] = true;
    }
}
```

In your calendar draw loop:

```angelscript
// Highlight days with event dots
if (g_DaysWithEvents[day - 1])
    UI::PushStyleColor(UI::Col::Button, vec4(0.4f, 0.8f, 0.4f, 0.25f));
UI::Button(dayStr);
if (g_DaysWithEvents[day - 1])
    UI::PopStyleColor();
```

### 📊 Inline data in cells — show computed value without hover

```angelscript
// In each calendar cell, after drawing the day number button:
UI::TextDisabled(Text::Format("%.0f%%", progress * 100.0));  // e.g. "23%" = 23%

// Moon phase icon alongside:
auto@ tex = GetMoonTexture(Time::Stamp);
if (tex !is null) {
    UI::SameLine();
    UI::Image(tex, vec2(14, 14));
}
```

---

## ⏱️ Upcoming Events Countdown

```angelscript
array<int64> eTs; array<string> eLabel;

void BuildUpcomingList() {
    eTs.Resize(0);
    eLabel.Resize(0);
    int64 now = Time::Stamp;
    for (int i = 0; i < g_Count; i++) {
        int64 ets = GetNextEventTs(g_WeekDay[i], g_Hour[i], g_Min[i]);
        if (ets > now) {
            eTs.InsertLast(ets);
            eLabel.InsertLast(g_Label[i]);
        }
    }
    // Bubble sort by timestamp (ascending)
    for (uint i = 0; i < eTs.Length - 1; i++) {
        for (uint j = 0; j < eTs.Length - 1 - i; j++) {
            if (eTs[j] > eTs[j + 1]) {
                int64 tmpT = eTs[j]; eTs[j] = eTs[j + 1]; eTs[j + 1] = tmpT;
                string tmpL = eLabel[j]; eLabel[j] = eLabel[j + 1]; eLabel[j + 1] = tmpL;
            }
        }
    }
}

// Display first 5 in UI:
void RenderUpcoming() {
    BuildUpcomingList();
    uint count = eTs.Length;
    if (count > 5) count = 5;
    for (uint i = 0; i < count; i++) {
        int64 ago = eTs[i] - Time::Stamp;
        string countdown = FormatCountdown(ago);
        UI::Text(eLabel[i] + " — " + countdown);
    }
}

string FormatCountdown(int64 seconds) {
    int h = int(seconds / 3600);
    int m = int((seconds % 3600) / 60);
    return Text::Format("%dh %dm", h, m);
}
```

---

## 🔁 Recurring Events Pattern

```angelscript
const int MAX_EVENTS = 16;
int g_Count = 0;
int[] g_WeekDay; int[] g_Hour; int[] g_Min; string[] g_Label;

void AddEvent(int d, int h, int m, const string &in l) {
    if (g_Count >= MAX_EVENTS) return;
    g_WeekDay[g_Count] = d; g_Hour[g_Count] = h;
    g_Min[g_Count] = m; g_Label[g_Count] = l; g_Count++;
}
```

⏱️ Upcoming events with countdown:

```angelscript
array<int64> eTs; array<string> eLabel;
for (int i = 0; i < g_EventCount; i++) {
    int64 ets = GetNextEventTs(g_WeekDay[i], g_Hour[i], g_Min[i]);
    if (ets > now) { eTs.InsertLast(ets); eLabel.InsertLast(g_Label[i]); }
}
// Bubble sort, display first 5
```

---

## 🔀 Preprocessor Directives

```angelscript
#if TMNEXT
    // Trackmania (2020) only
#elif MP4
    // Maniaplanet 4 only
#endif
```

---

## 🐛 Common Build/Compile Errors

| Error message | Cause | Fix |
|---|---|---|
| `ERR : No matching symbol 'X::Y'` at function call | Missing `dependencies` in `info.toml` | Add the owning plugin to `[script].dependencies` |
| `ERR : Unexpected token '<identifier>'` after numeric literal | Integer suffix (`u`, `l`, etc.) not supported | Drop suffix or use `uint64(x)` cast |
| `ERR : Expected '(' Instead found '['` on `const TYPE name[N]` | `const` on fixed-size value-type array | Use `TYPE[] name = { ... };` (dynamic, no const) |
| `ERR : Expected ';' Instead found identifier 'pts'` on `vec2 pts[8];` | Local fixed-size array not supported | Use individual variables |
| `ERR : No matching signatures to 'dictionary::Exists(uint64)'` | Dictionary only takes string keys | Convert to `string` key |
| `WARN : Signed/Unsigned mismatch` in `for` loop | `int i` vs `uint Length` | Use `uint i` |
| `ERR : Can't implicitly convert from 'vec2' to 'vec3'` | `Camera::ToScreenSpace` returns `vec2` | Use `vec2`; test `Camera::IsBehind` for cull |
| `'year' is not a member of 'Time::Info'` | Wrong case on member | Use PascalCase: `info.Year`, `info.Month`, `info.Day`, etc. |
| `'Weekday' is not a member of 'Time::Info'` | Weekday doesn't exist on Time::Info | Use Zeller's formula (see Time API section) |
| `No matching symbol 'UI::Font::...'` | Font enum doesn't exist | Use `PushFontSize`/`PopFontSize` |
| `No matching symbol 'UI::TextColored'` | Function doesn't exist | Use `PushStyleColor(UI::Col::Text, ...)` |
| `Float value truncated in implicit conversion` | float where int expected | Cast: `int(value)` |
| `ERR : No matching symbol 'outDepth'` | `out` param name mismatch | Match parameter name exactly |
| `ERR : Can't implicitly convert from 'string' to 'bool'` | `UI::InputText` return in `if()` | Call separately, check `changed` bool after |
| `ERR on '&inout' with primitive` | `&inout` not allowed on primitives | Pass by value for reads |
| `ERR on 'IndexOf' with 2 args` | `string::IndexOf` takes 1 param | Use `SubStr` first for offset |
| `ERR on 'Text::Format' with 2 values` | `Text::Format` takes 1 value arg | Chain multiple `Text::Format` calls |

---

## 🔧 Debugging Tips

- 📝 **`F3 → Log`** — `print("hello")` lands here
- 🔄 **Reload scripts** after every save via `F3 → Developer → Reload Scripts` — no restart needed
- 📋 **F3 → Developer → Plugin Manager** — shows load order and compile errors
- 🔍 **Nod Explorer** (`F3 → Developer → Nod Explorer`) — browse live `CGameCtnApp` tree
- 📄 **Openplanet.log** (`%USERPROFILE%\OpenplanetNext\Openplanet.log`) — stack traces for runtime crashes

---

## 🚀 Quick-Start Template

```toml
# info.toml
[meta]
name        = "My Plugin"
author      = "Me"
category    = "Tools"
version     = "1.0.0"

[script]
timeout         = 0
dependencies    = [ "VehicleState" ]
```

```angelscript
// main.as
[Setting name="Enabled" category="General"]
bool S_Enabled = true;

void Update(float dt) {
    if (!S_Enabled) return;
    auto state = VehicleState::ViewingPlayerState();
    if (state is null) return;
    // ... per-frame work ...
}

void Render() {
    if (!S_Enabled) return;
    if (UI::Begin(Icons::Cog + " My Plugin")) {
        UI::Text("Hello world");
    }
    UI::End();
}
```

---

## 🧹 Cleanup When Removing a Feature

Check EVERY `.as` file:

```bash
grep -rn "DeletedName" Plugins/<name>/
```

---

## 📚 Reference

Full API reference: 🌐 **https://openplanet.dev/docs**

Hermes skills repo reference files: 📎 https://github.com/tomekdot/hermes-skills/tree/main/skills/software-development/openplanet-plugin-dev/references

---

*Last updated: 2026-06-12. Covers AngelScript build as of OpenplanetNext 2026.*
