---
name: ink-tui
description: Ink — React for interactive command-line apps. Build rich terminal UIs with React components. 
---

# Ink Skill Guide

## Overview

Ink renders React components directly to the terminal using Yoga layout (Flexbox for CLI). It handles diffing, re-rendering, and terminal I/O. Components receive real React state, effects, and hooks — the same mental model as web React.Requires Node.js 22+ and React 19.2+ as peer dependencies.

## Triggers

when the user wants to create CLI/TUI apps, terminal dashboards, interactive prompts, colored terminal output, spinners, progress bars, or tables using JSX/React syntax. 
 
- building CLI apps with React
- creating interactive terminal UIs
- rendering styled terminal output
- handling keyboard input in the terminal
- terminal layout with Flexbox/Yoga

## Quick Start

```bash
mkdir my-cli && cd my-cli
pnpm init
pnpm add ink react @types/react
pnpm add -D tsx typescript @types/node
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "outDir": "build"
  }
}
```

```tsx
// index.tsx
import { render, Box, Text } from 'ink';

const App = () => (
  <Box flexDirection="column">
    <Text color="green" bold>Hello, CLI!</Text>
  </Box>
);

render(<App />);
```

Run: `node --import=tsx index.tsx`

## Architecture

Ink uses `react-reconciler` as its rendering core and `yoga-layout` as its layout engine. It mounts components into a virtual terminal, diffs against current output, and writes changes to stdout. This means:
- Full React state/lifecycle (useState, useEffect, etc.)
- Flexbox layout via Yoga (not CSS — uses integer-based positioning)
- Terminal output is treated as an append-only buffer that gets replaced on re-render

## Components

### `<Box>` — Layout Container

```tsx
import { Box, Text } from 'ink';

// Row layout (default flexDirection)
<Box gap={2}>
  <Text>Left</Text>
  <Text>Right</Text>
</Box>

// Column layout with border
<Box flexDirection="column" borderStyle="round" padding={1} width={40}>
  <Text bold>Title</Text>
  <Text dim>subtitle</Text>
</Box>
```

Key Box props: `width`, `height`, `padding`/`paddingX`/`paddingY`, `borderStyle` (single/double/round/classic/bold), `borderDimColor`, `gap`, `flexGrow`, `flexShrink`, `flexDirection` (row/column), `justifyContent`, `alignItems`.

### `<Text>` — Styled Text

```tsx
// Direct styling
<Text color="green" bold underline>Success</Text>

// Nested spans
<Text>
  Regular <Text bold>bold</Text> and <Text color="red" inverse>inverse red</Text>
</Text>

// Wrap via width
<Text width={40} wrap="truncate">Truncated long text...</Text>
```

Colors: black/red/green/yellow/blue/magenta/cyan/white/gray + Bright variants (redBright, etc.), hex (#ff0000), rgb(255,0,0).  
Background: prefix with `bg` (bgGreen, bgCyanBright).  
Styles: bold, dim, italic, underline, strikethrough, inverse.

### `<Newline>`, `<Spacer>`

```tsx
<Newline count={2} />       // n blank lines
<Spacer />                   // flex spacer
<Spacer height={3} />        // fixed height spacer
```

## Hooks

### `useInput` — Keyboard Input

```tsx
import { useInput } from 'ink';

useInput((input, key) => {
  if (key.escape || input === 'q') exit();           // exit on Escape or 'q'
  if (key.upArrow) navigateUp();
  if (key.downArrow) navigateDown();
  if (key.return) selectItem();
});
```

key object: upArrow, downArrow, leftArrow, rightArrow, return, escape, tab, backspace, delete, ctrl, shift, meta, space, pageUp, pageDown, home, end, f1–f12.

### `useApp` — App-Level Control

```tsx
import { useApp } from 'ink';
const { exit } = useApp();
exit();  // or exit(error)
```

### `useFocus` — Focus Management

```tsx
import { useFocus } from 'ink';
const { isFocused } = useFocus({ autoFocus: true });
// Style differently when focused
<Text color={isFocused ? 'blue' : 'dim'}>{label}</Text>
```

### `useStdin` / `useStdout` — Stream Access

```tsx
const { stdin, isRawModeSupported } = useStdin();
const { stdout } = useStdout();
```

## render() Options

```tsx
render(<App />, {
  exitOnCtrlC: true,         // default true
  debug: false,              // show Yoga layout debug
  patchConsole: true,        // suppress console output
});
```

## Common Patterns

### Select/Menu

```tsx
const Menu = ({ items, onSelect }) => {
  const [idx, setIdx] = useState(0);
  useInput((_, key) => {
    if (key.upArrow) setIdx(i => Math.max(0, i - 1));
    if (key.downArrow) setIdx(i => Math.min(items.length - 1, i + 1));
    if (key.return) onSelect(items[idx]);
  });
  return (
    <Box flexDirection="column">
      {items.map((item, i) => (
        <Text key={i} color={i === idx ? 'green' : undefined}>
          {i === idx ? '❯ ' : '  '}{item}
        </Text>
      ))}
    </Box>
  );
};
```

### Spinner (useEffect + setInterval)

```tsx
const Spinner = () => {
  const [frame, setFrame] = useState(0);
  const chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
  useEffect(() => {
    const id = setInterval(() => setFrame(f => (f + 1) % chars.length), 80);
    return () => clearInterval(id);
  }, []);
  return <Text>{chars[frame]} Loading...</Text>;
};
```

### Progress Bar

```tsx
const ProgressBar = ({ percent }) => {
  const filled = '█'.repeat(Math.round(percent / 5));
  const empty = '░'.repeat(20 - filled.length);
  return <Text>{filled}{empty} {percent}%</Text>;
};
```

### Input Field (useInput + useState)

```tsx
const Input = ({ onSubmit }) => {
  const [value, setValue] = useState('');
  useInput((input, key) => {
    if (key.return) { onSubmit(value); setValue(''); }
    else if (key.backspace) setValue(v => v.slice(0, -1));
    else if (input.length === 1 && !key.ctrl) setValue(v => v + input);
  });
  return <Text>❯ {value}<Text dim>█</Text></Text>;
};
```

## Resources

This skill includes:
- **[components.md](references/components.md)** — Full component and prop reference
- **[hooks.md](references/hooks.md)** — Hook API details and custom hook patterns
- **[examples.md](references/examples.md)** — Complete runnable examples (counter, table, loading, CLI arguments)

## Key Constraints

- **Node.js >= 22** required (ESM only)
- **React >= 19.2** is a peer dependency
- Only works in real terminal (no browser)
- Layout via Yoga Flexbox — units are characters/rows, not pixels
- No scrolling — the terminal viewport is the canvas
- Colors depend on terminal support (most modern terminals support 256-color)
- Interactive mode requires raw stdin (Ink enables it automatically)