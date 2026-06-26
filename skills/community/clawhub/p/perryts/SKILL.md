---
name: perryts
description: PerryTS native TypeScript compiler guide. Covers installation, compilation, perry/ui, perry/tui, multi-threading, standard library, cross-platform compilation, project configuration, CLI commands. 
---

# PerryTS — Native TypeScript Compiler

Compiles `.ts` to native binaries via SWC parsing → LLVM code generation. No V8/Node.js.

## Use Cases 

Use when writing/debugging PerryTS projects, asking about API usage, or cross-platform compilation.

## Installation

```bash
npm install @perryts/perry          # Recommended, requires Node ≥ 16
brew install perryts/perry/perry    # macOS
winget install PerryTS.Perry        # Windows
perry doctor; perry --version       # Verify
perry update                        # Self-update
```

Prerequisites: macOS `xcode-select --install` / Linux `apt install build-essential` / Windows `winget install LLVM.LLVM && perry setup windows`

## CLI

```bash
perry compile main.ts -o app                   # Compile
perry main.ts -o app                           # Shorthand
perry compile app.ts --target ios-simulator    # Cross-compile
perry compile app.ts --print-hir               # Debug HIR
perry compile plugin.ts --output-type dylib    # Compile as shared library
perry run [ios|visionos|android|web]           # Compile + run
perry dev src/main.ts                          # Watch + auto-restart
perry check src/ [--check-deps] [--fix]        # Compatibility check
perry init my-project                          # Create project
perry publish [macos|ios|android|linux]        # Build for distribution
perry setup [ios|android|macos|windows]        # Credentials/toolchain
perry explain U001                             # Error code explanation
perry i18n extract src/main.ts                 # Internationalization extraction
perry native init/list/validate                # Native binding tools
```

Compile targets: `ios-simulator` `ios` `visionos-simulator` `android` `wasm` `web` `windows` `linux` `ios-widget` `watchos-widget` `wearos-tile`

Key flags: `--minify` `--type-check` `--trace hir,llvm` `--focus <name>` `--enable-js-runtime` `--enable-geisterhand`

## Language Support

Full support: variables/functions/classes/enums/interfaces/async/Promise/generators/closures/Map/Set/RegExp/JSON/BigInt/ES modules. Types erased at compile time.

**Not supported**: `eval()` `new Function()` `require()` `await import()` `Object.setPrototypeOf()` prototype mutation, full Proxy/WeakRef

## Multi-threading (`perry/thread`)

```typescript
import { parallelMap, parallelFilter, spawn } from "perry/thread"

// Data parallelism: auto-detects CPU core count, splits arrays, OS threads, ordered collection
const results = parallelMap(data, (item: T) => transform(item))
// Suitable for large arrays; small arrays (< core count) use zero-overhead in-place processing

// Parallel filter: maintains original order
const filtered = parallelFilter(items, (item) => predicate(item))

// Background thread: returns Promise immediately, main thread not blocked
const result = await spawn(() => heavyComputation())
// Concurrent tasks: await Promise.all([spawn(t1), spawn(t2), spawn(t3)])
```

**Thread safety**: Closures cannot capture mutable variables (compile-time rejection), values are deep-copied to worker threads.

## Native UI (`perry/ui`)

Declarative TS, compiled to real platform controls (AppKit/UIKit/GTK4/Win32/DOM).

```typescript
import { App, VStack, Text, Button, State, ForEach } from "perry/ui"

const count = State(0)

App({
  title: "App", width: 400, height: 300,
  body: VStack(16, [
    Text(`Count: ${count.value}`),                        // Auto-reactive binding
    Button("+", () => count.set(count.value + 1)),
  ]),
})
```

### Controls (all imported from `perry/ui`)

| Control | Signature |
|---------|-----------|
| Text | `Text(content)` — template strings auto-bind to State |
| Button | `Button(label, onClick)` |
| TextField | `TextField(placeholder, (v: string) => void)` |
| SecureField | `SecureField(placeholder, onChange)` |
| TextArea | `TextArea(placeholder, onChange)` |
| Toggle | `Toggle(label, (v: boolean) => void)` |
| Slider | `Slider(min, max, (v: number) => void)` |
| Picker | `Picker(onChange)` + `pickerAddItem(p, label)` |
| ProgressView | `ProgressView()` |
| ImageFile | `ImageFile(path)` |
| ImageSymbol | `ImageSymbol(name)` — macOS/iOS only |

Platform-specific: `Canvas(w,h)` `WebView({url,...})` `MapView(w,h)` `Chart(kind,w,h)` `RichTextEditor` `PdfView` `QRCode` `TreeView` `Calendar` `Table` `CameraView`

### State

```typescript
const s = State(0); s.value; s.set(42)  // .set() triggers UI re-render
ForEach(count, (i) => Text(items.value[i]))  // Iterate list by count
stateOnChange(s, (v) => cb)                  // Listen for changes
// Object/array state must create new references: s.set({...s.value, k: v})
// Two-way binding: stateBindTextfield(state, field) / stateBindSlider / stateBindToggle
```

### Layout

