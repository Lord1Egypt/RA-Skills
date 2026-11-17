# Multi-Screen Wireframe User Guide

**Language:** [中文](使用说明.md) | [English](user-guide.md)

For product, design, and review users who open a prototype. Double-click `index.html` in the deliverable directory—no install, build, or network required.

To try it yourself, open the demos in this repo:

- Desktop: `demo/api-client/index.html`
- Mobile: `demo/travel-app/index.html`

---

## How this differs from traditional prototyping tools

Tools like Axure, Figma prototypes, or MockingBot maintain an **element tree** on the canvas: content, style, position, and hierarchy are edited in the tool and update immediately. That is structured UI editing.

This tool works differently. Pages are AI-generated **runnable business source** (`src/screens/*.js` and related files). What you see in the browser is the compiled/runtime result. You cannot reverse the on-screen look into the right source change—the same region may map to a template, state, a loop node, or a shared component. Clicking to restyle by eye is not enough.

The path this tool provides:

1. In Modify mode, **pin the exact DOM nodes** to change (including breadcrumb parent selection and multi-select binding).
2. Turn the notes into a **Prompt** with stable selectors (id / class / `data-wf-key`).
3. Give the Prompt to AI so it **edits the source**; you refresh `index.html` to verify.

Modify mode does not—and cannot—edit source in the browser. Its job is to lock down *where* and *what* to change so AI edits the right files.

---

## 1. Open a prototype

1. Find the deliverable directory (or a demo above).
2. Double-click `index.html` and open it in a modern browser (Chrome / Edge / Safari).
3. First entry defaults to **Board mode**: all pages laid out on one canvas.

The page loads over `file://` locally; no server is required.

---

## 2. Toolbar overview

Left to right, the top toolbar is roughly:

| Area | Functions |
| --- | --- |
| Mode | **Board** / **Demo** |
| Interaction | **Interactive** / **Locked** |
| Zoom | Zoom out, zoom in, reset |
| Demo-only | Hotspots, entry page, back (demo mode only) |
| Right side | Modify, Annotate, expand/collapse screens, Export, Immersive, Fullscreen, Help |

Hover a button for the full tip; press `?` to open Help.

---

## 3. Board mode

**Purpose:** See every page and the flow links between them at a glance.

**How to use**

1. Click **Board** in the toolbar, or press `Ctrl+1` (macOS) / `Alt+1` (Windows/Linux).
2. Pan the canvas:
   - **Locked**: drag to pan, wheel to zoom; you will not click into pages.
   - **Interactive**: you can click pages; hold `Space` then drag to pan; `Ctrl+wheel` to zoom.
3. Select screens with checkboxes in the left sidebar or screen title bars, then expand/collapse or export as a pack.
4. **Double-click** a screen (or the matching item in the sidebar / bottom index) to enter demo starting on that screen.
5. On a screen card you can **Expand** / **Collapse** (to see long pages fully) or **Export PNG**.

### Left sidebar

The left sidebar is the **page list** for overview, jump, and batch selection:

| Action | Effect |
| --- | --- |
| **Single-click** a row | Pan the canvas to that screen (current screen highlighted) |
| **Double-click** a row | Enter demo starting on that screen |
| Checkbox before a row | Select/deselect for expand, collapse, or pack export |
| Top **Select all** | Select or clear all checkboxes |
| Collapse / expand | Collapse from the sidebar top-right; a thin expand control remains when collapsed |

The sidebar footer shows two tips: how to pan/zoom when locked, and how to drag the canvas when interactive. In immersive mode the sidebar is hidden with the rest of the chrome.

### Bottom canvas index

Below the canvas there is a default **page index** (numbered dots)—draggable and closable. It complements the sidebar: the list shows titles; the index jumps by number:

| Action | Effect |
| --- | --- |
| Click a number | Jump to that screen; current number is highlighted |
| **Double-click** a number | Enter demo starting on that screen |
| Hover a number | Show page title and source path (`src/screens/<id>.js`) |
| Drag the left “Index” handle | Move the whole index anywhere on the canvas |
| Click close on the right | Hide the index |

Re-open it under **Help → Show canvas index**. Visibility is remembered per project in the browser; drag position lasts only for the current session. The index is a framework control: it stays clickable and draggable even when interaction is locked.

---

## 4. Demo mode

**Purpose:** Click through real page flows for review and walkthroughs.

**How to use**

1. Click **Demo**, or press `Ctrl+2` / `Alt+2`. You can also double-click a screen on the board.
2. Use the toolbar **Entry** dropdown to pick the start page; click **Back** to return to the previous screen.
3. Click buttons, links, tabs, and other navigable controls inside the screen to move forward.
4. To see clickable regions, turn on **Hotspots** (or `Ctrl+H` / `Alt+H`); click again to turn off.
5. Use the title bar to temporarily expand the current screen for long pages.
6. **Double-click empty space** to leave demo and return to the board.

Demo only navigates to pages declared in the current page's `links`; undeclared jumps do not happen.

