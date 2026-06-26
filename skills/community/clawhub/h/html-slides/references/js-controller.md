# JS Controller — SlidePresentation Class

Copy this complete `<script>` block at the end of `<body>`. The class is fully brand-agnostic — it reads from DOM elements and CSS properties only.

## Features

| Feature | Trigger | Description |
|---------|---------|-------------|
| Language switch | Click EN or CN segment, or press `L` | Switches `body.lang-cn` ↔ `body.lang-en`, updates sidebar text, persisted to localStorage |
| Sidebar auto-build | On load | Reads `data-title` (CN) and `data-title-en` from slides; `data-group` (CN) and `data-group-en` for group headers |
| Slide visibility | Intersection observer | Adds `.visible` class at 50% threshold (triggers reveal animations) |
| Keyboard nav | Arrow keys, Space, PageUp/Down, Home/End | Smooth scroll between slides |
| Touch/swipe | Vertical swipe >50px | Mobile-friendly navigation |
| Mouse wheel | With 800ms debounce | Scroll one slide at a time |
| Sidebar click | Click any sidebar item | Jump to slide |
| Progress bar | Auto-update | Top bar width = % of slides viewed |
| Page numbers | On load | `N / Total` rendered in each `.page-number` |
| Sidebar toggle | Click hamburger | Toggles `body.sidebar-hidden` |
| Comment panel | Press `C` or click icon | Per-slide notes, localStorage persistence, Copy All, Clear All |
| Zoom | +/- buttons | 70%–150%, step 10%, applies CSS `zoom` to `.slide-content` |
| Inline edit | Press `E` or click pencil | contentEditable on text elements, undo/redo history |
| Present mode | Press `F5` or click play | fullscreen, hides all chrome |

## Complete Script

**IMPORTANT:** Always copy the full ~600-line JS implementation from the most recent source presentation. The stub below shows the class structure.

