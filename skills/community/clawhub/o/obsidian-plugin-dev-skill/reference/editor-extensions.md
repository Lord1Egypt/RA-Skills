# CodeMirror 6 Editor Extensions

## Overview

Obsidian uses CodeMirror 6 (CM6) for its editor. Plugins extend the editor using CM6's extension system via `registerEditorExtension()`.

## Key Concepts

| Concept | Purpose |
|---------|---------|
| **StateField** | Store data attached to editor state |
| **ViewPlugin** | React to editor view changes, manage decorations |
| **Decoration** | Visual overlays, marks, widgets on editor content |
| **EditorState** | Immutable editor state (doc, selection, extensions) |
| **EditorView** | DOM representation of editor state |
| **Transaction** | State change (edit, selection change, etc.) |

## StateField

Use `StateField` to store computed data derived from the document.

```typescript
import { StateField, EditorState } from '@codemirror/state'

const wordCountField = StateField.define<number>({
  create(state: EditorState) {
    return state.doc.length
  },
  update(value, tr) {
    if (tr.docChanged) {
      return tr.state.doc.length
    }
    return value
  }
})

// Register
this.registerEditorExtension(wordCountField)
```

## ViewPlugin with Decorations

Use `ViewPlugin` to create decorations that respond to document changes.

```typescript
import { ViewPlugin, Decoration, DecorationSet, ViewUpdate } from '@codemirror/view'
import { RangeSetBuilder } from '@codemirror/state'

const highlightPlugin = ViewPlugin.fromClass(
  class {
    decorations: DecorationSet

    constructor(view: EditorView) {
      this.decorations = this.buildDecorations(view)
    }

    update(update: ViewUpdate) {
      if (update.docChanged || update.viewportChanged) {
        this.decorations = this.buildDecorations(update.view)
      }
    }

    buildDecorations(view: EditorView): DecorationSet {
      const builder = new RangeSetBuilder<Decoration>()
      for (const { from, to } of view.visibleRanges) {
        const text = view.state.doc.sliceString(from, to)
        // Find patterns and add decorations
        const regex = /\bTODO\b/g
        let match
        while ((match = regex.exec(text)) !== null) {
          const start = from + match.index
          const end = start + match[0].length
          builder.add(start, end, Decoration.mark({
            class: 'my-highlight'
          }))
        }
      }
      return builder.finish()
    }
  },
  { decorations: (v) => v.decorations }
)
```

## Widget Decoration

Insert custom DOM elements into the editor.

```typescript
import { WidgetType } from '@codemirror/view'

class TaskCheckboxWidget extends WidgetType {
  constructor(readonly checked: boolean) {
    super()
  }

  toDOM() {
    const checkbox = document.createElement('input')
    checkbox.type = 'checkbox'
    checkbox.checked = this.checked
    checkbox.className = 'task-checkbox'
    return checkbox
  }

  eq(other: TaskCheckboxWidget) {
    return this.checked === other.checked
  }

  ignoreEvent() { return false }
}

// Usage in a ViewPlugin:
const widget = Decoration.widget({
  widget: new TaskCheckboxWidget(true),
  side: -1  // Place before the position
})
builder.add(pos, pos, widget)
```

## Mark Decoration

Wrap text with a CSS class or inline styles.

```typescript
const mark = Decoration.mark({
  class: 'my-inline-highlight',
  attributes: { 'data-type': 'highlight' }
})

// CSS:
// .my-inline-highlight { background: var(--text-highlight-bg); }
```

## Inline Decoration

Add CSS styles directly to text ranges.

```typescript
const deco = Decoration.mark({
  class: 'red-text',
  // Or use inline styles (prefer CSS class instead)
})
```

## Reading Editor Content

```typescript
// Get full document
const doc = view.state.doc.toString()

// Get line
const line = view.state.doc.lineAt(pos)

// Get selected text
const selection = view.state.sliceDoc(
  view.state.selection.main.from,
  view.state.selection.main.to
)

// Position from coordinates
const pos = view.posAtCoords({ x: 100, y: 200 })

// Coordinates from position
const coords = view.coordsAtPos(pos)
```

## Editor Commands

