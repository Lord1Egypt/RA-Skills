# Internationalization Visual Patterns Reference

## Table of Contents
1. Logical Properties
2. RTL Layout Mirroring
3. Text Expansion by Language
4. CJK Text Rendering
5. Number and Currency Formatting
6. Font Stacks for Multi-Language
7. Icon Mirroring in RTL
8. Common Mistakes

---

## 1. Logical Properties

Replace physical properties with logical ones. This makes RTL support automatic.

| Physical (avoid) | Logical (use) |
|---|---|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `text-align: left` | `text-align: start` |
| `float: left` | `float: inline-start` |
| `border-left` | `border-inline-start` |
| `left: 0` | `inset-inline-start: 0` |

```css
/* Good: works in both LTR and RTL */
.sidebar { margin-inline-end: 2rem; padding-inline-start: 1rem; }

/* Bad: breaks in RTL */
.sidebar { margin-right: 2rem; padding-left: 1rem; }
```

---

## 2. RTL Layout Mirroring

Set `dir="auto"` on user-generated content. Set `dir="rtl"` on the `<html>` element for RTL languages.

```html
<html lang="ar" dir="rtl">
```

Flexbox and Grid automatically reverse in RTL when using logical properties. No extra CSS needed.

```css
/* This works in both directions automatically */
.nav { display: flex; gap: 1rem; }
.card { display: grid; grid-template-columns: auto 1fr; }
```

---

## 3. Text Expansion by Language

English text expands significantly when translated. Design for the longest likely translation.

| Language | Expansion from English |
|---|---|
| German | +30-35% |
| French | +15-20% |
| Finnish | +30-40% |
| Russian | +15-25% |
| Chinese | -30-50% (shorter) |
| Japanese | -20-40% (shorter) |
| Arabic | +20-25% |

Rules:
- Never use fixed-width containers for translatable text.
- Buttons: use `min-width` not `width`. Allow text to wrap or grow.
- Navigation: test with German translations (longest common language).
- Truncate with `text-overflow: ellipsis` as a last resort, never as the design.

```css
/* Good: grows with content */
.btn { min-width: 120px; padding-inline: 1.5rem; white-space: nowrap; }

/* Bad: text overflows in German */
.btn { width: 120px; }
```

---

## 4. CJK Text Rendering

Chinese, Japanese, and Korean text has different line-breaking and spacing rules.

```css
/* Allow CJK text to break at any character */
.cjk-text {
  line-break: auto;
  word-break: keep-all; /* Korean: don't break within words */
  overflow-wrap: break-word;
}

/* CJK doesn't need letter-spacing for readability */
:lang(zh), :lang(ja), :lang(ko) {
  letter-spacing: 0;
}
```

CJK text is denser — reduce line-height slightly:
```css
:lang(zh), :lang(ja) { line-height: 1.7; } /* vs 1.5 for Latin */
```

---

## 5. Number and Currency Formatting

Never hardcode currency symbols or number formats. Use `Intl.NumberFormat`.

```js
// Automatic locale-aware formatting
new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(1234.56)
// → "$1,234.56"

new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(1234.56)
// → "1.234,56 €"

new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' }).format(1234)
// → "￥1,234"
```

For dates: use `Intl.DateTimeFormat`, never manual formatting.

---

## 6. Font Stacks for Multi-Language

Include system fonts per script as fallbacks:

```css
body {
  font-family:
    'Your Custom Font',        /* Latin */
    'Noto Sans SC',            /* Simplified Chinese */
    'Noto Sans JP',            /* Japanese */
    'Noto Sans KR',            /* Korean */
    'Noto Sans Arabic',        /* Arabic */
    system-ui, sans-serif;     /* Fallback */
}
```

Google's Noto family covers every Unicode script. Use it as the universal fallback.

---

## 7. Icon Mirroring in RTL

Icons that imply direction MUST mirror in RTL. Icons that don't imply direction must NOT.

**Mirror in RTL:** arrows, back/forward, reply, undo/redo, text indent, send, search (if it implies reading direction), progress bars.

**Do NOT mirror:** play/pause, checkmarks, plus/minus, clock, globe, user, settings gear, download, external link.

```css
[dir="rtl"] .icon-directional {
  transform: scaleX(-1);
}
```

---

## 8. Common Mistakes

- **Hardcoding `left`/`right` in CSS.** Use logical properties.
- **Fixed-width buttons.** They overflow in German/Finnish. Use `min-width`.
- **Testing only in English.** Design breaks with 35% longer strings.
- **`text-align: left` instead of `text-align: start`.** Breaks RTL.
- **Mirroring ALL icons in RTL.** Only directional icons should flip.
- **Hardcoding date formats.** `01/02/2026` means different dates in US vs UK. Use `Intl.DateTimeFormat`.
- **Not loading CJK fonts.** System fonts for CJK vary wildly. Include Noto Sans.
- **Ignoring `dir="auto"` on user content.** A Hebrew comment in an English page needs auto-detection.
