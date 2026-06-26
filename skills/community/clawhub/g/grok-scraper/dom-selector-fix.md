# DOM Selector Fix Guide

Twitter/X uses CSS-in-JS with build-time hashed class names. These change on every front-end release and will silently break content extraction.

## 1. Detect the problem

Any of the following means the CSS classes have changed:
- `scrape.js` exits with "Reply too short" and `Method: none`
- `output/debug-dom.json` was written — open it and check which selectors show `0` count
- `output/latest.md` is empty or contains garbled UI text instead of the Grok reply

## 2. Inspect current DOM

```bash
cd scripts && npm run inspect
```

This opens a real browser, sends a test prompt, and prints:
- All current `data-testid` and `aria-label` values
- Full ancestor chain from the "Regenerate" button — with each node's class names and text length
- Which CSS classes currently carry `font-weight: 700` (bold)
- A compatibility check: ✅/❌ for each selector currently used by `scrape.js`

Also saves:
- `output/inspect-reply.html` — raw HTML of the reply container
- `output/inspect-dom.json` — structured DOM snapshot

## 3. Identify new class names

From the inspector's "Regenerate button → ancestor chain":

**contentClass**: Find the ancestor where `textLen` matches the reply length and its child `div` contains the reply text. The class on that ancestor (looks like `r-xxxxxxx`) replaces `contentClass`.

**boldClass**: Look at "粗体 class (font-weight:700)" in the inspector output. Pick the class that is NOT a generic layout class (ignore `r-bcqeeo`, `r-1ttztb7`, `r-qvutc0`, `r-poiln3`). That replaces `boldClass`.

If the "Regenerate" button depth changed from 6 levels: find the new depth from the ancestor chain and update the `for` loop in `extractReplyHTML()`.

## 4. Update `SELECTORS` in `scripts/scrape.js`

The `SELECTORS` constant is at the very top of `scrape.js`:

```js
const SELECTORS = {
  contentClass: 'r-16lk18l',   // ← update if changed
  boldClass: 'r-b88u0q',       // ← update if changed
  regenerateBtn: '[aria-label="重新生成"]',        // stable
  primaryColumn: '[data-testid="primaryColumn"]', // stable
  grokContainer: '[aria-label="Grok"]',           // stable
};
```

Only `contentClass` and `boldClass` typically break.

## 5. Verify

```bash
cd scripts && npm run scrape -- "用标题和列表格式介绍 Python 的3个优点"
```

Check `output/latest.md` for correct `##` headings, `**bold**` text, and `- ` list items.

If format is still wrong (headings/bold not rendering), read `output/inspect-reply.html` directly to see the raw HTML, then adjust `grok-heading` or `grok-bold` rules inside `createTurndown()` in `scrape.js`.

## Background

Full design rationale and selector stability table: `learn/dom-selector-fragility.md`