```typescript
import { KeyBinding } from '@codemirror/view'

const myKeymap: KeyBinding[] = [
  {
    key: 'Mod-b',
    run: (view) => {
      const { from, to } = view.state.selection.main
      const selected = view.state.sliceDoc(from, to)
      view.dispatch({
        changes: { from, to, insert: `**${selected}**` }
      })
      return true
    }
  }
]
```

## Live Preview vs Reading Mode

| Mode | How to Access | Behavior |
|------|---------------|----------|
| **Live Preview** | Default editing mode | Decorations visible in editor |
| **Reading Mode** | Preview tab | Use `registerMarkdownPostProcessor()` instead |

**Important:** Decorations from CM6 extensions only appear in Live Preview. For Reading mode, use `registerMarkdownPostProcessor()`.

```typescript
// Reading mode post-processing
this.registerMarkdownPostProcessor((element, context) => {
  // Modify rendered HTML
  element.querySelectorAll('code').forEach((code) => {
    // Process code blocks
  })
})
```

## Code Block Processor

```typescript
this.registerMarkdownCodeBlockProcessor('my-lang', (source, el, ctx) => {
  el.createEl('pre', { text: source })
  // Or render custom UI
})
```

## Practical Example: Inline Link Preview

```typescript
const linkPreviewPlugin = ViewPlugin.fromClass(
  class {
    decorations: DecorationSet
    constructor(view: EditorView) {
      this.decorations = this.buildDecorations(view)
    }
    update(update: ViewUpdate) {
      if (update.docChanged) this.decorations = this.buildDecorations(update.view)
    }
    buildDecorations(view: EditorView): DecorationSet {
      const builder = new RangeSetBuilder<Decoration>()
      const doc = view.state.doc.toString()
      const wikiLinkRegex = /\[\[([^\]]+)\]\]/g
      let match
      while ((match = wikiLinkRegex.exec(doc)) !== null) {
        const from = match.index
        const end = from + match[0].length
        builder.add(from, end, Decoration.mark({ class: 'wiki-link-inline' }))
      }
      return builder.finish()
    }
  },
  { decorations: (v) => v.decorations }
)
```

## CSS for Decorations

```css
.my-highlight {
  background: var(--text-highlight-bg);
  border-radius: 2px;
}

.my-inline-highlight {
  color: var(--text-accent);
  font-weight: bold;
}

.task-checkbox {
  margin-right: 4px;
  vertical-align: middle;
}
```

## Theme-Aware Decoration CSS

Always provide `.theme-dark` and `.theme-light` variants for decoration classes. Even though Obsidian CSS variables auto-adapt, explicit theme blocks handle edge cases (transparency, hover states, subtle borders).

```css
/* Base styles — use Obsidian vars for auto-adaptation */
.my-decoration {
  background-color: var(--background-modifier-hover);
  border-radius: var(--radius-s);
  color: var(--text-normal);
}

/* Dark mode refinements — adjust opacity and borders */
.theme-dark .my-decoration {
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

/* Light mode refinements */
.theme-light .my-decoration {
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

For CM6 `EditorView.baseTheme()`, register theme styles directly in the extension. Use Obsidian CSS variables as fallbacks:

```typescript
import { EditorView } from '@codemirror/view'

const myTheme = EditorView.baseTheme({
  '.cm-my-decoration': {
    backgroundColor: 'var(--background-modifier-hover)',
    borderRadius: 'var(--radius-s)',
    padding: '0 2px',
  },
  // Dark-specific overrides via nested selector
  '&dark .cm-my-decoration': {
    borderColor: 'rgba(255, 255, 255, 0.08)',
  },
  '&light .cm-my-decoration': {
    borderColor: 'rgba(0, 0, 0, 0.08)',
  },
})
```

**Rule of thumb:** If your decoration uses `background-color`, `border`, `box-shadow`, or `opacity`, always add `.theme-dark` / `.theme-light` variants. Purely semantic styles (font-weight, border-radius) don't need them.

## Best Practices

1. **Always provide `eq()` in WidgetType** — prevents unnecessary DOM re-creation
2. **Use `view.visibleRanges`** — only process visible content for performance
3. **Debounce rebuilds** — don't rebuild decorations on every keystroke
4. **Use CSS variables** — `var(--text-normal)`, `var(--background-modifier-border)`, etc.
5. **Avoid `innerHTML`** — use DOM API in `toDOM()`
6. **Extensions are auto-cleaned** — `registerEditorExtension()` handles cleanup
