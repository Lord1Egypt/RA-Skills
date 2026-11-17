---
name: preact-docs-v10-29-7
description: "Documentation reference for Preact v10.29.7. Use to look up the correct syntax, hooks, components, and API behavior for Preact. Not a coding tutor — only a reference lookup. Example triggers: \"How does useState() work in Preact?\", \"What props does render() accept?\", \"What's the difference between preact and preact/compat?\""
version: 1.0.0
homepage: https://preactjs.com/guide/v10/
license: MIT
required_commands: []
required_environment_variables: []
required_privileges: none
metadata: {"hermes":{"emoji":"📚","category":"knowledge"},"required_binaries":[]}
---

# Preact v10.29.7 Documentation Reference

Look up Preact v10.29.7 syntax, hooks, components, and API behavior from the official docs.

## Requirements

- None. This skill is a read-only documentation reference.

## Quick Reference

| User wants... | Do this |
|---------------|---------|
| API reference (full surface) | Read `api-reference` from `scripts/preact-reference.json` |
| Hooks (useState, useEffect, etc.) | Read `hooks` from `scripts/preact-reference.json` |
| Components (Fragment, Context) | Read `components` from `scripts/preact-reference.json` |
| Context API | Read `context` from `scripts/preact-reference.json` |
| Forms guidance | Read `forms` from `scripts/preact-reference.json` |
| Debugging tools | Read `debugging` from `scripts/preact-reference.json` |
| Preact vs React differences | Read `differences-to-react` from `scripts/preact-reference.json` |
| Getting started | Read `getting-started` from `scripts/preact-reference.json` |
| Preact CLI | Read `cli` from `scripts/preact-reference.json` |
| Options/config | Read `options` from `scripts/preact-reference.json` |

## Important Rules

1. **This is a reference lookup skill, not a coding teacher.** Use it to verify Preact syntax, hook signatures, and API behavior. Do not use it to generate entire apps from scratch.
2. **Background knowledge:** Preact is based on concepts from React. If the user has zero React/JSX background (e.g., doesn't know about `className`, JSX, or hooks), point them to [React's Getting Started guide](https://react.dev/learn) first before using this Preact reference.
3. **Always** check `differences-to-react.md` first when user mentions React or React-like behavior — this is the #1 source of agent mistakes when mental model is React
4. **Always** search `scripts/preact-reference.json` for Preact-specific answers
5. **Cite** category and slug when providing guidance (e.g., "api-reference" for full API, "differences-to-react" for React comparisons)
6. **Flag** `preact/compat` requirement for React ecosystem libraries — don't assume they work with vanilla Preact
7. **Distinguish** between `h()` function and JSX — both work but have different use cases

## Usage Guide

This skill provides read-only access to the official Preact v10.29.7 documentation. Use it to answer questions like:

- "How does `useState()` work in Preact?"
- "What props does `render()` accept?"
- "What's the difference between `preact` and `preact/compat`?"
- "How do I import `useEffect`?"

Do not use this skill to teach Preact from scratch or to generate whole projects.

### Basic Pattern

```javascript
// In your code
const fs = require('fs');
const reference = JSON.parse(fs.readFileSync('{baseDir}/scripts/preact-reference.json', 'utf8'));

// Search for specific hook
const result = reference.find(item => 
  item.category === "hooks" && 
  item.slug.includes("hooks")
);
```

### Critical Knowledge: Preact vs React

**This is the most important page** — read `differences-to-react` category thoroughly before answering any Preact/React compatibility questions.

Key differences:
- **No Synthetic Events** — Preact uses native DOM events
- **Different children handling** — Preact passes `children` as prop, React uses `props.children`
- **Component lifecycles** — Some lifecycle methods behave differently
- **Context API** — Similar but not identical to React
- **Hooks** — Mostly compatible, but subtle differences exist

### When to use `preact/compat`

Use `preact/compat` (alias for `react` and `react-dom`) when:
- Importing React ecosystem libraries (Redux, React Router, Material-UI, etc.)
- Working with code that expects React APIs
- Needing drop-in React compatibility

Do NOT use `preact/compat` when:
- Writing new Preact-native code
- Building lightweight apps where bundle size matters
- Using Preact-specific features

### Search Strategy

1. **API surface** → `category="api-reference"` — complete API in one place
2. **Hooks** → `category="hooks"` — useState, useEffect, useContext, etc.
3. **React differences** → `category="differences-to-react"` — critical for React devs
4. **Components** → `category="components"` — Fragment, Context, etc.
5. **Context** → `category="context"` — Provider/Consumer pattern
6. **Forms** → `category="forms"` — controlled components, refs
7. **Debugging** → `category="debugging"` — devtools, warnings
8. **CLI** → `category="cli"` — Preact CLI usage
9. **Options** → `category="options"` — configuration options

## Key API Reference

| Topic | Category | Key exports |
|-------|----------|-------------|
| Core | `api-reference` | `h()`, `render()`, `Component`, `Fragment` |
| Hooks | `hooks` | `useState`, `useEffect`, `useContext`, `useRef`, `useReducer`, `useMemo`, `useCallback` |
| Components | `components` | `Fragment`, `Portal`, `Suspense` |
| Context | `context` | `createContext`, `Provider`, `Consumer` |
| Compat | `differences-to-react` | `preact/compat` alias for React ecosystem |

## Common Usage Examples

### Functional component with hooks

```jsx
import { h, render } from 'preact';
import { useState, useEffect } from 'preact/hooks';

function Counter() {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    console.log('Count changed:', count);
  }, [count]);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}

render(<Counter />, document.getElementById('app'));
```

### Using preact/compat for React libraries

```jsx
// Instead of: import React from 'react';
import { h, Component } from 'preact';
// Or use the compat layer:
import React from 'preact/compat';
import ReactDOM from 'preact/compat';

// Now you can use React Router, Redux, etc.
import { BrowserRouter } from 'react-router-dom';
```

### Context usage

```jsx
import { createContext, useContext } from 'preact/hooks';

const ThemeContext = createContext('light');

function ThemedButton() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Themed</button>;
}

// Provider usage
<ThemeContext.Provider value="dark">
  <ThemedButton />
</ThemeContext.Provider>
```

## Gotchas

- **React libraries require `preact/compat`** — vanilla Preact won't work with most React ecosystem packages
- **JSX vs `h()`** — both work, but `h()` is the native Preact function; JSX compiles to `h()`
- **Event handlers** — Preact uses native DOM events, not SyntheticEvent like React
- **Children prop** — Preact passes `children` differently than React in some edge cases
- **Lifecycle methods** — `componentWillMount`, `componentWillReceiveProps` behave differently or are deprecated
- **DevTools** — Preact DevTools extension exists but is separate from React DevTools
- **Server-side rendering** — Use `preact-render-to-string` package, not React's SSR APIs

## Critical Differences from React

| Feature | React | Preact |
|---------|-------|--------|
| Bundle size | ~40KB | ~3KB |
| Synthetic events | Yes | No (native events) |
| Children handling | `props.children` | Passed as prop, different edge cases |
| createContext default | `undefined` | `null` |
| useEffect cleanup | Fires after paint | Fires before next effect |
| Fragment syntax | `<></>` | Same, but different internal representation |
| Error boundaries | Full support | Limited support |

## Further Reading

- `{baseDir}/scripts/preact-reference.json` — Complete Preact v10.29.7 documentation index (embedded in skill)
- [Preact official guide](https://preactjs.com/guide/v10/) — Live documentation
- `differences-to-react` category — **Must-read for React developers**
