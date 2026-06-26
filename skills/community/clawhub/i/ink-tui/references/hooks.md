# Ink Hook API Reference

## `useInput(handler, options?)`

The primary hook for keyboard input. Ink enters raw mode automatically.

```tsx
import { useInput } from 'ink';

function MyComponent() {
  useInput((input, key) => {
    if (key.escape) exit();
    if (key.return) submit();
    if (key.upArrow) moveUp();
    if (input === 'q') exit();
  });

  return <Text>Press a key...</Text>;
}
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `isActive` | boolean | true | Enable/disable handling |
| `handleTab` | boolean | false | Include Tab key events |
| `handleBackspace` | boolean | false | Include Backspace events |
| `handleArrows` | boolean | true | Include arrow key events |

### Key Object

```typescript
type Key = {
  // Arrows
  upArrow: boolean;
  downArrow: boolean;
  leftArrow: boolean;
  rightArrow: boolean;

  // Enter/Return
  return: boolean;
  enter: boolean;    // alias for return

  // Modifiers
  ctrl: boolean;
  shift: boolean;
  alt: boolean;      // Option on Mac
  meta: boolean;

  // Special keys
  escape: boolean;
  tab: boolean;
  backspace: boolean;
  delete: boolean;
  space: boolean;
  capsLock: boolean;
  numLock: boolean;
  fn: boolean;

  // Navigation
  pageUp: boolean;
  pageDown: boolean;
  home: boolean;
  end: boolean;
  insert: boolean;

  // Function keys (f1–f12)
  f1: boolean;
  // ... f2–f12
}
```

### Common Patterns

```tsx
// Arrow navigation
useInput((input, key) => {
  if (key.upArrow) setIndex(i => max(0, i - 1));
  if (key.downArrow) setIndex(i => min(len - 1, i + 1));
});

// Text input buffering
const [value, setValue] = useState('');
useInput((input, key) => {
  if (key.return) onSubmit(value);
  else if (key.backspace) setValue(v => v.slice(0, -1));
  else if (input.length === 1 && !key.ctrl && !key.meta) setValue(v => v + input);
});

// Confirm dialog
useInput((_, key) => {
  if (key.escape) onCancel();
  if (key.return) onConfirm();
  if (input === 'y' || input === 'Y') onConfirm();
  if (input === 'n' || input === 'N') onCancel();
});
```

---

## `useApp()`

Access app-level utilities.

```tsx
import { useApp } from 'ink';

const { exit } = useApp();

// Standard exit
exit();

// Exit with error
exit(new Error('Something went wrong'));
```

---

## `useFocus(options?)`

Focus management for interactive components (form fields, menus).

```tsx
import { useFocus } from 'ink';

function FocusableInput() {
  const { isFocused } = useFocus({ autoFocus: true });

  return (
    <Text color={isFocused ? 'blue' : undefined}>
      {isFocused ? '❯ ' : '  '}Input field
    </Text>
  );
}
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `autoFocus` | boolean | false | Auto-focus on mount |
| `isActive` | boolean | true | Whether component is active for focus |
| `id` | string | — | Focus group identifier |

---

## `useFocusManager()`

Provides focus navigation between focusable components.

```tsx
import { useFocus, useFocusManager } from 'ink';

function App() {
  const { focusNext, focusPrevious, focus } = useFocusManager();
  // focusNext() — move to next focusable
  // focusPrevious() — move to previous
  // focus(id) — jump to specific component

  return (
    <Box flexDirection="column">
      <Option label="Option 1" id="opt-1" />
      <Option label="Option 2" id="opt-2" />
      <Option label="Option 3" id="opt-3" />
    </Box>
  );
}
```

---

## `useStdin()`

```tsx
import { useStdin } from 'ink';

const { stdin, isRawModeSupported, setRawMode } = useStdin();

// isRawModeSupported — whether terminal supports raw mode
// setRawMode(true/false) — toggle raw mode
```

---

## `useStdout()`

```tsx
import { useStdout } from 'ink';

const { stdout } = useStdout();

// stdout is a Node.js WritableStream
stdout.write('manual output');
```

---

## `useStderr()`

```tsx
import { useStderr } from 'ink';

const { stderr, write } = useStderr();
write('Error message to stderr');
```

---

## Custom Hook Patterns

### Persistent State with Side Effects

```tsx
import { useState, useEffect } from 'react';
import { useInput } from 'ink';

function useListNavigator(items: string[]) {
  const [selected, setSelected] = useState(0);

  useInput((_, key) => {
    if (key.upArrow)   setSelected(i => Math.max(0, i - 1));
    if (key.downArrow) setSelected(i => Math.min(items.length - 1, i + 1));
  });

  return selected;
}
```

### Keyboard Shortcut Registry

```tsx
import { useInput } from 'ink';

type Shortcut = { keys: string; handler: () => void };

function useShortcuts(shortcuts: Shortcut[]) {
  useInput((input, key) => {
    for (const s of shortcuts) {
      const matches = s.keys.split(',').some(k => {
        const trimmed = k.trim();
        if (trimmed.length === 1 && !key.ctrl && !key.meta)
          return input === trimmed;
        if (key[trimmed as keyof typeof key])
          return true;
        return false;
      });
      if (matches) {
        s.handler();
        break;
      }
    }
  });
}

// Usage:
useShortcuts([
  { keys: 'q, escape', handler: () => exit() },
  { keys: 'return', handler: () => submit() },
]);
```