---

## 5. Interaction lock

**Purpose:** Avoid accidentally clicking page content while panning or zooming.

| State | Behavior |
| --- | --- |
| **Locked** | Pages are not clickable; drag to pan, wheel to zoom |
| **Interactive** | Click buttons, forms, tabs, etc.; hold `Space` to pan, `Ctrl`+wheel to zoom |

Toggle: toolbar lock button, or `Ctrl+I` / `Alt+I`.

In Help settings you can enable **Restore interactive on entering demo**: if locked when entering demo, it unlocks automatically; you can still lock again during demo.

---

## 6. Zoom and pan

- Toolbar: zoom out, zoom in, **Reset** (reset zoom).
- Shortcut: `Ctrl+wheel` (when interactive); when locked, wheel also zooms.
- Hold `Space`: temporary canvas pan; release to restore the previous behavior.
- Mac trackpad: enable **Trackpad zoom** in Help and adjust sensitivity.

---

## 7. Modify mode

**Purpose:** Pin page nodes precisely, organize change notes, and generate a Prompt you can copy to AI so it edits `src/`.  
**Does not change business source directly.** Records live only in the current browser session and are lost on refresh or close. Copy the Prompt first if you need to keep them.

### Why this workflow

The UI is code running in the browser, not a draggable design file. Select + Prompt pins “which node” to stable DOM selectors, so verbal notes like “the button on the left” do not send AI to the wrong place.

### How to select nodes

1. Click **Modify**, or press `Ctrl+M` / `Alt+M`.
2. Click the target inside a screen. The first hit is often the innermost child (a line of text, an icon).
3. Use the panel **breadcrumb** to move up to parents: from an inner node to a card, list item, or whole module. Click a breadcrumb level to select that parent.  
   Common case: you want the whole card but hit the title first—move up the breadcrumb to the card root, then add to the list.
4. **Multi-select** (one note bound to multiple targets):
   - Turn on **Multi-select** in the panel, then click nodes one by one; or
   - Hold `Shift` / `Command` / `Ctrl` while clicking to add/remove.
   - Remove a single node from the selected list, or **Clear** all.
5. Pick a change type, write the note, click **Add to change list (N nodes)**.

The same note shows one translucent **yellow number** beside all targets; click the number to float-review it. You can still hold `Space` to pan while modifying.

### Change types and examples

| Type | Use when | Example |
| --- | --- | --- |
| **Suggestion** | Free-form description | “Make this a two-column layout with actions on the right” |
| **Change text** | Copy update | New text: “Submit application” |
| **Reorder** | Move / swap | See “Multi-select reorder” below |
| **Delete node** | Remove a block | Optionally add “also clean up unused code” |

**Multi-select reorder (recommended)**

1. Enable multi-select and click the two elements to swap (use the breadcrumb to reach the right level—e.g. two list-item roots, not the text inside).
2. Set type to **Reorder**.
3. State the goal clearly, e.g. “Swap these two nodes” or “Move A after B”.
4. Add to the list → copy the Prompt to AI.

Multi-select also works for “one note, several places”: select the same kind of copy in header and footer and write one shared requirement.

### Generate a Prompt and hand it to AI

1. Below the list, a **final Prompt** is generated (page id, DOM selectors, source hints).
2. You can edit the text box by hand; **Regenerate** overwrites manual edits.
3. Click **Copy Prompt** and paste it to an AI agent.
4. AI should edit only business `src/`, locating nodes in `src/screens/*.js` templates via the selectors.
5. Refresh `index.html` to verify.

Press `Esc` to close the panel or leave Modify mode.

---

## 8. Annotation mode

**Purpose:** Persistent notes, questions, and design decisions on pages or modules. Markers are **blue numbers**. They do not carry Todo / review status.

**How to use**

1. Click **Annotate**.
2. Choose scope:
   - **Page**: whole-page note; pick the page from the dropdown.
   - **Selected module**: click a module in the screen, then write the note.
3. Enter the note, click **Add and save locally**.
4. Filter the list by “Current page / All”; edit or delete entries.
5. Click a blue marker to read the content.

**Local drafts and sync**

- Annotations first save as an operation log in the current browser; the panel shows a pending-sync count.
- Click **Copy sync Prompt**, give it to AI, and merge changes into `src/annotations.js` idempotently.
- After refresh, annotations travel with the prototype and Git.
- If the browser cannot store drafts, the panel warns you—**Export annotation JSON** immediately.

**Cross-device exchange**

| Action | Effect |
| --- | --- |
| **Export annotation JSON** | Download `<project-id>.wireframe-annotations.json` |
| **Import annotation JSON** | Merge with local drafts; same project id only |
| **Clear local drafts** | Requires confirmation; does not affect built-in prototype annotations |

JSON is for backup and cross-browser exchange. Day-to-day annotation edits do not require exporting every time.

---

## 9. Expand / collapse pages

In board or demo, long or wide pages (e.g. tables with many columns and horizontal scroll) may be clipped by default. Expand to see the full content.

