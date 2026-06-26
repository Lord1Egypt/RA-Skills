# Ink Examples

All examples require `tsx` to run (tsx handles TSX compilation): `node --import=tsx index.tsx`
Or compile first with `tsc` and run with `node build/index.js`.

## 1. Minimal App

```tsx
// index.tsx
import { render, Text } from 'ink';

render(<Text>Hello from Ink!</Text>);
```

## 2. Interactive Counter

```tsx
import { useState } from 'react';
import { render, Box, Text, useInput } from 'ink';

function Counter() {
  const [count, setCount] = useState(0);

  useInput((input) => {
    if (input === '+') setCount(c => c + 1);
    if (input === '-') setCount(c => c - 1);
    if (input === 'r') setCount(0);
  });

  return (
    <Box flexDirection="column" alignItems="center" padding={1}>
      <Text bold color="cyan">Counter</Text>
      <Text color="yellow">{count}</Text>
      <Box marginTop={1}>
        <Text dim>+/− to change, r to reset, q to quit</Text>
      </Box>
    </Box>
  );
}

render(<Counter />);
```

## 3. Select Menu with Arrow Keys

```tsx
import { useState } from 'react';
import { render, Box, Text, useInput } from 'ink';

const OPTIONS = ['Install', 'Update', 'Remove', 'Exit'];

function Menu() {
  const [selected, setSelected] = useState(0);

  useInput((_, key) => {
    if (key.upArrow)   setSelected(i => Math.max(0, i - 1));
    if (key.downArrow) setSelected(i => Math.min(OPTIONS.length - 1, i + 1));
    if (key.return)    console.log(`Selected: ${OPTIONS[selected]}`);
  });

  return (
    <Box flexDirection="column" borderStyle="round" padding={1}>
      <Text bold>Main Menu</Text>
      <Box flexDirection="column" marginTop={1}>
        {OPTIONS.map((opt, i) => (
          <Text key={i} color={i === selected ? 'green' : undefined}>
            {i === selected ? '❯ ' : '  '}{opt}
          </Text>
        ))}
      </Box>
    </Box>
  );
}

render(<Menu />);
```

## 4. CLI Arguments with meow

```tsx
import meow from 'meow';
import { render, Box, Text, Newline } from 'ink';

const cli = meow(`
  Usage
    $ hello <name>

  Options
    --shout   Use all caps
`, { importMeta: import.meta });

function App({ name, shout }: { name: string; shout: boolean }) {
  const display = shout ? name.toUpperCase() : name;
  return (
    <Box flexDirection="column" padding={1}>
      <Text color="green">Hello, {display}!</Text>
    </Box>
  );
}

const name = cli.input[0] || 'World';
render(<App name={name} shout={cli.flags.shout} />);
```

## 5. Task Runner / Spinner

```tsx
import { useState, useEffect } from 'react';
import { render, Box, Text } from 'ink';

const FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];

function TaskRunner() {
  const [frame, setFrame] = useState(0);
  const [tasks, setTasks] = useState([
    { label: 'Installing dependencies', status: 'pending' },
    { label: 'Building project', status: 'pending' },
    { label: 'Running tests', status: 'pending' },
  ]);

  // Spinner animation
  useEffect(() => {
    const id = setInterval(() => setFrame(f => (f + 1) % FRAMES.length), 80);
    return () => clearInterval(id);
  }, []);

  // Simulate task progress
  useEffect(() => {
    const finish = (i: number) => {
      if (i >= tasks.length) return;
      setTasks(prev => prev.map((t, j) => j === i ? { ...t, status: 'done' } : t));
      setTimeout(() => finish(i + 1), 1000 + Math.random() * 1000);
    };
    setTimeout(() => finish(0), 500);
  }, []);

  return (
    <Box flexDirection="column" padding={1}>
      <Text bold>Task Runner</Text>
      <Box flexDirection="column" marginTop={1}>
        {tasks.map((task, i) => (
          <Box key={i}>
            <Text width={2}>
              {task.status === 'pending' && <Text color="yellow">{FRAMES[frame]}</Text>}
              {task.status === 'done' && <Text color="green">✓</Text>}
              {task.status === 'error' && <Text color="red">✗</Text>}
            </Text>
            <Text dim={task.status === 'done'}>
              {task.label}
            </Text>
          </Box>
        ))}
      </Box>
    </Box>
  );
}

render(<TaskRunner />);
```

## 6. Table Renderer

```tsx
import { Box, Text } from 'ink';

interface TableProps {
  headers: string[];
  rows: string[][];
  widths?: number[];
}

function Table({ headers, rows, widths }: TableProps) {
  const cols = widths || headers.map(() => 15);

  return (
    <Box flexDirection="column">
      {/* Header */}
      <Box borderStyle="round" paddingX={1}>
        {headers.map((h, i) => (
          <Box key={i} width={cols[i]}>
            <Text bold color="cyan">{h}</Text>
          </Box>
        ))}
      </Box>
      {/* Rows */}
      {rows.map((row, i) => (
        <Box key={i} paddingX={1}>
          {row.map((cell, j) => (
            <Box key={j} width={cols[j]}>
              <Text wrap="truncate-end">{cell}</Text>
            </Box>
          ))}
        </Box>
      ))}
    </Box>
  );
}

// Usage:
const headers = ['Name', 'Version', 'Size'];
const rows = [
  ['react', '19.2.0', '12.4 kB'],
  ['ink', '7.0.3', '537 kB'],
  ['chalk', '5.6.2', '8.2 kB'],
];

render(<Table headers={headers} rows={rows} />);
```

## 7. Debug Setup (render options)

```tsx
render(<App />, {
  exitOnCtrlC: true,      // Default behavior
  debug: false,            // Set true for Yoga layout output
  patchConsole: true,      // Suppress console in rendered area
});
```

## 8. Error Boundary

```tsx
import { render, Text } from 'ink';
import React from 'react';

class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  state = { hasError: false };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <Text color="red">Fatal: {this.state.error.message}</Text>
      );
    }
    return this.props.children;
  }
}

render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
);
```

## 9. Searchable List with Filter

```tsx
import { useState} from 'react';
import { render, Box, Text, useInput } from 'ink';

const ITEMS = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape'];

function SearchableList() {
  const [filter, setFilter] = useState('');
  const [selected, setSelected] = useState(0);

  const filtered = ITEMS.filter(item =>
    item.toLowerCase().includes(filter.toLowerCase())
  );

  useInput((input, key) => {
    if (key.upArrow)   setSelected(i => Math.max(0, i - 1));
    if (key.downArrow) setSelected(i => Math.min(filtered.length - 1, i + 1));
    else if (key.backspace) setFilter(f => f.slice(0, -1));
    else if (input.length === 1 && !key.ctrl && !key.meta) setFilter(f => f + input);
  });

  return (
    <Box flexDirection="column" padding={1}>
      <Text>Search: <Text color="yellow">{filter}_</Text></Text>
      <Box flexDirection="column" marginTop={1}>
        {filtered.slice(0, 10).map((item, i) => (
          <Text key={i} color={i === selected ? 'green' : undefined}>
            {i === selected ? '❯ ' : '  '}{item}
          </Text>
        ))}
        {filtered.length === 0 && <Text dim>No results</Text>}
      </Box>
    </Box>
  );
}

render(<SearchableList />);
```