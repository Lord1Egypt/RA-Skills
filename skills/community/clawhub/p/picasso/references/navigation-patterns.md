# Navigation Patterns Reference

## Table of Contents
1. Breadcrumb Systems
2. Sidebar and Drawer Navigation
3. Tab Navigation vs Button Groups
4. Mobile Bottom Bar vs Hamburger
5. Sticky Headers
6. Mega Menus
7. Skip Links
8. Common Mistakes

---

## 1. Breadcrumb Systems

```html
<nav aria-label="Breadcrumb">
  <ol class="flex items-center gap-1.5 text-sm">
    <li><a href="/" class="text-muted hover:text-primary">Home</a></li>
    <li aria-hidden="true" class="text-muted">/</li>
    <li><a href="/products" class="text-muted hover:text-primary">Products</a></li>
    <li aria-hidden="true" class="text-muted">/</li>
    <li><span aria-current="page" class="text-primary font-medium">Widget Pro</span></li>
  </ol>
</nav>
```

Rules:
- Use `<nav aria-label="Breadcrumb">` with `<ol>` (ordered list).
- Mark current page with `aria-current="page"`. Don't make it a link.
- Separator (`/` or `>`) gets `aria-hidden="true"`.
- Show 3-5 levels max. Truncate middle levels with `...` on mobile.

---

## 2. Sidebar and Drawer Navigation

Desktop: fixed sidebar, 240-280px width. Mobile: off-canvas drawer with overlay.

```jsx
<aside className={`fixed inset-y-0 left-0 w-[260px] bg-surface-1 border-r border-border
  transform transition-transform duration-200 z-50
  ${mobileOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0`}>
  <nav aria-label="Main navigation">
    {/* nav items */}
  </nav>
</aside>

{/* Mobile overlay */}
{mobileOpen && (
  <div className="fixed inset-0 bg-black/50 z-40 md:hidden"
    onClick={() => setMobileOpen(false)} />
)}
```

Active state: use background tint + accent color text, not bold weight (weight change shifts text width).

```css
.nav-item { padding: 7px 12px; border-radius: 6px; transition: background 100ms; }
.nav-item:hover { background: oklch(1 0 0 / 0.04); }
.nav-item.active { background: oklch(0.65 0.15 230 / 0.1); color: var(--accent); }
```

Section labels: 10px, uppercase, `tracking-[0.12em]`, muted color. Group related items visually.

---

## 3. Tab Navigation vs Button Groups

**Tabs:** switch between views of the SAME content. One is always active. Use `role="tablist"`.

```html
<div role="tablist" aria-label="Account sections">
  <button role="tab" aria-selected="true" aria-controls="panel-profile" id="tab-profile">
    Profile
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-billing" id="tab-billing">
    Billing
  </button>
</div>
<div role="tabpanel" id="panel-profile" aria-labelledby="tab-profile">
  <!-- content -->
</div>
```

**Button groups:** trigger independent ACTIONS. Multiple can be active (toggle group) or none.

```html
<div role="group" aria-label="View options">
  <button aria-pressed="true">Grid</button>
  <button aria-pressed="false">List</button>
</div>
```

Decision: if clicking switches what you see → tabs. If clicking does something → button group.

---

## 4. Mobile Bottom Bar vs Hamburger

Bottom bar outperforms hamburger for engagement. Hamburger hides navigation behind a tap, reducing discoverability.

**When to use bottom bar:**
- 3-5 primary destinations
- Mobile-first app (not marketing site)
- User needs to switch between sections frequently

**When to use hamburger:**
- 6+ navigation items
- Marketing/content site with hierarchical nav
- Secondary navigation (settings, help)

```css
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px; /* 48px min for touch, 56px comfortable */
  padding-bottom: env(safe-area-inset-bottom); /* notch-safe */
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: var(--surface-1);
  border-top: 1px solid var(--border);
  z-index: 50;
}

.bottom-bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  min-width: 64px;
  padding: 4px 12px;
  font-size: 10px;
}
```

---

## 5. Sticky Headers

Keep slim: 48-56px height. Hide on scroll-down, reveal on scroll-up.

```js
let lastScroll = 0;
const header = document.querySelector('header');

window.addEventListener('scroll', () => {
  const current = window.scrollY;
  if (current > lastScroll && current > 80) {
    header.style.transform = 'translateY(-100%)';
  } else {
    header.style.transform = 'translateY(0)';
  }
  lastScroll = current;
}, { passive: true });
```

```css
header {
  position: sticky;
  top: 0;
  height: 56px;
  z-index: 40;
  backdrop-filter: blur(12px);
  background: oklch(var(--bg-l) var(--bg-c) var(--bg-h) / 0.8);
  border-bottom: 1px solid var(--border);
  transition: transform 200ms ease-out;
}
```

---

## 6. Mega Menus

For sites with 20+ navigation items. Two approaches:

**Full-width panel** (preferred): Flyout spans full viewport width. Organized in columns.

```css
.mega-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  padding: 2rem;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  background: var(--surface-1);
  border-top: 1px solid var(--border);
  box-shadow: var(--shadow-lg);
}
```

**Alternatives to mega menus:**
- Search-first navigation (Command+K palette)
- Two-level sidebar (category → items)
- Card-based navigation page

Keep mega menu hover delay at 200-300ms to prevent accidental opens.

---

## 7. Skip Links

First focusable element on the page. Visually hidden until focused.

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<!-- header, nav, etc -->
<main id="main-content" tabindex="-1">
```

```css
.skip-link {
  position: absolute;
  top: -100%;
  left: 1rem;
  z-index: 100;
  padding: 0.5rem 1rem;
  background: var(--accent);
  color: white;
  border-radius: 0 0 8px 8px;
  font-weight: 600;
}
.skip-link:focus {
  top: 0;
}
```

---

## 8. Common Mistakes

- **Hamburger as the only mobile navigation.** Bottom bar is better for primary destinations.
- **Active nav state using `font-weight: bold`.** Shifts text width. Use background/color instead.
- **Sidebar over 300px wide.** Steals too much screen. 240-280px is ideal.
- **Sticky header over 64px.** Takes too much vertical space. 48-56px max.
- **No `aria-current="page"` on breadcrumbs.** Screen readers can't identify current page.
- **Tabs without `role="tablist"`/`role="tab"`.** Not accessible.
- **Mega menu without hover delay.** Opens accidentally when moving mouse across nav.
- **No skip link.** Keyboard users must tab through entire header to reach content.
- **Bottom bar without `safe-area-inset-bottom`.** Content hides behind iPhone notch.
