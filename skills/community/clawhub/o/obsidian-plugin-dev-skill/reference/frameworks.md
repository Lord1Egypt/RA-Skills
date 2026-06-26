# React / Svelte / Vue Integration

## React Integration

### Mounting in ItemView

```typescript
import { ItemView, WorkspaceLeaf } from 'obsidian'
import { Root, createRoot } from 'react-dom/client'
import { StrictMode } from 'react'
import App from './App'

export const REACT_VIEW_TYPE = 'react-view'

export class ReactView extends ItemView {
  root: Root | null = null

  constructor(leaf: WorkspaceLeaf) {
    super(leaf)
  }

  getViewType() { return REACT_VIEW_TYPE }
  getDisplayText() { return 'React view' }
  getIcon() { return 'atom' }

  async onOpen() {
    // containerEl.children[1] is the content area (children[0] is header)
    const container = this.containerEl.children[1]
    container.empty()
    this.root = createRoot(container)
    this.root.render(
      <StrictMode>
        <App plugin={this.app} />
      </StrictMode>
    )
  }

  async onClose() {
    // CRITICAL: manually unmount React root
    this.root?.unmount()
    this.root = null
  }
}
```

### Mounting in PluginSettingTab

```typescript
import { PluginSettingTab } from 'obsidian'
import { Root, createRoot } from 'react-dom/client'
import SettingsApp from './SettingsApp'

export class MySettingTab extends PluginSettingTab {
  root: Root | null = null

  display() {
    const { containerEl } = this
    containerEl.empty()
    this.root = createRoot(containerEl)
    this.root.render(<SettingsApp plugin={this.plugin} />)
  }

  hide() {
    // CRITICAL: unmount when tab is hidden
    this.root?.unmount()
    this.root = null
  }
}
```

### Error Boundary

Always wrap React components in an ErrorBoundary to prevent plugin crashes.

```typescript
import React, { Component, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-boundary">
          <p>Something went wrong.</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Retry
          </button>
        </div>
      )
    }
    return this.props.children
  }
}

// Usage:
this.root.render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
)
```

### Passing Obsidian App to React

```typescript
import { createContext, useContext } from 'react'
import { App } from 'obsidian'

const AppContext = createContext<App | null>(null)

export const useObsidianApp = (): App => {
  const app = useContext(AppContext)
  if (!app) throw new Error('useObsidianApp must be used within AppContext.Provider')
  return app
}

// In view:
this.root.render(
  <AppContext.Provider value={this.app}>
    <App />
  </AppContext.Provider>
)

// In any component:
function MyComponent() {
  const app = useObsidianApp()
  const file = app.workspace.getActiveFile()
  // ...
}
```

### Vault Events in React Components

```typescript
import { useEffect, useState } from 'react'
import { debounce } from 'obsidian'

function FileList() {
  const app = useObsidianApp()
  const [files, setFiles] = useState<string[]>([])

  useEffect(() => {
    const refresh = debounce(() => {
      setFiles(app.vault.getMarkdownFiles().map(f => f.path))
    }, 500, false)

    const ref = app.vault.on('modify', refresh)
    refresh()

    // CRITICAL: cleanup with offref + cancel
    return () => {
      app.vault.offref(ref)
      refresh.cancel()
    }
  }, [app])

  return <ul>{files.map(f => <li key={f}>{f}</li>)}</ul>
}
```

## Svelte Integration

```svelte
<!-- MyComponent.svelte -->
<script>
  import { App } from 'obsidian'
  export let app
  
  let file = app.workspace.getActiveFile()
  
  function handleClick() {
    new Notice('Clicked!')
  }
</script>

<div class="my-svelte-component">
  <p>Active: {file?.name ?? 'No file'}</p>
  <button on:click={handleClick}>Click me</button>
</div>
```

```typescript
// View with Svelte
import MyComponent from './MyComponent.svelte'

export class SvelteView extends ItemView {
  component: MyComponent | null = null

  async onOpen() {
    const container = this.containerEl.children[1]
    container.empty()
    this.component = new MyComponent({
      target: container,
      props: { app: this.app }
    })
  }

  async onClose() {
    this.component?.$destroy()
    this.component = null
  }
}
```

## Vue Integration

```typescript
import { createApp } from 'vue'
import MyComponent from './MyComponent.vue'

export class VueView extends ItemView {
  app: ReturnType<typeof createApp> | null = null

  async onOpen() {
    const container = this.containerEl.children[1]
    container.empty()
    this.app = createApp(MyComponent, { app: this.app })
    this.app.mount(container)
  }

  async onClose() {
    this.app?.unmount()
    this.app = null
  }
}
```

## Common Patterns

### Helper: Unmount Root

```typescript
// Extract to avoid duplication
function unmountRoot(root: Root | null) {
  root?.unmount()
  return null
}

// Usage in onClose/Hide:
async onClose() {
  this.root = unmountRoot(this.root)
}
```

### Using Obsidian CSS Variables in React/Svelte

```css
/* Always use Obsidian CSS variables */
.my-component {
  color: var(--text-normal);
  background: var(--background-primary);
  border: 1px solid var(--background-modifier-border);
  border-radius: var(--radius-s);
  padding: var(--size-4-2);
}

.my-button {
  background: var(--interactive-accent);
  color: var(--text-on-accent);
}

/* Theme-specific */
.theme-dark .my-component { /* dark overrides */ }
.theme-light .my-component { /* light overrides */ }

/* Mobile */
.is-mobile .my-component { /* mobile overrides */ }
```

## Best Practices

1. **Always unmount in `onClose()`/`hide()`** — memory leaks are the #1 issue
2. **Use ErrorBoundary** — prevent a React error from crashing the plugin
3. **Don't pass the Plugin as a prop** — pass `app` via context instead
4. **Use `vault.offref()`** in React useEffect cleanup, not `vault.off()`
5. **Debounce event handlers** — Obsidian fires events rapidly
6. **Use `containerEl.children[1]`** — children[0] is Obsidian's header element
