# Openplanet API Reference - Namespaces

Source: https://openplanet.dev/docs/api

## List of all namespaces (as of Openplanet 1.29.5)

| Namespace | Description |
|-----------|-------------|
| `// Global namespace` | Global functions |
| `namespace UI` | UI tools (ImGui) |
| `namespace nvg` | NanoVG drawing |
| `namespace Audio` | Audio playback |
| `namespace Auth` | Third-party API authentication |
| `namespace Crypto` | Cryptography and hashing |
| `namespace Display` | Display functions |
| `namespace Fids` | Game files and folders |
| `namespace IO` | Filesystem I/O |
| `namespace Icons` | Icon helpers |
| `namespace Json` | JSON serialization |
| `namespace Math` | Math functions |
| `namespace Net` | Networking and sockets |
| `namespace Path` | File path operations |
| `namespace Permissions` | Trackmania permission checks |
| `namespace Regex` | Regular expressions |
| `namespace SQLite` | SQLite database access |
| `namespace Settings` | Openplanet settings |
| `namespace Tests` | Testing utilities |
| `namespace Text` | Text parsing and formatting |
| `namespace Time` | Date and time |
| `namespace XML` | XML deserialization |
| `namespace mat3` | 3x3 matrix |
| `namespace mat4` | 4x4 matrix |
| `namespace string` | String static functions |
| `namespace Reflection` | Type reflection |
| `namespace Discord` | Discord rich presence |
| `namespace Meta` | Openplanet meta API |
| `namespace Import` | DLL import |
| `namespace Dev` | Advanced memory access |
| `namespace Internal` | Internal/built-in use only |

## UI Namespace - Key Functions (AngelScript)

From global namespace:
- `bool UI::Begin(string name, bool* open = nil, UI.WindowFlags flags = 0)` - Begin window
- `void UI::End()` - End window
- `bool UI::BeginChild(string id, vec2 size = {0,0}, bool border = false, UI.WindowFlags flags = 0)`
- `void UI::EndChild()`
- `void UI::Text(string text)`
- `void UI::TextColored(vec4 color, string text)` - NOTE: Does NOT exist in Openplanet AngelScript! Use PushStyleColor instead
- `void UI::TextDisabled(string text)`
- `void UI::TextWrapped(string text)`
- `void UI::LabelText(string label, string text)`
- `bool UI::Button(string label, vec2 size = {0,0})`
- `bool UI::SmallButton(string label)`
- `bool UI::Checkbox(string label, bool* value)`
- `bool UI::RadioButton(string label, bool active)`
- `bool UI::InputText(string label, string* buffer, int bufferSize, UI.InputTextFlags flags = 0)` - Returns true if text changed
- `bool UI::Combo(string label, int* currentItem, string[] items)`
- `bool UI::SliderFloat(string label, float* value, float min, float max, string format = "%.3f")`
- `bool UI::SliderInt(string label, int* value, int min, int max, string format = "%d")`
- `bool UI::DragFloat(string label, float* value, float speed = 1.0, float min = 0, float max = 0)`
- `bool UI::ColorEdit3(string label, float[3] color, UI.ColorEditFlags flags = 0)`
- `bool UI::ColorEdit4(string label, float[4] color, UI.ColorEditFlags flags = 0)`
- `bool UI::TreeNode(string label)`
- `void UI::TreePop()`
- `bool UI::Selectable(string label, bool selected = false)`
- `bool UI::ListBox(string label, int* currentItem, string[] items)`
- `void UI::ProgressBar(float fraction, vec2 size = {-1,0}, string overlay = "")`
- `void UI::BulletText(string text)`
- `void UI::Separator()`
- `void UI::SameLine()`
- `void UI::Spacing()`
- `void UI::Dummy(vec2 size)`
- `void UI::PushItemWidth(float width)`
- `void UI::PopItemWidth()`
- `void UI::SetNextWindowPos(int x, int y, UI.Cond condition = UI.Cond::FirstUseEver)`
- `void UI::SetNextWindowSize(int w, int h, UI.Cond condition = UI.Cond::FirstUseEver)`
- `void UI::PushStyleColor(UI.Col idx, vec4 color)`
- `void UI::PopStyleColor()`
- `void UI::PushFontSize(float size)`
- `void UI::PopFontSize()`
- `void UI::BeginTabBar(string id)`
- `void UI::EndTabBar()`
- `bool UI::BeginTabItem(string label)`
- `void UI::EndTabItem()`
- `void UI::BeginTable(string id, int columns, UI.TableFlags flags = 0)`
- `void UI::EndTable()`
- `void UI::TableNextRow()`
- `void UI::TableSetColumnIndex(int col)`
- `void UI::Image(string texturePath, vec2 size)`

