# Usage and API

Use this file for practical usage patterns, API options, and when to choose SVG vs ASCII.

## Environments

### Node.js / Bun

```typescript
import { renderMermaidAscii } from 'beautiful-mermaid'
// CommonJS: const { renderMermaidAscii } = require('beautiful-mermaid')

const ascii = renderMermaidAscii(`graph LR\n  A --> B`)
console.log(ascii)
```

### Browser (CDN)

```html
<script src="https://unpkg.com/beautiful-mermaid/dist/beautiful-mermaid.browser.global.js"></script>
<script>
  const { renderMermaidAscii } = beautifulMermaid
  const ascii = renderMermaidAscii('graph LR; A-->B')
  console.log(ascii)
</script>
```

## Sync vs Async

```typescript
import { renderMermaid, renderMermaidAscii } from 'beautiful-mermaid'

const ascii = renderMermaidAscii(`graph LR\n  A --> B`) // sync
const svg = await renderMermaid(`graph LR\n  A --> B`)  // async
```

## AsciiRenderOptions

| Option | Type | Default | Range | Effect |
|--------|------|---------|-------|--------|
| `useAscii` | `boolean` | `false` | `true` / `false` | `true` uses pure ASCII, `false` uses Unicode box-drawing |
| `paddingX` | `number` | `5` | `0` - `20` | Horizontal spacing between nodes |
| `paddingY` | `number` | `5` | `0` - `20` | Vertical spacing between nodes |
| `boxBorderPadding` | `number` | `1` | `0` - `3` | Padding between label and box border |

## SVG vs ASCII

Use `renderMermaid` (SVG) when you need themes, interactivity, or scalable output. Use `renderMermaidAscii` when you need terminal-safe, sync, plain-text output.
