# Autocomplete & Key Detection

## CombinedAutocompleteProvider

For Editor, supports both slash commands and file paths:

```typescript
import { CombinedAutocompleteProvider } from "@earendil-works/pi-tui";
const provider = new CombinedAutocompleteProvider(
  [{ name: "help", description: "Show help" }],
  process.cwd()
);
editor.setAutocompleteProvider(provider);
```

- Type `/` → slash command list
- Tab → file path completion (supports `~/`, `./`, `../`, `@`)

## Key Detection

```typescript
import { matchesKey, Key } from "@earendil-works/pi-tui";
matchesKey(data, Key.ctrl("c"))   // or string "ctrl+c"
matchesKey(data, Key.enter)       // "enter"
matchesKey(data, Key.shift("tab")) // "shift+tab"
```

Supports Kitty keyboard protocol. Key identifiers: `enter/escape/tab/space/backspace/delete/home/end`, `up/down/left/right`, `ctrl(k)/shift(k)/alt(k)/ctrlShift(k)`.

## Component Shortcuts

**Input**: Enter submit, Ctrl+A/E line start/end, Ctrl+W/Alt+Backspace delete word, Ctrl+U/K delete to line start/end, Ctrl+Left/Right word navigation

**Editor**: Enter submit, Shift/Ctrl/Alt+Enter newline, Tab complete, Ctrl+K/U delete to line end/start, Ctrl+W/Alt+Backspace delete word backward, Alt+D/Delete delete word forward, Ctrl+A/E line start/end, Ctrl+] jump char

**SelectList**: Arrow keys navigate, Enter select, Escape cancel

**SettingsList**: Arrow keys navigate, Enter/Space activate, Escape cancel