- Single screen: use **Expand** / **Collapse** on that screen.
- Multiple screens: check several screens, then use toolbar **Expand selected** / **Collapse selected**; with nothing checked, the action applies to all screens.

Expanded screens are easier to screenshot, export, and read end-to-end.

---

## 10. Export

| Method | Action |
| --- | --- |
| Single-page PNG | On a board screen, click **Export PNG** |
| Multi-page ZIP | Check the screens you need (default: all), click **Pack download** |

Export runs in the local browser; nothing is uploaded. On failure, an error appears beside the canvas.

---

## 11. Immersive and fullscreen

| Feature | Effect | Shortcut |
| --- | --- | --- |
| **Immersive** | Hides the regular toolbar for a cleaner view; compact controls remain | `Ctrl+3` / `Alt+3` |
| **Browser fullscreen** | System fullscreen for the window | `Ctrl+Shift+F` / `Alt+Shift+F` |

In immersive mode you can expand/collapse the compact toolbar and still open Help and settings. `Esc` exits immersive or closes the current panel.

---

## 12. Help, shortcuts, and settings

Click **Help** in the toolbar, or press `?`.

### Shortcut list

macOS uses `Ctrl`; Windows / Linux use `Alt`.

| Shortcut | Action |
| --- | --- |
| `Ctrl/Alt+1` | Board mode |
| `Ctrl/Alt+2` | Demo mode |
| `Ctrl/Alt+I` | Interactive / Locked |
| `Ctrl/Alt+M` | Modify mode |
| `Ctrl/Alt+3` | Immersive mode |
| `Ctrl/Alt+Shift+F` | Browser fullscreen |
| `Ctrl/Alt+H` | Demo hotspots |
| `Space` (hold) | Temporary canvas pan |
| `Esc` | Close panel or exit mode |
| `?` | Toggle Help |

When focus is in an input, textarea, select, or editable content, ordinary shortcuts do not fire.

### Board settings

| Setting | Description |
| --- | --- |
| **UI language** | Simplified Chinese / Traditional Chinese / English; stored globally on the machine |
| **Show canvas index** | Whether the draggable page index is visible; remembered per project |
| **Show annotation markers by default** | When off, blue markers are hidden during normal browsing; annotation mode still shows them temporarily |
| **Restore interactive on entering demo** | Auto-unlock on entering demo (you can still lock manually during demo) |
| **Trackpad zoom** | On Mac, continuous zoom with two-finger gestures, with sensitivity control |

---

## 13. Editing business source (for people who keep editing)

The deliverable is plain multi-file JavaScript, not a bundled app:

1. Edit only `src/` (pages, annotations, styles, business components).
2. Save, then refresh the browser.
3. Do not change `framework/` to work around page errors.
4. If one screen errors, that screen shows an error card; others keep working.

Component usage: `COMPONENTS.md` in the deliverable. Full editing rules: `EDITING.md`, `AGENTS.md`.

When using AI for revisions: prefer pasting the Modify-mode Prompt or the annotation sync Prompt directly to the agent.

---

## 14. Recommended paths

| Scenario | Suggested path |
| --- | --- |
| Learn the product yourself | Board overview (sidebar / bottom index) → double-click into demo → hotspots on the main path |
| Review meeting | Demo + hotspots; expand long pages first |
| Collect change requests | Modify: breadcrumb to the right node → multi-select (e.g. reorder) → copy Prompt → AI edits source → refresh to verify |
| Capture decisions | Annotate clearly → copy sync Prompt → write into source |
| Share screenshots | Expand long pages → single PNG or checked ZIP pack |
| Continue notes on another machine | Export annotation JSON → import on the other machine |

---

## 15. FAQ

**Canvas will not pan / dragging clicks into the page?**  
Check the interaction lock: when unlocked, hold `Space` to pan and `Ctrl`+wheel to zoom; when locked, drag to pan and wheel to zoom without clicking the page.

**Clicked in demo but nothing navigated?**  
Confirm you are in demo mode, interaction is unlocked, and the control's target is in the current page's flow. Turn on hotspots to verify clickable areas.

**Modify list disappeared after refresh?**  
Expected. Modify data is session-only and never writes to source. Copy the Prompt first, or refresh only after AI has edited the source.

**Why can't I edit on the canvas like Figma / Axure?**  
The UI is AI-generated business code running in the browser, not a structured design file; appearance does not map back to source by eye. Modify mode pins nodes and generates a Prompt for AI to edit `src/`.

**I always hit a tiny child node?**  
Use the panel breadcrumb to move up to a parent, then add to the list.

**Annotations survive refresh, but “pending sync” remains?**  
Local drafts are not yet in `src/annotations.js`. Copy the sync Prompt for AI to merge, then refresh.

**Annotation import failed?**  
JSON must come from the same project id; wrong version or format also fails.

**One screen is red; others still work?**  
That is per-screen error isolation. Fix the matching `src/screens/<id>.js` and refresh.
