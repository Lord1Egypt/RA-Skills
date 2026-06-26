# Viewport Fitting & Interactive Chrome

All CSS in this file is brand-agnostic — it references only CSS custom properties, so it works with any brand preset.

## Viewport Fitting (MANDATORY)

Copy this entire block into every presentation.

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

html, body { height: 100%; overflow-x: hidden; }
html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }

body {
    background: var(--bg-primary);
    font-family: var(--font-display);
    color: var(--text-primary);
    -webkit-font-smoothing: antialiased;
}

.slide {
    width: 100vw; height: 100vh; height: 100dvh;
    overflow: hidden; scroll-snap-align: start;
    display: flex; flex-direction: column; position: relative;
}

.slide-content {
    flex: 1; display: flex; flex-direction: column;
    justify-content: center; max-height: 100%; overflow: hidden;
    padding: calc(var(--slide-padding) / var(--zoom-level, 1));
    padding-left: calc((var(--sidebar-width) + clamp(1.5rem, 4vw, 4rem)) / var(--zoom-level, 1));
    transition: padding-left var(--panel-transition), padding-right var(--panel-transition);
}

.card, .container, .content-box { max-width: min(90vw, 1000px); max-height: min(80vh, 700px); }
img, .image-container { max-width: 100%; max-height: min(50vh, 400px); object-fit: contain; }
```

## Responsive Breakpoints

```css
@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(0.75rem, 3vw, 2rem);
        --content-gap: clamp(0.4rem, 1.5vw, 1rem);
        --title-size: clamp(1.5rem, 5.4vw, 3rem);
        --h2-size: clamp(1.2rem, 3.6vw, 2.1rem);
    }
}
@media (max-height: 600px) {
    :root {
        --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --title-size: clamp(1.32rem, 4.8vw, 2.4rem);
        --body-size: clamp(0.84rem, 1.44vw, 1.14rem);
    }
    .nav-dots, .keyboard-hint, .decorative { display: none; }
}
@media (max-height: 500px) {
    :root {
        --slide-padding: clamp(0.4rem, 2vw, 1rem);
        --title-size: clamp(1.2rem, 4.2vw, 1.8rem);
    }
}
@media (max-width: 600px) {
    :root { --title-size: clamp(1.5rem, 8.4vw, 3rem); }
    .grid { grid-template-columns: 1fr; }
    .metrics-grid { grid-template-columns: 1fr 1fr; }
    .two-col-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
    :root { --sidebar-width: 0px; --comment-panel-width: 85vw; }
    .sidebar, .sidebar-toggle { display: none; }
    .slide-content { padding-left: calc(var(--slide-padding) / var(--zoom-level, 1)); }
    .chrome-toolbar { right: 0.5rem !important; }
}
@media (max-width: 480px) {
    .metrics-grid { grid-template-columns: 1fr; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }
    html { scroll-behavior: auto; }
}
```

---

## Chrome HTML Templates

### Sidebar Navigation + Toggle + Progress Bar

The sidebar is auto-built by JS from `data-title` and `data-group` attributes on slides.

**Toggle button is flush against the sidebar's right edge** — it moves with the sidebar when expanding/collapsing.

**Progress bar only spans the slide area** (starts at `left: var(--sidebar-width)`, not from the viewport edge).

```html
<nav class="sidebar" id="sidebar" aria-label="Slide navigation">
    <div class="sidebar-header">
        <div class="sidebar-logo" id="sidebarLogo"></div>
    </div>
    <div class="sidebar-divider"></div>
    <div id="sidebarNav"></div>
</nav>

<!-- Toggle sits OUTSIDE the sidebar, flush against its right edge -->
<button class="sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar" title="Toggle sidebar">
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <path d="M3 4h12M3 9h12M3 14h12"/>
    </svg>
</button>

<!-- Progress bar covers ONLY the slide area, NOT the sidebar -->
<div class="progress-bar" id="progressBar"></div>
```

#### Sidebar + Toggle + Progress CSS

```css
/* === SIDEBAR === */
.sidebar {
    position: fixed; left: 0; top: 0; bottom: 0;
    width: var(--sidebar-width);
    background: #fff; z-index: 1000;
    border-right: 1px solid var(--border-subtle);
    display: flex; flex-direction: column;
    transition: transform var(--panel-transition);
    overflow-y: auto;
}
body.sidebar-hidden .sidebar {
    transform: translateX(-100%);
}