## UI::InputText - CRITICAL

The documentation shows:
```angelscript
bool UI::InputText(string label, string* buffer, int bufferSize, UI.InputTextFlags flags = 0)
```

But in practice (Openplanet 1.29.5), the compiler shows these overloads:
```angelscript
string UI::InputText(const string&in label, string str, int flags = UI::InputTextFlags::None, UI::InputTextCallback@ callback = null)
string UI::InputText(const string&in label, string str, bool&out changed, int flags = UI::InputTextFlags::None, UI::InputTextCallback@ callback = null)
```

Both return `string`, NOT `bool`. The `bool&out changed` parameter is set to true when Enter is pressed.

**Working pattern:**
```angelscript
bool changed = false;
UI::InputText("##Input", g_Text, changed, UI::InputTextFlags::EnterReturnsTrue);
if (changed) {
    // Enter was pressed, g_Text contains the input
}
```

## UI::Col enum values

- `UI::Col::Text`
- `UI::Col::TextDisabled`
- `UI::Col::WindowBg`
- `UI::Col::ChildBg`
- `UI::Col::PopupBg`
- `UI::Col::Border`
- `UI::Col::FrameBg`
- `UI::Col::FrameBgHovered`
- `UI::Col::FrameBgActive`
- `UI::Col::TitleBg`
- `UI::Col::TitleBgActive`
- `UI::Col::MenuBarBg`
- `UI::Col::ScrollbarBg`
- `UI::Col::ScrollbarGrab`
- `UI::Col::ScrollbarGrabHovered`
- `UI::Col::ScrollbarGrabActive`
- `UI::Col::CheckMark`
- `UI::Col::SliderGrab`
- `UI::Col::SliderGrabActive`
- `UI::Col::Button`
- `UI::Col::ButtonHovered`
- `UI::Col::ButtonActive`
- `UI::Col::Header`
- `UI::Col::HeaderHovered`
- `UI::Col::HeaderActive`
- `UI::Col::Separator`
- `UI::Col::SeparatorHovered`
- `UI::Col::SeparatorActive`
- `UI::Col::ResizeGrip`
- `UI::Col::Tab`
- `UI::Col::TabHovered`
- `UI::Col::TabActive`
- `UI::Col::PlotLines`
- `UI::Col::PlotLinesHovered`
- `UI::Col::PlotHistogram`
- `UI::Col::PlotHistogramHovered`
- `UI::Col::TextSelectedBg`
- `UI::Col::ModalWindowDimBg`

## UI::WindowFlags enum values

- `UI::WindowFlags::None`
- `UI::WindowFlags::NoTitleBar`
- `UI::WindowFlags::NoResize`
- `UI::WindowFlags::NoMove`
- `UI::WindowFlags::NoScrollbar`
- `UI::WindowFlags::NoScrollWithMouse`
- `UI::WindowFlags::NoCollapse`
- `UI::WindowFlags::AlwaysAutoResize`
- `UI::WindowFlags::NoBackground`
- `UI::WindowFlags::NoSavedSettings`
- `UI::WindowFlags::NoMouseInputs`
- `UI::WindowFlags::MenuBar`
- `UI::WindowFlags::HorizontalScrollbar`
- `UI::WindowFlags::NoFocusOnAppearing`
- `UI::WindowFlags::NoBringToFrontOnFocus`
- `UI::WindowFlags::AlwaysVerticalScrollbar`
- `UI::WindowFlags::AlwaysHorizontalScrollbar`
- `UI::WindowFlags::AlwaysUseWindowPadding`
- `UI::WindowFlags::NoNavInputs`
- `UI::WindowFlags::NoNavFocus`

## UI::InputTextFlags enum values

