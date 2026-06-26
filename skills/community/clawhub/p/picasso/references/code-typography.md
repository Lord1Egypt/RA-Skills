# Code Typography Reference

## Table of Contents
1. Monospace Font Selection
2. Code Block Design
3. Syntax Highlighting Accessibility
4. Copy-to-Clipboard
5. Responsive Code Blocks
6. Inline Code Styling
7. Diff Views
8. Terminal Output
9. Common Mistakes

---

## 1. Monospace Font Selection

| Font | Ligatures | Style | Best For |
|---|---|---|---|
| JetBrains Mono | Yes | Clean, geometric | General purpose, IDEs |
| Fira Code | Yes | Slightly rounded | Tutorials, docs |
| Source Code Pro | No | Adobe, professional | Enterprise, clean look |
| IBM Plex Mono | No | Corporate, legible | Documentation |
| Geist Mono | No | Vercel, modern | Next.js projects |
| Cascadia Code | Yes | Microsoft, playful | Terminals |

```css
code, pre, .mono {
  font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
  font-feature-settings: 'liga' 1, 'calt' 1; /* enable ligatures */
  font-variant-ligatures: common-ligatures;
}
```

Ligatures: `=>` becomes ⇒, `!==` becomes ≢, `>=` becomes ≥. Enable for display, disable for editing if users copy code.

---

## 2. Code Block Design

```css
pre {
  background: var(--surface-1);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  font-size: 0.875rem;    /* 14px — slightly smaller than body */
  line-height: 1.65;       /* Looser than body text for readability */
  overflow-x: auto;
  tab-size: 2;
  -moz-tab-size: 2;
}

/* Dark mode code blocks on light sites */
[data-theme="light"] pre {
  background: oklch(0.14 0.02 230);
  color: oklch(0.90 0.01 230);
}
```

Line numbers (optional):
```css
pre.line-numbers {
  counter-reset: line;
  padding-left: 3.5rem;
  position: relative;
}
pre.line-numbers .line::before {
  counter-increment: line;
  content: counter(line);
  position: absolute;
  left: 1rem;
  color: var(--text-muted);
  font-size: 0.75rem;
  user-select: none; /* don't copy line numbers */
}
```

---

## 3. Syntax Highlighting Accessibility

Every token color must have **minimum 3:1 contrast** against the code block background. Don't rely on color alone — use font-weight or font-style for emphasis.

| Token Type | Suggested OKLCH (dark bg) | Purpose |
|---|---|---|
| Keywords | `oklch(0.75 0.15 300)` | purple-ish, bold |
| Strings | `oklch(0.72 0.14 150)` | green |
| Numbers | `oklch(0.75 0.12 60)` | amber |
| Comments | `oklch(0.50 0.01 230)` | muted, italic |
| Functions | `oklch(0.78 0.10 230)` | blue |
| Variables | `oklch(0.85 0.01 230)` | near-white |

```css
.token-keyword { color: oklch(0.75 0.15 300); font-weight: 600; }
.token-string { color: oklch(0.72 0.14 150); }
.token-comment { color: oklch(0.50 0.01 230); font-style: italic; }
```

---

## 4. Copy-to-Clipboard

Position: top-right corner of the code block. Show on hover. Provide visual feedback.

```jsx
function CopyButton({ code }) {
  const [copied, setCopied] = useState(false);

  return (
    <button
      onClick={() => {
        navigator.clipboard.writeText(code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }}
      className="absolute top-2 right-2 p-1.5 rounded-md bg-white/5 hover:bg-white/10 text-xs text-muted"
      aria-label="Copy code"
    >
      {copied ? 'Copied' : 'Copy'}
    </button>
  );
}
```

---

## 5. Responsive Code Blocks

Code blocks should **scroll horizontally** on mobile, never wrap. Terminal output CAN wrap.

```css
pre {
  overflow-x: auto;
  white-space: pre;         /* code: no wrap */
  -webkit-overflow-scrolling: touch; /* smooth scroll on iOS */
}

pre.terminal {
  white-space: pre-wrap;    /* terminal: wrap is OK */
  word-break: break-all;
}

/* Hide scrollbar but keep functionality */
pre::-webkit-scrollbar { height: 4px; }
pre::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
```

On very small screens (< 375px), consider reducing code font-size to 12px.

---

## 6. Inline Code Styling

Inline code needs subtle visual distinction from body text:

```css
code:not(pre code) {
  background: var(--surface-2);
  padding: 0.15em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;        /* slightly smaller than surrounding text */
  font-weight: 500;
  border: 1px solid var(--border);
}
```

Never use inline code for emphasis. It's for code references (`useState`, `border-radius`, `GET /api/users`), not for highlighting words.

---

## 7. Diff Views

Use color + icon, not color alone (colorblind users):

```css
.diff-add {
  background: oklch(0.62 0.19 150 / 0.1);
  border-left: 3px solid oklch(0.62 0.19 150);
}
.diff-add::before { content: '+'; color: oklch(0.62 0.19 150); }

.diff-remove {
  background: oklch(0.55 0.22 25 / 0.1);
  border-left: 3px solid oklch(0.55 0.22 25);
  text-decoration: line-through;
  opacity: 0.7;
}
.diff-remove::before { content: '-'; color: oklch(0.55 0.22 25); }
```

---

## 8. Terminal Output

Terminal/console styling should feel distinct from code:

```css
.terminal {
  background: oklch(0.08 0.01 230);
  color: oklch(0.80 0.01 150); /* slight green tint for terminal feel */
  font-family: 'JetBrains Mono', monospace;
  padding: 1rem;
  border-radius: 8px;
}
.terminal .prompt { color: oklch(0.65 0.10 230); } /* blue prompt */
.terminal .output { color: oklch(0.75 0.01 230); } /* neutral output */
.terminal .error { color: oklch(0.65 0.22 25); }   /* red errors */
```

---

## 9. Common Mistakes

- **Code font too large.** 14px for blocks, 0.9em for inline. Larger fights with body text.
- **No horizontal scroll on code blocks.** Wrapping code breaks readability. Always `overflow-x: auto`.
- **Syntax colors with < 3:1 contrast.** Comments especially — they tend to be too faint.
- **Color-only diff indication.** Always add + / - markers or icons alongside color.
- **Copying includes line numbers.** Use `user-select: none` on line number elements.
- **Same styling for code blocks and terminal.** They serve different purposes. Terminal gets darker bg, green tint.
- **`font-family: monospace` without named fonts.** Browsers default to Courier New which looks dated. Always specify a modern monospace font first.
- **No copy button.** Users shouldn't have to triple-click and drag to copy code.
