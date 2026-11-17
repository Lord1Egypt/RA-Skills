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
|| `ERR on '&inout' with primitive` | `&inout` not allowed on primitives | Pass by value for reads |
|| `ERR on 'IndexOf' with 2 args` | `string::IndexOf` takes 1 param | Use `SubStr` first for offset |
|| `ERR on 'Text::Format' with 2 values` | `Text::Format` takes 1 value arg | Chain multiple `Text::Format` calls |
|| `No matching symbol 'InsertLast'` on `Json::Value` | JSON arrays use `.Add()` not `.InsertLast()` | Use `messages.Add(item)` for Json::Value arrays |
|| `'ByteAt' is not a member of 'string'` | AngelScript strings lack byte-level access | Use `Text::EncodeHex()` + manual hex parsing for UTF-8 byte access |
|| `No matching symbol 'px'` after refactor | Variables in AngelScript are block-scoped | Declare shared variables at function top, not inside `if` blocks |

---

## 🌐 HTTP + UTF-8 Escaping (ChatBot RAG pattern)

When sending JSON via `Net::HttpRequest` to external APIs (OpenRouter, OpenAI, etc.), non-ASCII characters (Polish diacritics: ą,ć,ę,ł,ń,ó,ś,ź,ż) must be escaped to `\uXXXX` format. The server may reject raw UTF-8 bytes as malformed JSON.

```angelscript
// Convert string to hex, then parse bytes manually
string hexStr = Text::EncodeHex(str);
// ... parse 2-char hex pairs into uint8, decode UTF-8 to code points ...
// Output: \u015b for 'ś', \u0107 for 'ć', etc.
```

Use `Content-Type: application/json; charset=utf-8` header. Always test with Polish text early in development.

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

---

## ⚡ Performance Patterns (from Grid Explorer & Tracker)

### Zero-Allocation Grid Key (bit-packing)

```angelscript
// ❌ BAD: 3 string concatenations = 3 heap allocations per call
string CellKey(int gx, int gy, int gz) {
    return gx + "," + gy + "," + gz;
}

// ✅ GOOD: Single integer → string, one allocation
string CellKey(int gx, int gy, int gz) {
    uint keyVal = (uint(gx + 512) & uint(1023))
                | ((uint(gy + 512) & uint(1023)) << 10)
                | ((uint(gz + 512) & uint(1023)) << 20);
    return tostring(keyVal);
}

// Decode back:
void ParseCellKey(string key, int &out gx, int &out gy, int &out gz) {
    uint keyVal = Text::ParseUInt(key);
    gx = int((keyVal & uint(1023)) - uint(512));
    gy = int(((keyVal >> uint(10)) & uint(1023)) - uint(512));
    gz = int(((keyVal >> uint(20)) & uint(1023)) - uint(512));
}
```

### Pre-Allocated Buffers (no GC stutter)

```angelscript
// Module-level: allocated once, reused every frame
array<vec3> g_CornerBuffer(8);
array<vec2> g_ProjBuffer(8);
array<bool> g_VisibleBuffer(8);

void Draw3DBlock(int gx, int gy, int gz, bool visited) {
    // Fill buffers, project, draw — zero allocations
    for (uint i = 0; i < 8; i++) {
        g_VisibleBuffer[i] = ProjectToScreen(g_CornerBuffer[i], g_ProjBuffer[i]);
    }
}
```

### Single Loop for Multiple Layers

```angelscript
// ❌ BAD: Two separate loops = 2x iteration overhead
for (/*xyz*/) if (visited) Draw3DBlock(..., true);
for (/*xyz*/) if (!visited) Draw3DBlock(..., false);

// ✅ GOOD: One loop, branch inside
for (/*xyz*/) {
    bool isVisited = g_VisitedCells.Exists(CellKey(gx, gy, gz));
    if (isVisited) Draw3DBlock(..., true);
    else if (S_ShowUnvisited) Draw3DBlock(..., false);
}
```

### dt is Milliseconds

```angelscript
// Openplanet Update() passes dt in MILLISECONDS
void Update(float dt) {
    float dtSeconds = dt / 1000.0f;  // Convert to seconds for time tracking
    g_CurrentCellAccum += dtSeconds;
}
```

### Variable Scope in Render()