- `UI::InputTextFlags::None`
- `UI::InputTextFlags::CharsDecimal`
- `UI::InputTextFlags::CharsHexadecimal`
- `UI::InputTextFlags::CharsUppercase`
- `UI::InputTextFlags::CharsNoBlank`
- `UI::InputTextFlags::AutoSelectAll`
- `UI::InputTextFlags::EnterReturnsTrue`
- `UI::InputTextFlags::CallbackCompletion`
- `UI::InputTextFlags::CallbackHistory`
- `UI::InputTextFlags::CallbackAlways`
- `UI::InputTextFlags::CallbackCharFilter`
- `UI::InputTextFlags::AllowTabInput`
- `UI::InputTextFlags::CtrlEnterForNewLine`
- `UI::InputTextFlags::NoHorizontalScroll`
- `UI::InputTextFlags::AlwaysOverwrite`
- `UI::InputTextFlags::ReadOnly`
- `UI::InputTextFlags::Password`
- `UI::InputTextFlags::NoUndoRedo`

## UI::Cond enum values

- `UI::Cond::None`
- `UI::Cond::Always`
- `UI::Cond::Once`
- `UI::Cond::FirstUseEver`
- `UI::Cond::Appearing`

## UI::TableFlags enum values

- `UI::TableFlags::None`
- `UI::TableFlags::Resizable`
- `UI::TableFlags::Reorderable`
- `UI::TableFlags::Hideable`
- `UI::TableFlags::Sortable`
- `UI::TableFlags::NoSavedSettings`
- `UI::TableFlags::ContextMenuInBody`
- `UI::TableFlags::RowBg`
- `UI::TableFlags::BordersInnerH`
- `UI::TableFlags::BordersOuterH`
- `UI::TableFlags::BordersInnerV`
- `UI::TableFlags::BordersOuterV`
- `UI::TableFlags::BordersH`
- `UI::TableFlags::BordersV`
- `UI::TableFlags::BordersInner`
- `UI::TableFlags::BordersOuter`
- `UI::TableFlags::Borders`
- `UI::TableFlags::NoBordersInBody`
- `UI::TableFlags::NoBordersInBodyUntilResize`
- `UI::TableFlags::SizingFixedFit`
- `UI::TableFlags::SizingFixedSame`
- `UI::TableFlags::SizingStretchProp`
- `UI::TableFlags::SizingStretchSame`
- `UI::TableFlags::NoHostExtendX`
- `UI::TableFlags::NoHostExtendY`
- `UI::TableFlags::NoKeepColumnsVisible`
- `UI::TableFlags::PreciseWidths`
- `UI::TableFlags::NoClip`
- `UI::TableFlags::PadOuterX`
- `UI::TableFlags::NoPadOuterX`
- `UI::TableFlags::NoPadInnerX`
- `UI::TableFlags::ScrollX`
- `UI::TableFlags::ScrollY`
- `UI::TableFlags::SortMulti`
- `UI::TableFlags::SortTristate`

## Time Namespace

Properties:
- `int64 Time::Stamp` - Current Unix timestamp in seconds
- `uint64 Time::Now` - Milliseconds since game start
- `uint64 Time::FrameCount` - Frame counter

Functions:
- `string Time::FormatString(const string&in format, int64 stamp = -1)` - strftime format, local time
- `string Time::FormatStringUTC(const string&in format, int64 stamp = -1)` - strftime format, UTC
- `int64 Time::ParseFormatString(const string&in format, const string&in stamp)` - Parse time from string
- `string Time::Format(uint64 time, bool fractions = true, bool forceMinutes = true, bool forceHours = false, bool short = false)` - Race time format (e.g. "1:01.234")
- `uint64 Time::ParseRelativeTime(const string&in time)` - Parse race time to ms
- `Time::Info Time::Parse(int64 stamp = -1)` - Parse to Time::Info (local)
- `Time::Info Time::ParseUTC(int64 stamp = -1)` - Parse to Time::Info (UTC)

Time::Info members (PascalCase!):
- `int Year`
- `int Month`
- `int Day`
- `int Hour`
- `int Minute`
- `int Second`
- `int DayOfWeek` (0=Sunday)

## Text Namespace

