# Lifecycle & Core API

## Plugin Anatomy

An Obsidian plugin consists of three files:

| File | Required | Purpose |
|------|----------|---------|
| `main.js` | Yes | Compiled plugin code |
| `manifest.json` | Yes | Plugin metadata |
| `styles.css` | No | CSS styles |

### manifest.json

```json
{
  "id": "my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "minAppVersion": "1.0.0",
  "description": "Does something useful.",
  "author": "Author Name",
  "authorUrl": "https://example.com",
  "fundingUrl": "https://example.com/sponsor",
  "isDesktopOnly": false
}
```

**Rules:**
- `id` must not contain "obsidian"; must not end with "plugin"; must be lowercase only
- `name` must not contain "Obsidian"; must not end with "Plugin"; must not start with "Obsi" or end with "dian"
- `description` must not contain "Obsidian" or "This plugin"; must end with `.?!)` punctuation; max 250 chars
- `minAppVersion` is mandatory
- `isDesktopOnly: true` only if using Node.js/Electron APIs (`fs`, `crypto`, `os`)
- `manifest.json` `id`, `name`, `description` must match submission entry in `community-plugins.json`

## Plugin Class

```typescript
import { Plugin, Notice } from 'obsidian'

export default class MyPlugin extends Plugin {
  async onload() {
    // Load order matters:
    // 1. Settings first — UI depends on these
    await this.loadSettings()
    // 2. Settings tab
    this.addSettingTab(new MySettingTab(this.app, this))
    // 3. Commands
    this.addCommand({ id: 'hello', name: 'Say hello', callback: () => new Notice('Hi!') })
    // 4. Views
    this.registerView(MY_VIEW_TYPE, (leaf) => new MyView(leaf))
    // 5. Editor extensions
    this.registerEditorExtension(myCM6Extension)
    // 6. Ribbon icons
    this.addRibbonIcon('dice', 'Open view', () => this.activateView())
    // 7. Events
    this.registerEvent(this.app.vault.on('modify', this.onFileModify))
    this.registerDomEvent(document, 'click', this.onClick)
    this.registerInterval(window.setInterval(() => this.tick(), 1000))
  }

  async onunload() {
    // registerEvent/registerDomEvent/registerInterval — auto-cleaned
    // Manual cleanup: MutationObserver.disconnect(), React root.unmount()
    // ⚠️ NEVER call detachLeavesOfType() — Obsidian handles leaf cleanup automatically
  }
}
```

### Auto-Cleanup vs Manual Cleanup

| Method | Auto-Cleanup? | Notes |
|--------|---------------|-------|
| `registerEvent()` | ✅ | Preferred for all events |
| `registerDomEvent()` | ✅ | DOM events auto-removed |
| `registerInterval()` | ✅ | Interval auto-cleared |
| `registerEditorExtension()` | ✅ | CM6 extension auto-removed |
| `addCommand()` | ✅ | Command auto-unregistered |
| `addSettingTab()` | ✅ | Tab auto-removed |
| `MutationObserver` | ❌ | Must call `observer.disconnect()` in onunload |
| `vault.on()` in React useEffect | ❌ | Must call `app.vault.offref(ref)` in cleanup |
| `createRoot()` (React) | ❌ | Must call `root.unmount()` in cleanup |

### ⚠️ Critical: Never Detach Leaves in onunload()

This is the single most common rejection reason. The ESLint rule `detach-leaves` catches this.

```typescript
// ❌ WRONG — causes leaves to reinitialize on plugin update
async onunload() {
  this.app.workspace.detachLeavesOfType(MY_VIEW_TYPE)
}

// ✅ CORRECT — let Obsidian handle leaf cleanup
async onunload() {
  // Nothing needed here for leaves
}
```

**Why:** When you detach leaves in `onunload()`, Obsidian re-creates them on the next plugin load cycle (e.g., during hot-reload or settings change). This causes duplicate views and crashes. Obsidian's plugin system handles leaf cleanup automatically — your job is only to clean up things you manually created (MutationObserver, React roots, etc.).

### Component Lifecycle

`Plugin` extends `Component`. Key methods:

