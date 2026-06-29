# Pi TUI Component System

Extensions can render custom TUI components via `ctx.ui.custom()`.

## Component Interface

```ts
interface Component {
  render(width: number): string[];       // each line must not exceed width
  handleInput?(data: string): void;      // keyboard input
  wantsKeyRelease?: boolean;             // receive key release events
  invalidate(): void;                    // clear cache
}
```

## Focusable (IME Support)

```ts
interface Focusable {
  focused: boolean;  // auto-set by TUI
}

// use CURSOR_MARKER in render to mark cursor position
render(width) {
  return [`> ${CURSOR_MARKER}${charAtCursor}`];
}
```

Container components must propagate focus state to child Input/Editor components.

## Built-in Components

```ts
import { Text, Box, Container, Spacer, Markdown } from "@earendil-works/pi-tui";
```

- **Text**(content, padX, padY, bgFn?) — multi-line text (auto-wrapping)
- **Box**(padX, padY, bgFn) — container with padding + background
- **Container**() — vertical layout of child components
- **Spacer**(lines) — blank lines
- **Markdown**(text, padX, padY, theme) — syntax-highlighted Markdown
- **Image**(base64, mimeType, theme, opts?) — terminal image (requires kitty/iterm2 protocol)

## Overlay Components

```ts
ctx.ui.custom(component, {
  overlay: true,
  overlayOptions: {
    width: "50%", minWidth: 40, maxHeight: "80%",
    anchor: "right-center", offsetX: -2, offsetY: 0,
    margin: 2,
    visible: (tw, th) => tw >= 80,
  }
});
```

Anchor positions: center, top-left, top-center, top-right, left-center, right-center, bottom-left, bottom-center, bottom-right

## Key Detection

```ts
import { matchesKey, Key } from "@earendil-works/pi-tui";

handleInput(data: string) {
  if (matchesKey(data, Key.up)) ...
  if (matchesKey(data, Key.ctrl("c"))) ...
}
```

## Utilities

- `visibleWidth(str)` — display width excluding ANSI codes
- `truncateToWidth(str, width)` — truncate (with ...)
- `wrapTextWithAnsi(str, width)` — wrap preserving ANSI codes

## Render Cache Pattern

```ts
render(width: number): string[] {
  if (this.cachedLines && this.cachedWidth === width) return this.cachedLines;
  this.cachedLines = [...]; this.cachedWidth = width;
  return this.cachedLines;
}
invalidate() { this.cachedWidth = undefined; }  // called on theme change
```

## Common UI Patterns

- **SelectList** — selection list (↑↓ navigate, enter select, esc cancel)
- **BorderedLoader** — async operation + cancel (spinner + escape abort)
- **SettingsList** — toggle settings (cycle through options)

## Debugging

```bash
PI_TUI_WRITE_LOG=/tmp/tui-ansi.log pi    # capture raw ANSI stream
/debug                                    # writes to ~/.pi/agent/pi-debug.log
```