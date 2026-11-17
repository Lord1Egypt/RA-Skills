# Native UI

## Overview

```typescript
import { App, VStack, HStack, Text, Button, TextField, state } from 'perry/ui'
```

Handle-based widget system. 64-bit handles, free-function API. `App()` starts the native run loop.

```typescript
App({
  body: VStack([
    Text("Hello, Perry!"),
    Button("Click me", () => console.log("clicked"))
  ])
})
```

## Layout

### VStack / HStack / ZStack
```typescript
VStack([child1, child2])                    // vertical
HStack([child1, child2])                    // horizontal
ZStack([background, foreground])            // layered
```

### Stack Alignment & Distribution
```typescript
// Alignment: .leading, .center, .trailing (HStack) / .top, .center, .bottom (VStack)
VStack([ ... ], { alignment: "leading" })
// Distribution: .fill, .start, .center, .end, .spaceBetween, .spaceAround, .spaceEvenly
HStack([ ... ], { distribution: "spaceBetween" })
```

### ScrollView
```typescript
ScrollView(VStack([ /* many children */ ]))
// Or set child after construction:
scrollviewSetChild(scrollView, content)
```

### Child Management
```typescript
widgetAddChild(parent, child)
widgetAddChildAt(parent, child, index)
widgetClearChildren(parent)
```

## Widgets

| Widget | Usage |
|--------|-------|
| `Text(content)` | Display text |
| `Button(label, onClick)` | Interactive button |
| `TextField(placeholder, onChange)` | Single-line input |
| `SecureField(placeholder, onChange)` | Password input |
| `Toggle(label, isOn, onChange)` | Switch/toggle |
| `Slider(value, min, max, onChange)` | Range slider |
| `Picker(options, selected, onChange)` | Dropdown selector |
| `ImageFile(path)` | Image from file |
| `ImageSymbol(name)` | System icon |
| `ProgressView()` | Loading spinner |
| `TextArea(text, onChange)` | Multi-line text |
| `Spacer()` | Flexible space |
| `Divider()` | Horizontal/vertical line |
| `Canvas(width, height)` | Custom drawing surface |

## Styling

### Inline Style Object
```typescript
Text("Styled", {
  fontSize: 16,
  fontWeight: "bold",
  color: "#ff0000",
  backgroundColor: { r: 0, g: 0, b: 0, a: 1 },
  padding: 8,                          // uniform
  padding: { top: 4, right: 8, bottom: 4, left: 8 }, // per-side
  borderRadius: 8,
  opacity: 0.9,
  hidden: false
})
```

### Imperative API
```typescript
widgetSetBackgroundColor(handle, r, g, b, a)
widgetSetCornerRadius(handle, radius)
widgetSetHidden(handle, hidden)
widgetSetWidth(handle, width)
widgetSetHeight(handle, height)
widgetMatchParentWidth(handle)
widgetMatchParentHeight(handle)
setPadding(handle, top, right, bottom, left)
```

## State & Reactivity

### State Container
```typescript
const count = state(0)
App({
  body: VStack([
    Text(`Count: ${count.get()}`),     // reactive via template literal
    Button("+", () => count.set(count.get() + 1))
  ])
})
```

### Binding Inputs
```typescript
stateBindTextfield(textField, myState)  // two-way binding
stateBindSlider(slider, myState)
stateBindToggle(toggle, myState)
```

### ForEach (Dynamic Lists)
```typescript
const items = state(["A", "B", "C"])
VStack([
  ...items.get().map((item, i) =>
    Text(`Item ${i}: ${item}`)
  )
])
```

## Events

```typescript
// Click
Button("OK", () => { /* onClick */ })

// Hover (macOS/GTK4/Web only)
onHover(widget, (inside) => { /* ... */ })

// Double-click
onDoubleClick(widget, () => { /* ... */ })

// Keyboard shortcuts
menuAddItemWithShortcut(menu, "Save", () => save(), 1, "s")  // Cmd+S
// Modifier bits: 1=Cmd/Ctrl, 2=Shift, 4=Option/Alt, 8=Control
```

## Canvas Drawing

```typescript
const canvas = Canvas(400, 300)
canvas.drawRect(10, 10, 100, 80, 0, 0, 0, 1)   // x, y, w, h, r, g, b, a
canvas.drawLine(0, 0, 400, 300, 255, 0, 0, 1)
canvas.drawCircle(200, 150, 50, 0, 0, 255, 1)
canvas.drawText("Hello", 20, 30, 16, 0, 0, 0)
```

## Menus & Dialogs

### Menu Bar (macOS)
```typescript
const bar = menuBarCreate()
const fileMenu = menuCreate("File")
menuBarAddMenu(bar, fileMenu)
menuAddItemWithShortcut(fileMenu, "Open", () => open(), 1, "o")
menuBarAttach(bar)
```

### Context Menu
```typescript
widgetSetContextMenu(widget, menu)
```

### File Dialogs
```typescript
const files = openFileDialog(["ts", "js"], false)  // extensions, multiSelect
const folder = openFolderDialog()
const path = saveFileDialog("default.txt")
```

### Sheets & Alerts
```typescript
alert("Title", "Message")
alertWithButtons("Title", "Message", ["OK", "Cancel"], (button) => { /* ... */ })
const sheet = sheetCreate(VStack([Text("Sheet content")]))
sheetPresent(sheet)
sheetDismiss(sheet)
```

## Multi-Window

```typescript
const win = Window("Settings", 400, 300)
win.setBody(VStack([/* ... */]))
win.show()
win.onFocusLost(() => console.log("focus lost"))
win.close()
```

### App Config
```typescript
App({
  frameless: true,
  level: "floating",    // normal, floating, statusBar
  transparent: true,
  vibrancy: "sidebar",  // macOS only
  activationPolicy: "accessory",  // macOS: regular, accessory, prohibited
  body: /* ... */
})
```

## Table

```typescript
const table = Table(3, 2, (row, col) => {
  if (col === 0) return Text(`Row ${row}`)
  return Text(`Data ${row}`)
})
tableGetSelectedRow(table)  // returns selected row index
```

## Animation

```typescript
animateOpacity(widget, 0, 1, 300)    // fade in over 300ms
animatePosition(widget, 0, 100, 0, 0, 300)  // slide down
```

## Theming (perry-styling)

```typescript
import { getTheme, PerryColor, applyBg, applyRadius } from 'perry-styling'
const theme = getTheme()
// Token-based theming with codegen: `perry-styling generate`
```

## Platform Support Matrix

Styling (43 properties): macOS 43/43, iOS 42/43, Android 41/43, GTK4 39/43, Windows 38/43, Web 37/43. See `docs/src/ui/styling.md` for per-property breakdown.

## Geisterhand (UI Testing)

In-process HTTP testing API on port 7676:
```
GET  /health           → health check
GET  /widgets          → widget tree JSON
GET  /screenshot       → PNG screenshot
POST /tap {x, y}       → simulate tap
POST /type {text}      → simulate typing
POST /chaos {count}    → fuzz testing
```