`VStack(spacing, children)` `HStack(spacing, children)` — Stack containers
`ZStack()` + `widgetAddChild` — Overlay
`ScrollView()` + `scrollviewSetChild` — Scrollable
`LazyVStack(count, render)` — Lazy rendering (macOS NSTableView only)
`NavStack()` + `navstackPush/pop` — Navigation stack
`Spacer()` `Divider()` — Flexible space/separator
`SplitView()` + `splitViewAddChild` — Split panel

Child management: `widgetAddChild`/`widgetAddChildAt`/`widgetRemoveChild`/`widgetClearChildren`

Alignment: `stackSetAlignment(stack, 5=Leading|9=CenterX|7=Width)` / HStack:`3=Top|12=CenterY|4=Bottom`
Distribution: `stackSetDistribution(stack, 0=Fill|1=FillEqually|2=FillProportionally|3=EqualSpacing)`

Stretching: `widgetMatchParentWidth` `widgetMatchParentHeight` `widgetSetHugging`
Overlays: `widgetAddOverlay(parent, child)` `widgetSetOverlayFrame(child, x, y, w, h)`

### Styling

**Inline style (recommended)**: trailing argument in control constructors
```typescript
Button("Save", cb, {
  backgroundColor: "#3B82F6", borderRadius: 8, padding: 12,
  shadow: { color: "#0004", blur: 12, offsetY: 4 },
  tooltip: "Save", enabled: true,
})
```
Color support: `"#3B82F6"` / `"#3B82F6FF"` / `"blue"` / `{ r,g,b,a: [0,1] }`

**Imperative**: `textSetFontSize(w,24)` `textSetColor(w,r,g,b,a)` `setCornerRadius(w,8)` `widgetSetBackgroundColor(w,r,g,b,a)` `widgetSetEdgeInsets(w,top,left,bottom,right)` `widgetSetOpacity(w,0.5)` `widgetSetEnabled(w,0|1)` `widgetSetTooltip(w,text)` `widgetSetControlSize(w,0-3)`

### Events

```typescript
widgetSetOnClick(w, cb)
widgetSetOnHover(w, cb)           // Desktop/Web only
widgetSetOnDoubleClick(w, cb)
addKeyboardShortcut("n", 1, cb)   // 1=Cmd,2=Shift,4=Option,8=Control(macOS only)
registerGlobalHotkey("F5", 0, cb) // macOS only
clipboardWrite(txt) / clipboardRead()
```

### Dialogs & Menus

```typescript
openFileDialog(cb) / openFolderDialog(cb) / saveFileDialog(cb, name, ext)
alert(title, msg) / alertWithButtons(title, msg, ["Cancel","OK"], (idx)=>...)

const menu = menuCreate()
menuAddItemWithShortcut(menu, "Save", "s", cb)
menuBarAddMenu(menuBar, "File", menu); menuBarAttach(menuBar)
widgetSetContextMenu(widget, menu)  // Context menu

const sheet = sheetCreate(body, w, h); sheetPresent(sheet); sheetDismiss(sheet)
```

### Multi-window

```typescript
const win = Window("Title", 500, 400)
win.setBody(VStack(16, [...])); win.show(); win.hide(); win.close()
```
App properties: `frameless` `level:"floating"|"statusBar"|"modal"` `transparent` `vibrancy` `activationPolicy:"accessory"`

### Animation

```typescript
widget.animateOpacity(target, durationSecs)
widget.animatePosition(dx, dy, durationSecs)
```

### Cross-platform

```bash
perry app.ts -o app --target web|windows|linux|android|ios-simulator|...
```
`__platform__`: 0=macOS 1=iOS 2=Android 3=Windows 4=Linux 5=Web 6=tvOS 7=watchOS 8=visionOS, compile-time constant folding.

## Terminal UI (`perry/tui`)

Ink-style, double-buffered ANSI diff, no Node/React.

```typescript
import { Box, Text, useState, useInput, run, exit } from "perry/tui"

run(() => {
  const [n, setN] = useState(0)
  useInput((s: string) => { if (s === "+") setN(n+1); if (s === "q") exit() })
  return Box([Text("count: " + n)])
})
```

### Widgets

| Widget | Usage |
|--------|-------|
| Box | `Box({ flexDirection, gap, padding, ... }, children)` — Flexbox container |
| Text | `Text(content, { color, bold, italic, underline, inverse, dimColor })` |
| Spacer | `Spacer()` |
| Input | `Input(value, cursorPos)` |
| TextArea | `TextArea(value)` |
| List | `List(items, selectedIndex?)` |
| Select | `Select(items, selectedIndex?)` |
| Spinner | `Spinner(frame)` / `AnimatedSpinner({interval, frames})` |
| ProgressBar | `ProgressBar(filled, total, width?)` |
| Table | `Table({ headers, rows, selected? })` |
| Tabs | `Tabs({ tabs, active, body })` |

### Hooks

`useState(init)` → `[val, setter]` | `useEffect(fn, deps?)` | `useMemo(fn, deps)` | `useRef(init)` → `.get()/.set()` | `useApp()` → `{exit(), waitUntilExit()}` | `useStdout()` → `{columns(), rows(), write()}` | `useFocus(autoFocus, isActive)` | `useInput(handler)` — raw byte callback

