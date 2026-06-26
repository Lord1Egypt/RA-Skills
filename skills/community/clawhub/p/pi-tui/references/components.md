# Built-in Component API

## Layout Components

**Container** — Child component container: `new Container(); container.addChild(c); container.removeChild(c)`

**Box** — Padding + background: `new Box(paddingX=1, paddingY=1, bgFn?)`, `.setBgFn(fn)` dynamically switch background

**Spacer** — Vertical spacing: `new Spacer(lines=1)`

## Text Components

**Text** — Multi-line text with word wrap: `new Text(content, paddingX=1, paddingY=1, bgFn?)`, `.setText(s)`

**TruncatedText** — Single-line truncation: `new TruncatedText(content, paddingX=0, paddingY=0)`

## Input Components

**Input** — Single-line input: `new Input()`, `.onSubmit`, `.setValue/getValue`. Shortcuts: Enter submit, Ctrl+A/E line start/end, Ctrl+W/Alt+Backspace delete word, Ctrl+U/K delete to line start/end

**Editor** — Multi-line editor:
```typescript
const editor = new Editor(tui, { borderColor, selectList }, { paddingX? });
editor.onSubmit = (text) => {};   // Enter to submit
editor.onChange = (text) => {};   // Content changed
editor.disableSubmit = true;      // Disable submit
editor.setAutocompleteProvider(p); // Autocomplete
```
Features: word wrap, slash command completion, file path completion, >10 line paste markers, fake cursor. Shortcuts: see `references/autocomplete.md`

## Display Components

**Markdown** — Render Markdown:
```typescript
new Markdown(text, paddingX, paddingY, theme, defaultStyle?)
// theme: { heading, link, linkUrl, code, codeBlock, codeBlockBorder, quote, quoteBorder,
//          hr, listBullet, bold, italic, strikethrough, underline, highlightCode? }
// defaultStyle: { color?, bgColor?, bold?, italic?, strikethrough?, underline? }
```
Supports headings/bold/italic/code blocks/lists/links/quotes/HTML tags (plain text)/syntax highlighting. `.setText(s)` to update.

**Loader** — Animated loading indicator: `new Loader(tui, spinnerColor, msgColor, "text")`, `.start()/.setMessage(s)/.stop()`

**CancellableLoader** — Cancellable loader: `new CancellableLoader(tui, spinnerColor, msgColor, "text")`, `.onAbort` Escape callback, `.signal` is AbortSignal

**Image** — Inline terminal images (Kitty/iTerm2 protocol):
```typescript
new Image(base64Data, "image/png", { fallbackColor }, { maxWidthCells?, maxHeightCells?, filename? })
```
Supports PNG/JPEG/GIF/WebP, dimensions auto-parsed. Falls back to placeholder on unsupported terminals.

## Interactive Components

**SelectList** — Selection list:
```typescript
new SelectList(items, maxVisible, { selectedPrefix, selectedText, description, scrollInfo, noMatch })
// items: { value, label, description? }[]
// .onSelect/.onCancel/.onSelectionChange/.setFilter(s)
```
Arrow keys navigate, Enter select, Escape cancel.

**SettingsList** — Settings panel:
```typescript
new SettingsList(items, maxVisible, { label, value, description, cursor, hint }, onChange, onCancel)
// items: { id, label, description?, currentValue, values?, submenu? }[]
// values provided → Enter/Space cycles values, submenu provided → opens submenu
// .updateValue(id, newValue)
```
Arrow keys navigate, Enter/Space activate, Escape cancel.