Functions:
- `int Text::ParseInt(const string&in str, int base = 10)`
- `int64 Text::ParseInt64(const string&in str, int base = 10)`
- `uint Text::ParseUInt(const string&in str, int base = 10)`
- `float Text::ParseFloat(const string&in str)`
- `double Text::ParseDouble(const string&in str)`
- `vec4 Text::ParseHexColor(string str)` - e.g. "#FF0000"
- `string Text::Format(const string&in format, <type> value)` - Single value only!
- `string Text::StripFormatCodes(const string&in s)` - Strip Mania formatting codes ($f00 etc)
- `string Text::FormatGameColor(const vec3&in rgb)` - Format as $f00
- `string Text::FormatOpenplanetColor(const vec3&in rgb)` - Format as \$f00
- `string Text::EncodeHex(const string&in, bool upper = false)`
- `string Text::DecodeHex(const string&in)`
- `string Text::EncodeBase64(const string&in, bool url = false)`
- `string Text::DecodeBase64(const string&in, bool url = false)`

## IO Namespace

Functions:
- `string IO::FromStorageFolder(const string&in filename)` - Plugin storage path
- `string IO::FromDataFolder(const string&in filename)` - Openplanet data folder
- `string IO::FromAppFolder(const string&in filename)` - Game install folder
- `string IO::FromUserGameFolder(const string&in filename)` - User game folder
- `bool IO::FileExists(const string&in filename)`
- `uint64 IO::FileSize(const string&in filename)`
- `int64 IO::FileCreatedTime(const string&in filename)`
- `int64 IO::FileModifiedTime(const string&in filename)`
- `void IO::Delete(const string&in filename)`
- `void IO::Copy(const string&in path, const string&in target)`
- `void IO::Move(const string&in path, const string&in target)`
- `bool IO::FolderExists(const string&in path)`
- `void IO::CreateFolder(const string&in path, bool recursive = true)`
- `void IO::DeleteFolder(const string&in path, bool recursive = false)`
- `string[]@ IO::IndexFolder(const string&in path, bool recursive)`

## Meta Namespace

Functions:
- `Meta::Plugin@ Meta::ExecutingPlugin()` - Current plugin handle
- `Meta::Plugin@[]@ Meta::AllPlugins()` - All loaded plugins
- `Meta::Plugin@ Meta::GetPluginFromID(const string&in id)` - Get plugin by ID
- `void Meta::UnloadPlugin(Plugin@ plugin)` - Queue plugin unload
- `void Meta::ReloadPlugin(Plugin@ plugin)` - Queue plugin reload
- `void Meta::OpenSettings(Plugin@ plugin = null)` - Open settings window
- `void Meta::SaveSettings()` - Force save settings
- `bool Meta::IsDeveloperMode()` - Check dev mode
- `string Meta::OpenplanetVersion()` - Get Openplanet version
- `string Meta::OpenplanetBuildInfo()` - Get build info
- `void Meta::Terminate()` - Exit game

## Net Namespace

Functions:
- `Net::HttpRequest@ Net::HttpGet(const string&in url)`
- `Net::HttpRequest@ Net::HttpPost(const string&in url, const string&in data = "", const string&in contentType = "application/x-www-form-urlencoded")`
- `Net::HttpRequest@ Net::HttpHead(const string&in url)`
- `Net::HttpRequest@ Net::HttpPut(const string&in url, const string&in data = "", const string&in contentType = "application/x-www-form-urlencoded")`
- `Net::HttpRequest@ Net::HttpDelete(const string&in url)`
- `Net::HttpRequest@ Net::HttpPatch(const string&in url, const string&in data = "", const string&in contentType = "application/x-www-form-urlencoded")`
- `string Net::UrlEncode(const string&in str)`
- `string Net::UrlDecode(const string&in str)`

## Json Namespace

Classes:
- `class Json::Value` - JSON value node

Functions:
- `Json::Value@ Json::Object()` - Create JSON object
- `Json::Value@ Json::Array()` - Create JSON array
- `Json::Value@ Json::Parse(const string&in json)` - Parse JSON string
- `string Json::Write(const Json::Value@ value, bool pretty = false)` - Serialize to string
- `Json::Value@ Json::FromFile(const string&in filename)` - Load from file
- `void Json::ToFile(const string&in filename, const Json::Value@ value, bool pretty = false)` - Save to file

## nvg (NanoVG) Namespace