```angelscript
// ❌ BAD: px/py/pz only exist inside if(S_ShowGrid) block
void Render() {
    if (S_ShowGrid) {
        int px = g_PlayerGX, py = g_PlayerGY, pz = g_PlayerGZ;
        // ...
    }
    // ERROR: px not accessible here for ImGui window
    UI::Text("Position: " + px);
}

// ✅ GOOD: Declare at function top
void Render() {
    int px = g_PlayerGX, py = g_PlayerGY, pz = g_PlayerGZ;
    if (S_ShowGrid) { /* use px/py/pz */ }
    if (S_ShowInfoWindow) { UI::Text("Position: " + px); }
}
```

---

## 🎨 NanoVG UI Patterns (from Grid Explorer)

### Frosted Glass Radar

```angelscript
void DrawRadar() {
    float size = S_RadarSize;
    float posX = S_RadarX * (float(Display::GetWidth()) - size);
    float posY = S_RadarY * (float(Display::GetHeight()) - size);

    // Translucent grey-white background
    nvg::BeginPath();
    nvg::RoundedRect(vec2(posX, posY), vec2(size, size), 6.0f);
    nvg::FillColor(vec4(0.92f, 0.92f, 0.95f, S_RadarBgAlpha * 0.35f));
    nvg::Fill();

    // Cell borders for definition
    nvg::StrokeColor(vec4(0.15f, 0.15f, 0.18f, 0.18f));
    nvg::StrokeWidth(0.8f);
    nvg::Stroke();
}
```

### Animated Forza-Style Alert Banner

```angelscript
void DrawAlert() {
    uint elapsed = Time::Now - g_AlertTime;
    float alpha = 1.0f;
    if (elapsed < 500) alpha = float(elapsed) / 500.0f;      // Fade in
    else if (elapsed > 2500) alpha = 1.0f - float(elapsed-2500)/500.0f; // Fade out

    // Bold text: render twice with 1px offset
    nvg::FontSize(18.0f);
    nvg::Text(vec2(centerX, posY + 18.0f), "NEW BLOCK EXPLORED");
    nvg::Text(vec2(centerX + 1.0f, posY + 18.0f), "NEW BLOCK EXPLORED"); // Bold
}
```

### Heatmap Color Interpolation

```angelscript
vec4 GetHeatmapColor(float intensity, float alpha) {
    intensity = Math::Clamp(intensity, 0.0f, 1.0f);
    if (intensity < 0.5f) {
        float t = intensity * 2.0f;
        return vec4(Math::Lerp(0.10f, 0.10f, t),    // R: blue→green
                     Math::Lerp(0.70f, 0.90f, t),    // G
                     Math::Lerp(0.90f, 0.10f, t),    // B
                     alpha);
    } else {
        float t = (intensity - 0.5f) * 2.0f;
        return vec4(Math::Lerp(0.10f, 0.95f, t),    // R: green→orange
                     Math::Lerp(0.90f, 0.80f, t),    // G
                     Math::Lerp(0.10f, 0.00f, t),    // B
                     alpha);
    }
}
```

---

## 🔌 Public API Namespace Pattern

```angelscript
// Expose functions to other plugins via import
namespace GridExplorer {
    int GetPlayerCellX() {
        if (!S_ExposeApi) return 0;  // Graceful degradation
        return g_PlayerGX;
    }
    bool IsCellVisited(int gx, int gy, int gz) {
        if (!S_ExposeApi) return false;
        return g_VisitedCells.Exists(CellKey(gx, gy, gz));
    }
    // ... more functions
}

// Other plugins import with:
// import int GridExplorer::GetPlayerCellX() from "grid-explorer-dev";
```

---

## 💾 JSON Persistence Pattern

```angelscript
void SaveData() {
    Json::Value root = Json::Object();
    root["total"] = int(g_TotalVisited);
    Json::Value cells = Json::Array();
    array<string> keys = g_VisitedCells.GetKeys();
    for (uint i = 0; i < keys.Length; i++) {
        Json::Value c = Json::Object();
        c["x"] = gx; c["y"] = gy; c["z"] = gz;
        cells.Add(c);
    }
    root["cells"] = cells;
    Json::ToFile(IO::FromStorageFolder("grid-explorer/" + mapUid + ".json"), root);
}
```

---