/* === SIDEBAR TOGGLE — flush OUTSIDE sidebar right edge === */
.sidebar-toggle {
    position: fixed;
    top: clamp(0.6rem, 1.5vh, 1rem);
    left: calc(var(--sidebar-width) + 4px);
    z-index: 1001;
    width: 32px; height: 32px;
    border: none; border-radius: 6px; cursor: pointer;
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(8px);
    color: var(--text-secondary);
    display: flex; align-items: center; justify-content: center;
    transition: left var(--panel-transition);
}
.sidebar-toggle:hover {
    background: var(--bg-card-hover);
    color: var(--text-primary);
}
/* When sidebar hidden: toggle snaps to left edge of viewport */
body.sidebar-hidden .sidebar-toggle {
    left: 6px;
}
/* In present mode hide the toggle */
body.present-mode .sidebar-toggle { display: none; }

/* === PROGRESS BAR — spans slide area only === */
.progress-bar {
    position: fixed;
    top: 0;
    left: var(--sidebar-width);   /* starts where slides start */
    right: 0;
    height: 3px;
    background: var(--accent);
    transform-origin: left;
    transform: scaleX(0);
    z-index: 1002;
    transition: left var(--panel-transition), transform 0.3s ease;
}
/* When sidebar hidden, progress bar extends full width */
body.sidebar-hidden .progress-bar {
    left: 0;
}
body.present-mode .progress-bar { display: none; }
```

---

### Chrome Toolbar (Horizontal — Top Right)

All chrome controls are grouped in a **single horizontal toolbar**. Order left to right: **Language switch → Present → Zoom → Edit → Comment**.

The language switch is only included in **bilingual presentations**. For monolingual output, omit the `#langSwitch` div and its adjacent divider.

```html
<div class="chrome-toolbar" id="chromeToolbar">
    <!-- 0. Language switch (bilingual only) -->
    <div class="lang-switch" id="langSwitch">
        <button class="lang-option" data-lang="en" id="langEn">EN</button>
        <button class="lang-option active" data-lang="cn" id="langCn">CN</button>
    </div>

    <div class="toolbar-divider"></div>

    <!-- 1. Present -->
    <button class="chrome-btn present-toggle" id="presentToggle" aria-label="Present (F5)" title="Present (F5)">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
            <path d="M4 2l10 6-10 6V2z"/>
        </svg>
    </button>

    <div class="toolbar-divider"></div>

    <!-- 2. Zoom -->
    <div class="zoom-controls" id="zoomControls">
        <button class="zoom-btn" id="zoomOut" aria-label="Zoom out">&minus;</button>
        <span class="zoom-level" id="zoomLevel">100%</span>
        <button class="zoom-btn" id="zoomIn" aria-label="Zoom in">+</button>
    </div>

    <div class="toolbar-divider"></div>

    <!-- 3. Edit + undo/redo -->
    <button class="chrome-btn edit-toggle" id="editToggle" aria-label="Toggle text editing (E)" title="Edit text (E)">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M11.5 1.5l3 3L5 14H2v-3L11.5 1.5z"/>
        </svg>
    </button>
    <div class="edit-history" id="editHistory">
        <button class="edit-history-btn" id="editUndo" aria-label="Undo" disabled>&#8630;</button>
        <button class="edit-history-btn" id="editRedo" aria-label="Redo" disabled>&#8631;</button>
    </div>

    <div class="toolbar-divider"></div>

    <!-- 4. Comment -->
    <button class="chrome-btn comment-toggle" id="commentToggle" aria-label="Toggle comments" title="Toggle comments (C)">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M2 3h14v10H6l-4 3V3z"/>
        </svg>
    </button>
</div>
```

#### Chrome Toolbar CSS

