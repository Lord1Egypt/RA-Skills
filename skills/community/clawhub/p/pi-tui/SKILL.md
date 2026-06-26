---
name: pi-tui
description: Pi TUI — Terminal UI framework with differential rendering + synchronized output for flicker-free interactive CLIs. 
---

# Pi TUI

Component-based architecture (TUI/Container/Box/Text/TruncatedText/Input/Editor/Markdown/Loader/CancellableLoader/SelectList/SettingsList/Spacer/Image), overlay system, IME support, autocomplete, Kitty keyboard protocol. Differential rendering TUI framework.
Install: `npm install @earendil-works/pi-tui`

## Use Cases

Use when building terminal UIs, interactive CLI apps, TUI editors, terminal select lists/settings panels, terminal Markdown rendering, or inline terminal images.

## Core Concepts

**Component Interface** — All components implement `render(width): string[]` (each line ≤ width), `handleInput?(data)`, `invalidate?()`. Each line auto-appends SGR+OSC reset; styles do not carry across lines.

**Focusable Interface** — Components needing IME implement a `focused: boolean` property and insert `CURSOR_MARKER` before the cursor in render. Containers with Input/Editor children must propagate focus state (otherwise IME candidate window mispositions). Hardware cursor hidden by default; enable with `PI_HARDWARE_CURSOR=1`.

**Differential Rendering** — Three strategies: first render outputs all lines, width change clears and redraws, incremental only updates changed lines. CSI 2026 synchronized output prevents flicker.

## Quick Start

```typescript
import { TUI, Text, Editor, ProcessTerminal, matchesKey } from "@earendil-works/pi-tui";

const tui = new TUI(new ProcessTerminal());
tui.addChild(new Text("Welcome!"));
const editor = new Editor(tui, theme);
editor.onSubmit = (text) => tui.addChild(new Text(`> ${text}`));
tui.addChild(editor);
tui.setFocus(editor);
tui.addInputListener((data) => { if (matchesKey(data, 'ctrl+c')) { tui.stop(); process.exit(0); } });
tui.start();

// TUI API: addChild/removeChild/start/stop/requestRender/setFocus/onDebug
```

## Progressive References

Load on demand, only when needed:

- Overlays/dialogs/menus → `references/overlays.md`
- Component API reference → `references/components.md`
- Autocomplete/key detection → `references/autocomplete.md`

## Gotchas

1. **render(width) line width**: each line ≤ width, otherwise TUI throws
2. **Styles don't span lines**: auto-reset at line end, reapply styles per line for multi-line styled text
3. **Container IME propagation**: containers with Input/Editor must implement Focusable and propagate focus
4. **Ctrl+C**: raw mode doesn't send SIGINT, must handle via `matchesKey(data, 'ctrl+c')`
5. **Overlay focus**: `unfocus({ target: component })` releases to specific component, `unfocus({ target: null })` clears focus