Key functions:
- `nvg::Texture@ nvg::LoadTexture(const string&in filename, int flags = 0)`
- `int nvg::LoadFont(const string&in filename, bool fallbackIcons = false, bool fallbackArial = false)`
- `void nvg::Save()` / `void nvg::Restore()` / `void nvg::Reset()`
- `void nvg::BeginPath()` / `void nvg::EndPath()` (implied)
- `void nvg::Fill()` / `void nvg::Stroke()`
- `void nvg::FillColor(const vec4&in color)` / `void nvg::StrokeColor(const vec4&in color)`
- `void nvg::FillPaint(const nvg::Paint&in paint)` / `void nvg::StrokePaint(const nvg::Paint&in paint)`
- `void nvg::StrokeWidth(float size)`
- `void nvg::Rect(float x, float y, float w, float h)`
- `void nvg::RoundedRect(float x, float y, float w, float h, float r)`
- `void nvg::Circle(const vec2&in center, float r)`
- `void nvg::Ellipse(const vec2&in center, float rx, float ry)`
- `void nvg::Arc(const vec2&in center, float r, float a0, float a1, nvg::Winding dir)`
- `void nvg::MoveTo(const vec2&in pos)` / `void nvg::LineTo(const vec2&in pos)`
- `void nvg::BezierTo(const vec2&in c1, const vec2&in c2, const vec2&in pos)`
- `float nvg::Text(float x, float y, const string&in str)`
- `void nvg::TextBox(float x, float y, float w, const string&in str)`
- `vec2 nvg::TextBounds(const string&in str)`
- `void nvg::FontSize(float size)`
- `void nvg::FontFace(int font)`
- `void nvg::TextAlign(int align)`
- `void nvg::Scissor(float x, float y, float w, float h)`
- `void nvg::ResetScissor()`
- `nvg::Paint nvg::LinearGradient(const vec2&in start, const vec2&in end, const vec4&in color1, const vec4&in color2)`
- `nvg::Paint nvg::BoxGradient(float x, float y, float w, float h, float r, float f, const vec4&in color1, const vec4&in color2)`
- `nvg::Paint nvg::RadialGradient(const vec2&in center, float inr, float outr, const vec4&in color1, const vec4&in color2)`
- `nvg::Paint nvg::TexturePattern(const vec2&in origin, const vec2&in size, float angle, nvg::Texture@ texture, float alpha)`
- `void nvg::Translate(float x, float y)`
- `void nvg::Rotate(float angle)`
- `void nvg::Scale(float x, float y)`
- `void nvg::ResetTransform()`
- `void nvg::SetTransform(const mat3&in t)`
- `mat3 nvg::CurrentTransform()`

## Math Namespace

Constants:
- `float Math::PI`
- `float Math::PI2`
- `double Math::PIl`
- `double Math::PI2l`

Key functions:
- `int Math::Abs(int i)` / `float Math::Abs(float f)`
- `float Math::Sin(float f)` / `float Math::Cos(float f)` / `float Math::Tan(float f)`
- `float Math::Asin(float f)` / `float Math::Acos(float f)` / `float Math::Atan(float f)`
- `float Math::Atan2(float y, float x)`
- `float Math::Sqrt(float f)`
- `float Math::Pow(float x, float y)`
- `float Math::Exp(float f)`
- `float Math::Log(float f)` / `float Math::Log2(float f)` / `float Math::Log10(float f)`
- `float Math::Floor(float f)` / `float Math::Ceil(float f)` / `float Math::Round(float f)`
- `float Math::ToDeg(float rad)` / `float Math::ToRad(float deg)`
- `float Math::Rand(float min, float max)` / `int Math::Rand(int min, int max)`
- `int Math::Min(int x, int y)` / `float Math::Min(float x, float y)`
- `int Math::Max(int x, int y)` / `float Math::Max(float x, float y)`
- `int Math::Clamp(int x, int min, int max)` / `float Math::Clamp(float x, float min, float max)`
- `float Math::Lerp(const float&in min, const float&in max, float x)`
- `vec2 Math::Lerp(const vec2&in min, const vec2&in max, float x)`
- `vec3 Math::Lerp(const vec3&in min, const vec3&in max, float x)`
- `vec4 Math::Lerp(const vec4&in min, const vec4&in max, float x)`
- `float Math::Distance(const vec2&in a, const vec2&in b)` / `float Math::Distance(const vec3&in a, const vec3&in b)`
- `float Math::Distance2(const vec2&in a, const vec2&in b)` / `float Math::Distance2(const vec3&in a, const vec3&in b)`
- `float Math::Dot(const vec2&in a, const vec2&in b)` / `float Math::Dot(const vec3&in a, const vec3&in b)`
- `float Math::Angle(const vec2&in a, const vec2&in b)` / `float Math::Angle(const vec3&in a, const vec3&in b)`
- `vec3 Math::Cross(const vec3&in a, const vec3&in b)`
- `bool Math::IsNaN(float)` / `bool Math::IsInf(float)`
- `quat Math::Slerp(const quat&in a, const quat&in b, float x)`
- `float Math::InvLerp(const float&in min, const float&in max, const float&in value)`

