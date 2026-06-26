# marknative

Render Markdown into paginated PNG/SVG without a browser.

## What it does

- Parses Markdown directly
- Lays out text natively
- Paginates output deterministically
- Renders PNG or SVG

## Example

```ts
import { renderMarkdown } from 'marknative'

const pages = await renderMarkdown('# Hello', { format: 'png' })
```

## Notes

- Works best in Node/TypeScript-friendly environments
- Uses `skia-canvas` as the paint backend