| Method | Purpose |
|--------|---------|
| `this.addChild(child)` | Add child component (auto-managed lifecycle) |
| `this.removeChild(child)` | Remove child component |
| `this.register(fn)` | Register a cleanup function |
| `this.load()` | Called when component is loaded |
| `this.unload()` | Called when component is unloaded |

**Never pass `this` (the plugin) as a Component to another class.** Use `this.addChild()` instead.

## Workspace & Views

### Getting Active Content

```typescript
// Get active file
const file = this.app.workspace.getActiveFile()

// Get active Markdown view
const view = this.app.workspace.getActiveViewOfType(MarkdownView)

// Get active editor
const editor = this.app.workspace.activeEditor?.editor

// Get all leaves of a type
const leaves = this.app.workspace.getLeavesOfType(MY_VIEW_TYPE)
```

### Custom Views (ItemView)

```typescript
import { ItemView, WorkspaceLeaf } from 'obsidian'

export const MY_VIEW_TYPE = 'my-view'

export class MyView extends ItemView {
  constructor(leaf: WorkspaceLeaf) {
    super(leaf)
  }

  getViewType() { return MY_VIEW_TYPE }
  getDisplayText() { return 'My view' }
  getIcon() { return 'dice' }

  async onOpen() {
    const container = this.containerEl.children[1]
    container.empty()
    container.createEl('h2', { text: 'Hello from my view' })
  }

  async onClose() {
    // Cleanup
  }
}
```

### Activating a View

```typescript
async activateView() {
  const existing = this.app.workspace.getLeavesOfType(MY_VIEW_TYPE)
  if (existing.length > 0) {
    this.app.workspace.revealLeaf(existing[0])
    return
  }
  const leaf = this.app.workspace.getRightLeaf(false)
  if (leaf) {
    await leaf.setViewState({ type: MY_VIEW_TYPE, active: true })
    this.app.workspace.revealLeaf(leaf)
  }
}
```

## Modals

```typescript
import { Modal, Setting } from 'obsidian'

export class MyModal extends Modal {
  result: string

  constructor(app: App) {
    super(app)
  }

  onOpen() {
    const { contentEl } = this
    contentEl.createEl('h2', { text: 'Enter your name' })

    new Setting(contentEl)
      .setName('Name')
      .addText((text) =>
        text.setPlaceholder('Your name').onChange((value) => {
          this.result = value
        })
      )

    new Setting(contentEl)
      .addButton((btn) =>
        btn.setButtonText('Submit').setCta().onClick(() => {
          this.close()
          this.onSubmit(this.result)
        })
      )
  }

  onClose() {
    this.contentEl.empty()
  }

  onSubmit(result: string) {
    // Handle result
  }
}
```

## Notices

```typescript
import { Notice } from 'obsidian'

// Basic notice (default 5 seconds)
new Notice('Hello!')

// Custom duration (ms)
new Notice('Long message', 10000)

// Persistent notice (0 = until dismissed)
new Notice('Important!', 0)
```

## Events

### Vault Events

```typescript
// File created
this.registerEvent(this.app.vault.on('create', (file) => {}))

// File modified
this.registerEvent(this.app.vault.on('modify', (file) => {}))

// File deleted
this.registerEvent(this.app.vault.on('delete', (file) => {}))

// File renamed
this.registerEvent(this.app.vault.on('rename', (file, oldPath) => {}))
```

### Workspace Events

```typescript
// File opened
this.registerEvent(this.app.workspace.on('file-open', (file) => {}))

// Active leaf changed
this.registerEvent(this.app.workspace.on('active-leaf-change', (leaf) => {}))

// Layout changed
this.registerEvent(this.app.workspace.on('layout-change', () => {}))

// Editor change (debounced)
this.registerEvent(this.app.workspace.on('editor-change', (editor, info) => {}))
```

### DOM Events

```typescript
// Click
this.registerDomEvent(document, 'click', (evt) => {})

// Keyboard
this.registerDomEvent(document, 'keydown', (evt) => {})

// Window resize
this.registerDomEvent(window, 'resize', (evt) => {})
```
