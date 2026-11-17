# AIFLC CommandBoard

**Version:** 0.3.0
**Extension Code:** AIFLC-CommandBoard

---

## What Is This?

An interactive command palette that surfaces all AI-* family triggers and shortcuts in one searchable, filterable, expandable panel. Click any trigger to copy it — paste into your AI chat prompt.

Supports all AI-* families (PDLC today, more in the future via the Family filter).

---

## Dual-Mode Access

### Browser Mode

Open directly (works on file:// — no server needed):
```
tools/extensions/AIFLC-CommandBoard/ui/index.html
```

### VS Code Extension Mode

Install the extension, then: **AIFLC: Open Command Board**

Clicking a trigger in VS Code mode copies it to clipboard automatically.

---

## Features

- **Family filter** — top-level filter by AI-* family (PDLC now, future families auto-appear)
- **Category filter** — filter by type: Package Activation, Agent Shortcuts, Visual Tools, Utility
- **Search** — type to filter triggers by name, description, or package
- **Expandable cards** — click any card to reveal:
  - Full explanation of what the trigger does
  - All valid usage combinations with arguments
  - Copyable example prompt
- **Click to copy** — click any trigger key or example to copy to clipboard
- **Dark/light theme** — toggle via button
- **Responsive** — works on any screen size
- **Zero dependencies** — no npm, no server, pure HTML/CSS/JS
- **file:// compatible** — data inlined for direct browser access

---

## Updating Triggers

Edit `data/triggers.json` to add, remove, or update triggers. Then update the inline `var TRIGGERS = {...}` in `ui/index.html` to match. No build step needed.

---

## Filter Hierarchy

```
Family:   [ All ] [ PDLC ] [ ... future families ]
Type:     [ All ] [ Package Activation Keys ] [ Agent Shortcuts ] [ Utility Keys ] [ Visual Tools ]
Search:   [ free text — filters across all dimensions ]
```

All filters compose — selecting a family + type + search narrows results across all three dimensions.

---

*Part of [AIFLC](../../../README.md) — the AI-* Family*
