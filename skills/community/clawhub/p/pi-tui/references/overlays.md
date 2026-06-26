# Overlay System

Render components on top of existing content (dialogs/menus/modals).

## Usage

```typescript
// Default centered, max 80 cols
const handle = tui.showOverlay(component);

// Full options
const handle = tui.showOverlay(component, {
  width: 60 | "80%",            // Fixed/percentage width
  minWidth: 40,                 // Minimum width
  maxHeight: 20 | "50%",        // Maximum height (rows/percentage)
  anchor: 'bottom-right',       // Anchor, default center
  offsetX: 2, offsetY: -1,      // Anchor offset
  row: 5 | "25%", col: 10 | "50%", // Absolute/percentage position (overrides anchor)
  margin: 2 | { top, right, bottom, left },
  visible: (w, h) => w >= 100,  // Responsive visibility
  nonCapturing: true,           // Don't auto-focus
});
```

**Anchors**: center, top-left, top-right, bottom-left, bottom-right, top-center, bottom-center, left-center, right-center

**Priority**: minWidth → absolute row/col > percentage > anchor → margin clamp → visible

## OverlayHandle

| Method | Description |
|--------|-------------|
| `hide()` | Permanently remove |
| `setHidden(bool)` | Temporarily hide/show |
| `isHidden()` | Check hidden state |
| `focus()` | Focus and bring to front |
| `unfocus()` | Release focus, fall back to other overlay or previous focus |
| `unfocus({ target: c })` | Release to specific component |
| `unfocus({ target: null })` | Release and clear focus |
| `isFocused()` | Check focus state |

**TUI-level**: `tui.hideOverlay()` hides top overlay, `tui.hasOverlay()` checks for visible overlays