```javascript
class SlidePresentation {
    constructor() {
        this.slides = document.querySelectorAll('.slide');
        this.currentSlide = 0;
        this.isScrolling = false;
        this.scrollTimeout = null;

        // Language switch (bilingual only — skipped if #langSwitch absent)
        this.setupLanguageToggle();

        this.setupPageNumbers();
        this.buildSidebar();
        this.setupIntersectionObserver();
        this.setupKeyboardNav();
        this.setupTouchNav();
        this.setupProgressBar();
        this.setupWheelNav();
        this.setupSidebarNav();

        this.sidebarVisible = true;
        this.setupSidebarToggle();

        // Comment panel
        this.commentPanel = document.getElementById('commentPanel');
        this.commentTextarea = document.getElementById('commentTextarea');
        this.commentSlideLabel = document.getElementById('commentSlideLabel');
        this.commentSlideName = document.getElementById('commentSlideName');
        this.commentCopyAllBtn = document.getElementById('commentCopyAll');
        this.commentStatus = document.getElementById('commentStatus');
        this.commentsOpen = false;
        this.comments = this.loadComments();
        this.slideNames = Array.from(this.slides).map(
            slide => slide.dataset.title || 'Slide ' + (Array.from(this.slides).indexOf(slide) + 1)
        );
        this.setupCommentPanel();

        // Zoom
        this.zoomLevel = 1.0;
        this.zoomMin = 0.7;
        this.zoomMax = 1.5;
        this.zoomStep = 0.1;
        this.setupZoomControls();

        // Inline edit
        this.editActive = false;
        this.editHistory = [];
        this.editHistoryIndex = -1;
        this.activeEditEl = null;
        this.setupInlineEdit();

        // Present mode
        this.presentMode = false;
        this.setupPresentMode();

        this.slides[0].classList.add('visible');
        this.updateAll();
    }

    /* --- Language switch: body.lang-cn ↔ body.lang-en --- */
    setupLanguageToggle() {
        /* Only active when #langSwitch exists (bilingual presentations).
           - Reads saved preference from localStorage (key: title-slug + '-lang')
           - Default: 'cn' (body starts with class lang-cn)
           - #langEn click → setLanguage('en'); #langCn click → setLanguage('cn')
           - Press L: toggle between 'en' and 'cn'
           - Update .lang-option.active class to highlight active segment
           - Persist choice to localStorage
           - If #langSwitch not found, skip entirely (monolingual mode) */
    }
    setLanguage(lang) {
        /* lang = 'en' | 'cn'
           - Remove both lang-en and lang-cn from body
           - Add body.lang-{lang}
           - Update .lang-option active state (#langEn / #langCn)
           - Update sidebar text: for each sidebar item, read its stored data-title-en / data-title (CN)
             and set textContent based on active language.
             For group headers, read data-group-en / data-group (CN).
           - Save to localStorage */
    }

    /* --- Sidebar auto-build from data-title / data-title-en / data-group / data-group-en --- */
    buildSidebar() {
        /* Reads each slide's data-title (CN) and data-title-en (EN).
           Group headers use data-group (CN) and data-group-en (EN).
           Sidebar items store both titles as data attributes for language switching.
           Renders text based on current body language class. */
    }

    /* --- Intersection observer for .visible class --- */
    setupIntersectionObserver() { /* threshold: 0.5 */ }

    /* --- Keyboard: arrows, space, page up/down, home/end, L for language switch --- */
    setupKeyboardNav() { /* skips TEXTAREA/INPUT/contentEditable targets; L toggles between en/cn */ }

    /* --- Touch: vertical swipe >50px --- */
    setupTouchNav() { /* skips .comment-panel targets */ }

    /* --- Mouse wheel with 800ms debounce --- */
    setupWheelNav() { /* deltaY >30 threshold */ }

    /* --- Sidebar click navigation --- */
    setupSidebarNav() { /* reads data-slide attribute */ }

    /* --- Navigate to slide index --- */
    goToSlide(index) { /* scrollIntoView + updateAll */ }

    /* --- Update progress, sidebar, page number, comments --- */
    updateAll() { /* calls all update methods */ }

    /* --- Progress bar: width = (current+1)/total * 100% --- */
    setupProgressBar() { /* ... */ }
    updateProgressBar() { /* ... */ }

    /* --- Sidebar active state tracking --- */
    updateSidebar() { /* toggles .active class, scrollIntoView */ }

    /* --- Static page numbers in each footer --- */
    setupPageNumbers() { /* renders N / Total into .page-number elements */ }

    /* --- Sidebar toggle: body.sidebar-hidden --- */
    setupSidebarToggle() { /* click handler on #sidebarToggle */ }

    /* --- Comment panel --- */
    toggleComments() { /* body.comments-open */ }
    setupCommentPanel() {
        /* Toggle: click #commentToggle or press C
           Auto-save: debounced 500ms to localStorage
           Copy All: exports as Markdown with slide headers
           Clear All: with confirmation dialog */
    }
    updateCommentPanel() { /* sync textarea to current slide */ }
    loadComments() { /* localStorage key derived from document.title */ }
    saveComments() { /* clean empty entries, persist */ }
    async copyAllComments() { /* clipboard API with fallback */ }
    showStatus(msg) { /* flash message for 2s */ }

    /* --- Zoom: 70%-150%, step 10% --- */
    setupZoomControls() { /* #zoomIn, #zoomOut click handlers */ }
    setZoom(level) { /* CSS zoom on .slide-content, --zoom-level variable */ }
    updateZoomButtons() { /* disable at min/max */ }

    /* --- Inline text editing --- */
    setupInlineEdit() {
        /* Toggle: click #editToggle or press E
           Selectors for editable elements:
           h1, h2, h3, p, li, td (not thead), .eyebrow, .slide-title,
           .kpi-label, .kpi-number, .kpi-change, .body-text
           Each gets .editable class + edit icon overlay
           Double-click or icon click activates contentEditable
           Escape cancels edit */
    }
    toggleEditMode() { /* body.edit-active, optional discard dialog */ }
    startInlineEdit(el) { /* contentEditable=true, .editing class, select all */ }
    stopInlineEdit() { /* save to history if changed */ }
    editUndo() { /* restore oldHTML from history */ }
    editRedo() { /* apply newHTML from history */ }

    /* --- Present mode --- */
    setupPresentMode() { /* F5 or #presentToggle click */ }
    enterPresentMode() { /* body.present-mode, requestFullscreen */ }
    exitPresentMode() { /* triggered by fullscreenchange event */ }
}

document.addEventListener('DOMContentLoaded', () => {
    new SlidePresentation();
});
```

## Implementation Notes

1. **Language switch** localStorage key is `{title-slug}-lang`, stores `'en'` or `'cn'`. Default is `'cn'`. Only initialized when `#langSwitch` element exists (bilingual mode). Two segment buttons: EN and CN. The active segment has `.active` class (highlighted with accent color). When language changes, `setLanguage()` also updates all sidebar item text (reads stored `data-title-en`/`data-title-cn` attributes from sidebar links and `data-group-en`/`data-group-cn` from group headers).
2. **Sidebar logo** is extracted from `document.title` — split on `—`, `–`, or `|` delimiters
3. **Comment localStorage key** is a slug of `document.title` — unique per presentation
4. **Zoom** uses CSS `zoom` property on `.slide-content` elements and updates `--zoom-level` CSS variable (for padding compensation)
5. **Edit history** is per-session only (not persisted)
6. **Present mode** uses Fullscreen API — exit via Escape key or browser controls

**Always copy the full implementation from the most recent source presentation file.** The stub above is for reference only.