## string (static) Namespace

Functions:
- `string string::Join(const string[]&in arr, const string&in delimiter)`
- `string string::Repeat(const string&in str, int count)`

## Regex Namespace

Functions:
- `bool Regex::IsMatch(const string&in source, const string&in pattern, int flags = Regex::Flags::ECMAScript)`
- `bool Regex::Contains(const string&in source, const string&in pattern, int flags = Regex::Flags::ECMAScript)`
- `string[]@ Regex::Match(const string&in source, const string&in pattern, int flags = Regex::Flags::ECMAScript)`
- `string[]@ Regex::Search(const string&in source, const string&in pattern, int flags = Regex::Flags::ECMAScript)`
- `Regex::SearchAllResult@ Regex::SearchAll(const string&in source, const string&in pattern, int flags = Regex::Flags::ECMAScript)`
- `string Regex::Replace(const string&in source, const string&in pattern, const string&in replace, int flags = Regex::Flags::ECMAScript)`

## Path Namespace

Functions:
- `string Path::GetExtension(const string&in path)`
- `bool Path::HasExtension(const string&in path)`
- `string Path::ChangeExtension(const string&in path, const string&in extension)`
- `string Path::RemoveExtension(const string&in path)`
- `string Path::Join(const string&in a, const string&in b)`
- `bool Path::Equals(const string&in a, const string&in b, bool caseSensitive = false)`
- `string Path::GetDirectoryName(const string&in path)`
- `string Path::GetFileName(const string&in path)`
- `string Path::GetFileNameWithoutExtension(const string&in path)`
- `string Path::SanitizeFileName(const string&in name)`

## Fids Namespace

Functions:
- `CSystemFidFile@ Fids::GetResource(const string&in path)`
- `CSystemFidsFolder@ Fids::GetResourceFolder(const string&in path)`
- `CSystemFidFile@ Fids::GetProgramData(const string&in path)`
- `CSystemFidsFolder@ Fids::GetProgramDataFolder(const string&in path)`
- `CSystemFidFile@ Fids::GetUser(const string&in path)`
- `CSystemFidsFolder@ Fids::GetUserFolder(const string&in path)`
- `CSystemFidFile@ Fids::GetGame(const string&in path)`
- `CSystemFidsFolder@ Fids::GetGameFolder(const string&in path)`
- `CSystemFidFile@ Fids::GetFake(const string&in path)`
- `CSystemFidsFolder@ Fids::GetFakeFolder(const string&in path)`
- `CMwNod@ Fids::Preload(CSystemFidFile@ fid)`
- `bool Fids::Extract(CSystemFidFile@ fid, bool hookMethod = false)`
- `string Fids::GetFullPath(CSystemFidFile@ fid)`
- `void Fids::UpdateTree(CSystemFidsFolder@ fids, bool withFiles = true)`
- `CSystemFidFile@ Fids::GetFidsFile(CSystemFidsFolder@ fids, const string&in path)`
- `CSystemFidsFolder@ Fids::GetFidsFolder(CSystemFidsFolder@ fids, const string&in path)`

## Display Namespace

Functions:
- `int Display::GetWidth()` - Game resolution width
- `int Display::GetHeight()` - Game resolution height

## Discord Namespace