Differences from ink: `useRef` uses `.get()/.set()` not `.current`; Box uses function calls not JSX.

## Standard Library

Importing the following packages automatically routes to Rust native implementations, no configuration needed:

**HTTP**: `fastify` `axios` `fetch` `ws` `node:http`/`node:https`/`node:http2` (includes WebSocket upgrade)
**Databases**: `mysql2` `pg` `better-sqlite3` `mongodb` `ioredis`/`redis`
**Crypto**: `bcrypt` `argon2` `jsonwebtoken` `crypto` `ethers`
**Utilities**: `lodash` `dayjs` `uuid` `nanoid` `slugify` `validator` `commander` `sharp` `cheerio` `nodemailer` `zlib` `cron` `lru-cache` `decimal.js`
**Files**: `fs` `path` `child_process`
**External**: `@perryts/tursodb` `@perryts/iroh` `@perryts/postgres` `@perryts/mysql` `@perryts/mongodb` `@perryts/redis`

**compilePackages** (pure TS packages compiled natively): set `{"perry":{"compilePackages":["pkg"]}}` in `package.json`

**Binary size**: No stdlib ~300KB / fs+path ~3MB / UI ~3MB / full stdlib ~48MB

## Project Configuration

```toml
# perry.toml (minimal)
[project]
name = "my-app"
entry = "src/main.ts"
[build]
out_dir = "dist"
```

Platform config: `[macos]` (bundle_id/category/minimum_os/distribute:"appstore"|"notarize"|"both") `[ios]` (deployment_target/device_family/distribute) `[android]` (package_name/min_sdk/target_sdk/permissions) `[linux]` (format:"appimage"|"deb"|"rpm")

Config precedence: CLI flags → environment variables → perry.toml → ~/.perry/config.toml

## Type System

Types erased at compile time. Type inference handles common patterns, `--type-check` integrates tsgo strict checking. Supports `Partial<T>` `Pick<T,K>` `Record<K,V>` `Omit<T,K>` `ReturnType<T>` `Readonly<T>`. Union/intersection type syntax recognized but does not affect code generation; runtime narrowing uses `typeof`.

## Limitations

- No eval()/new Function()/dynamic require()/await import()
- No Object.setPrototypeOf()/dynamic prototype mutation
- Decorators: compile-time transforms only + limited legacy compatibility (Reflect.defineMetadata/getMetadata), no Angular/NestJS/TypeORM full runtime support
- Proxy/WeakRef not fully implemented
- JSX parsed but `_jsx` runtime symbol not linked; use function call form

## Decorator Migration

Angular/NestJS/TypeORM → Remove decorators, use explicit construction:
```typescript
// services.ts — single-file dependency wiring
export const api = new ApiService()
export const rating = new RatingService(api)
export const chat = new ChatService(api, rating)
```

## Native Binding Architecture

Four layers: User TS → Bindings (well-known table + node_modules) → perry-ffi (stable ABI) → perry-runtime

Writing bindings: `perry native init` → edit `src/lib.rs` (use perry_ffi types only) → `perry native validate` → npm publish

## npm Package Porting

`compilePackages` compiles pure TS/JS packages. Common fixes: reverse-lookahead regex → forward capture; Symbol → string sentinel; Proxy → not portable; WeakMap → replace with Map; computed property keys `{[k]:v}` → create empty object then assign.

## Plugin System

```typescript
// Plugin (--output-type dylib)
export function activate(api: PluginApi) {
  api.setMetadata(name, ver, desc)
  api.registerHook("onRequest", (data) => data)
  api.registerTool("toolName", "desc", (args) => result)
}
export function deactivate() { /* cleanup */ }

// Host
import { loadPlugin, emitHook, invokeTool } from "perry/plugin"
loadPlugin("./plugin.dylib")
emitHook("hookName", data)
invokeTool("toolName", args)
```

## Geisterhand (UI Testing)

`perry app.ts --enable-geisterhand && ./app` → HTTP server on `127.0.0.1:7676`

```bash
GET  /health /widgets[?label=&type=] /screenshot → PNG /chaos/status
POST /click/:handle /type/:handle {"text":"..."} /slide/:handle {"value":0.75}
POST /toggle/:handle /key {"shortcut":"s"} /scroll/:handle {"x":0,"y":100}
POST /chaos/start {"interval_ms":200} /chaos/stop
```
Control types: 0=Button 1=TextField 2=Slider 3=Toggle 4=Picker 5=Menu 6=Shortcut

## i18n

```toml
# perry.toml
[i18n]
locales = ["en", "de"]
default_locale = "en"
```
```bash
perry i18n extract src/main.ts  # Generates locales/{en,de}.json
```
Compile-time validation + baked into binary, zero runtime overhead. `t("Next")` / `t("Hello, {name}!", {name:"Alice"})`

## References

- Website: https://perryts.com | Docs: https://docs.perryts.com/
- GitHub: https://github.com/PerryTS/perry | npm: https://www.npmjs.com/package/@perryts/perry