```css
/* === HORIZONTAL TOOLBAR — top right === */
.chrome-toolbar {
    position: fixed;
    top: clamp(0.6rem, 1.5vh, 1rem);
    right: clamp(0.5rem, 1.5vw, 1rem);
    z-index: 1001;
    display: flex;
    align-items: center;
    gap: 4px;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(8px);
    border-radius: 8px;
    padding: 4px 6px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    transition: right var(--panel-transition);
}

/* When comment panel is open, shift toolbar left */
body.comments-open .chrome-toolbar {
    right: calc(var(--comment-panel-width) + clamp(0.5rem, 1.5vw, 1rem));
}

body.present-mode .chrome-toolbar { display: none; }

.toolbar-divider {
    width: 1px; height: 18px;
    background: var(--border-subtle);
    flex-shrink: 0;
}

/* Chrome buttons (present, edit, comment) */
.chrome-btn {
    width: 32px; height: 32px;
    border: none; border-radius: 6px; cursor: pointer;
    background: transparent;
    color: var(--text-secondary);
    display: flex; align-items: center; justify-content: center;
    transition: background 0.2s, color 0.2s;
}
.chrome-btn:hover {
    background: var(--bg-card-hover);
    color: var(--text-primary);
}
.chrome-btn.active {
    background: var(--accent);
    color: #fff;
}

/* Zoom controls (inline in toolbar) */
.zoom-controls {
    display: flex; align-items: center; gap: 2px;
}
.zoom-btn {
    width: 28px; height: 28px;
    border: none; border-radius: 4px; cursor: pointer;
    background: transparent;
    font-size: 16px; font-weight: 600;
    color: var(--text-secondary);
    display: flex; align-items: center; justify-content: center;
    transition: background 0.2s, color 0.2s;
}
.zoom-btn:hover {
    background: var(--bg-card-hover);
    color: var(--text-primary);
}
.zoom-level {
    font-size: var(--small-size);
    font-family: var(--font-mono);
    color: var(--text-secondary);
    min-width: 3.2em; text-align: center;
    user-select: none;
}

/* Edit history (visible only when edit mode active) */
.edit-history {
    display: none;
    align-items: center; gap: 2px;
}
body.edit-active .edit-history { display: flex; }

.edit-history-btn {
    width: 26px; height: 26px;
    border: none; border-radius: 4px; cursor: pointer;
    background: transparent;
    font-size: 14px; color: var(--text-secondary);
    display: flex; align-items: center; justify-content: center;
}
.edit-history-btn:hover:not(:disabled) {
    background: var(--bg-card-hover);
    color: var(--text-primary);
}
.edit-history-btn:disabled { opacity: 0.3; cursor: default; }

/* === LANGUAGE SWITCH (bilingual presentations only) === */
.lang-switch {
    display: flex;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--border-subtle, #e0e0e0);
    height: 28px;
}
.lang-option {
    padding: 0 10px;
    height: 100%;
    border: none;
    background: transparent;
    font-size: 12px; font-weight: 600;
    font-family: var(--font-mono);
    cursor: pointer;
    color: var(--text-secondary);
    transition: background 0.2s, color 0.2s;
    line-height: 28px;
}
.lang-option.active {
    background: var(--accent);
    color: #fff;
}
.lang-option:hover:not(.active) {
    background: var(--bg-card-hover, #f5f5f5);
}

/* === BILINGUAL CONTENT SWITCHING === */
body.lang-en .lang-cn { display: none; }
body.lang-cn .lang-en { display: none; }
```

---

### Comment Panel

The comment panel HTML remains separate from the toolbar. The toolbar's comment button toggles it.

```html
<aside class="comment-panel" id="commentPanel" aria-label="Slide comments">
    <div class="comment-panel-header">
        <div class="comment-panel-title">
            <span class="comment-slide-label" id="commentSlideLabel"></span>
            <span class="comment-slide-name" id="commentSlideName"></span>
        </div>
        <div style="display: flex; gap: 0.3rem; flex-shrink: 0;">
            <button class="comment-copy-all comment-clear-all" id="commentClearAll" title="Clear all comments">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 4h10M5 4V2h4v2M3 4v8a1 1 0 001 1h6a1 1 0 001-1V4"/>
                </svg>
                Clear All
            </button>
            <button class="comment-copy-all" id="commentCopyAll" title="Copy all comments to clipboard">
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="4" y="4" width="9" height="9" rx="1"/>
                    <path d="M1 10V2a1 1 0 011-1h8"/>
                </svg>
                Copy All
            </button>
        </div>
    </div>
    <textarea class="comment-textarea" id="commentTextarea" placeholder="Add notes for this slide..."></textarea>
    <div class="comment-status" id="commentStatus"></div>
</aside>
```

---

## Chrome CSS Summary

All chrome CSS uses only CSS custom properties — brand-agnostic by design. Key structural rules:

| Element | Positioning | Key CSS |
|---------|-------------|---------|
| **Sidebar** | Fixed left, `width: var(--sidebar-width)` | `z-index: 1000`, white bg, transition via `transform` |
| **Sidebar toggle** | Fixed, `left: calc(var(--sidebar-width) + 4px)` | Sits just outside sidebar right edge, follows sidebar |
| **Progress bar** | Fixed top, `left: var(--sidebar-width)` to `right: 0` | Only covers slide area, never overlaps sidebar |
| **Chrome toolbar** | Fixed top-right, horizontal flex | Contains: lang → present → zoom → edit → comment |
| **Comment panel** | Fixed right, slides out from off-screen | `z-index: 1000`, pushes toolbar left when open |

### Body State Classes

| Class | Effect |
|-------|--------|
| `body.lang-cn` | Shows `.lang-cn` spans, hides `.lang-en` spans (default for bilingual) |
| `body.lang-en` | Shows `.lang-en` spans, hides `.lang-cn` spans |
| `body.sidebar-hidden` | Sidebar translateX(-100%), toggle snaps to left:6px, progress bar left:0 |
| `body.comments-open` | Comment panel visible, toolbar shifts right by panel width |
| `body.edit-active` | Edit history buttons appear in toolbar, contentEditable enabled |
| `body.present-mode` | Hides ALL chrome (sidebar, toggle, toolbar, progress bar, comment panel) |