Functions:
- `void Discord::Initialize(const string&in applicationId)`
- `void Discord::Shutdown()`
- `bool Discord::IsReady()`
- `Discord::User@ Discord::GetUser()`
- `void Discord::SetStatus(const Discord::Status&in status)`
- `void Discord::Respond(const string&in userId, Discord::Response reply)`
- `string Discord::GetQueuedJoin()`
- `string Discord::GetQueuedSpectate()`
- `int Discord::GetNumJoinRequests()`
- `Discord::User@ Discord::GetQueuedJoinRequest()`

## Dev Namespace

Functions:
- `void Dev::Sleep(uint ms)`
- `uint64 Dev::BaseAddress()`
- `uint64 Dev::BaseAddressEnd()`
- `uint64 Dev::FindPattern(const string&in pattern)`
- `string Dev::Patch(uint64 ptr, const string&in pattern)`
- `Dev::HookInfo@ Dev::Hook(uint64 ptr, int padding, const string&in func, int pushRegisters = 0)`
- `void Dev::Unhook(Dev::HookInfo@ hook)`
- `void Dev::DebugBreak()`
- `uint64 Dev::Allocate(uint size, bool executable = false)`
- `void Dev::Free(uint64 ptr)`
- Various Read/Write functions for memory access

## Auth Namespace

Classes:
- `class Auth::PluginAuthTask`

Functions:
- `Auth::PluginAuthTask@ Auth::GetToken()`

## Crypto Namespace

Functions:
- `string Crypto::MD5(const string&in str)`
- `string Crypto::Sha1(const string&in str)`
- `string Crypto::Sha256(const string&in str)`
- `MemoryBuffer@ Crypto::Random(int length)`
- `string Crypto::RandomBase64(int length, bool url = false)`

## Audio Namespace

Classes:
- `class Audio::Sample`
- `class Audio::Voice`

Functions:
- `Audio::Sample@ Audio::LoadSample(const string&in filename, bool streamed = false)`
- `Audio::Sample@ Audio::LoadSample(MemoryBuffer&in buffer, bool streamed = false)`
- `Audio::Sample@ Audio::LoadSampleFromAbsolutePath(const string&in filename, bool streamed = false)`
- `Audio::Voice@ Audio::Play(Sample@ sample, float gain = 1.0f)`
- `Audio::Voice@ Audio::Start(Sample@ sample)`

## SQLite Namespace

Classes:
- `class SQLite::Database`
- `class SQLite::Statement`

## Settings Namespace

Classes:
- `class Settings::Section`

## Tests Namespace

Classes:
- `class Tests::Context`

## XML Namespace

Classes:
- `class XML::Node`
- `class XML::Document`

## Reflection Namespace

Classes:
- `class Reflection::MwMemberInfo`
- `class Reflection::MwClassInfo`

Functions:
- `const Reflection::MwClassInfo@ Reflection::GetType(const string&in name)`
- `const Reflection::MwClassInfo@ Reflection::GetType(uint id)`
- `const Reflection::MwClassInfo@ Reflection::TypeOf(CMwNod@ nod)`
- `int Reflection::GetRefCount(CMwNod@ nod)`

## Import Namespace

Classes:
- `class Import::Library`
- `class Import::Function`
- `class Import::Ref`

Functions:
- `Import::Library@ Import::GetLibrary(const string&in path)`

## mat3 Namespace

Functions:
- `mat3 mat3::Identity()`
- `mat3 mat3::Translate(const vec2&in v)`
- `mat3 mat3::Rotate(float angle)`
- `mat3 mat3::Scale(const vec2&in scale)`
- `mat3 mat3::Scale(float scale)`
- `mat3 mat3::Inverse(const mat3&in)`
- `mat3 mat3::Transpose(const mat3&in)`

## mat4 Namespace

Functions:
- `mat4 mat4::Identity()`
- `mat4 mat4::Translate(const vec3&in v)`
- `mat4 mat4::Rotate(float angle, const vec3&in dir)`
- `mat4 mat4::Scale(const vec3&in scale)`
- `mat4 mat4::Scale(float scale)`
- `mat4 mat4::Perspective(float yFov, float aspect, float nearZ, float farZ)`
- `mat4 mat4::Inverse(const mat4&in)`
- `mat4 mat4::LookAt(const vec3&in eye, const vec3&in center, const vec3&in up)`
- `mat4 mat4::Transpose(const mat4&in)`

### Reference: OpenPlanet-Basic-API

