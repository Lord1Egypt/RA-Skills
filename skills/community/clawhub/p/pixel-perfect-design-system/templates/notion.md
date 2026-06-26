# DESIGN.md - Notion Style

> 温暖极简，内容至上，舒适的生产力工具

---

## 1. Visual Theme & Atmosphere

**Design Philosophy**: Warm minimalism, content-first, productivity-focused  
**Mood**: Friendly, productive, calm, approachable  
**Density**: Comfortable, breathing room, document-centric  
**Design Language**: Editorial, warm neutrals, paper-like aesthetic  
**Target Audience**: Knowledge workers, teams, content creators  
**Brand Personality**: Friendly, simple, powerful, human

### Design Principles

1. **Content over chrome** - UI should disappear, content shines
2. **Warmth through simplicity** - Friendly, not sterile
3. **Flexibility through blocks** - Modular, customizable

### Visual Metaphors

- **Warm paper tones**: Comfortable reading, friendly workspace
- **Serif headings**: Editorial quality, trust, credibility
- **Subtle borders**: Gentle structure, not harsh lines

---

## 2. Color Palette & Roles

### Primary Colors

| Name | Hex | RGB | Role |
|------|-----|-----|------|
| `notion-black` | #191919 | rgb(25, 25, 25) | Primary text, headings |
| `notion-gray` | #787774 | rgb(120, 119, 116) | Secondary text, descriptions |
| `notion-bg` | #FFFFFF | rgb(255, 255, 255) | Background |
| `notion-surface` | #F7F6F3 | rgb(247, 246, 243) | Card backgrounds, hover states |

### Secondary Colors

| Name | Hex | Role |
|------|-----|------|
| `gray-100` | #E9E9E7 | Borders, dividers |
| `gray-200` | #D3D1CB | Disabled states |
| `gray-300` | #9B9A97 | Muted text, placeholders |
| `gray-400` | #6B6B6B | Body text on light backgrounds |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| `success` | #0F7B6C | Success states, checkmarks |
| `warning` | #D9730D | Warnings, cautions |
| `error` | #E03E3E | Errors, destructive actions |
| `info` | #2383E2 | Informational, links |

### Notion Color System

| Color Name | Hex | Usage |
|-----------|-----|-------|
| `default` | #37352F | Default text |
| `gray` | #787774 | Gray text/blocks |
| `brown` | #9F6F4C | Brown text/blocks |
| `orange` | #D9730D | Orange text/blocks |
| `yellow` | #CB912F | Yellow text/blocks |
| `green` | #448361 | Green text/blocks |
| `blue` | #337EA9 | Blue text/blocks |
| `purple` | #9065B0 | Purple text/blocks |
| `pink` | #C14C8A | Pink text/blocks |
| `red` | #D44C47 | Red text/blocks |

### Accessibility

- **Contrast ratio**: 4.5:1 (AA) for text
- **Color blind safe**: Yes
- **Focus indicators**: Subtle blue outline

---

## 3. Typography Rules

### Font Families

```css
--font-heading: 'Lyon Text', Georgia, serif;
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-code: 'iawriter-mono', 'Menlo', monospace;
```

### Type Scale

| Element | Font | Size | Weight | Line Height | Letter Spacing |
|---------|------|------|--------|-------------|----------------|
| `h1` | Lyon Text | 40px | 600 | 1.2 | 0 |
| `h2` | Lyon Text | 30px | 600 | 1.3 | 0 |
| `h3` | Lyon Text | 24px | 600 | 1.4 | 0 |
| `h4` | Inter | 20px | 600 | 1.4 | 0 |
| `body-large` | Inter | 16px | 400 | 1.6 | 0 |
| `body` | Inter | 15px | 400 | 1.6 | 0 |
| `body-small` | Inter | 14px | 400 | 1.5 | 0 |
| `caption` | Inter | 12px | 400 | 1.4 | 0 |
| `code` | iawriter-mono | 14px | 400 | 1.6 | 0 |

### Typography Usage

#### Headings
- **H1**: Page titles, document headers
- **H2**: Section titles, major divisions
- **H3**: Subsection titles, card headers
- **H4**: Small headings, callouts

#### Body Text
- **Large**: Feature descriptions, important content
- **Regular**: Paragraphs, lists, general content
- **Small**: Secondary descriptions, metadata
- **Caption**: Timestamps, footnotes, labels

### Special Typography

```css
/* Code blocks */
code {
  font-family: var(--font-code);
  font-size: 14px;
  background: rgba(135, 131, 120, 0.15);
  padding: 2px 6px;
  border-radius: 4px;
  color: #EB5757;
}

/* Block quote */
.blockquote {
  border-left: 3px solid #191919;
  padding-left: 16px;
  color: #787774;
  font-style: italic;
}

/* Callout */
.callout {
  background: #F7F6F3;
  padding: 16px;
  border-radius: 4px;
  display: flex;
  gap: 8px;
}
```

---

## 4. Component Stylings

### Buttons

#### Primary Button

```css
.btn-primary {
  /* Base styles */
  background: #191919;
  color: #FFFFFF;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 500;
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

/* Hover state */
.btn-primary:hover {
  background: #000000;
}

/* Active state */
.btn-primary:active {
  transform: scale(0.98);
}

/* Focus state */
.btn-primary:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(35, 131, 226, 0.5);
}

/* Disabled state */
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

#### Secondary Button

```css
.btn-secondary {
  background: transparent;
  color: #191919;
  border: 1px solid #E9E9E7;
  padding: 7px 15px;
  border-radius: 4px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-secondary:hover {
  background: #F7F6F3;
  border-color: #D3D1CB;
}
```

#### Ghost Button

```css
.btn-ghost {
  background: transparent;
  color: #787774;
  padding: 8px 12px;
  border-radius: 4px;
  font-weight: 500;
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-ghost:hover {
  background: #F7F6F3;
  color: #191919;
}
```

### Inputs

#### Text Input

```css
.input {
  /* Base styles */
  background: #FFFFFF;
  border: 1px solid #E9E9E7;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 15px;
  color: #191919;
  width: 100%;
  transition: all 0.15s ease;
  font-family: var(--font-body);
}

/* Placeholder */
.input::placeholder {
  color: #9B9A97;
}

/* Focus state */
.input:focus {
  outline: none;
  border-color: #2383E2;
  box-shadow: 0 0 0 2px rgba(35, 131, 226, 0.2);
}

/* Error state */
.input.error {
  border-color: #E03E3E;
}

/* Disabled state */
.input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #F7F6F3;
}
```

### Cards

#### Default Card

```css
.card {
  background: #FFFFFF;
  border: 1px solid #E9E9E7;
  border-radius: 6px;
  padding: 16px;
  transition: all 0.15s ease;
}

.card:hover {
  background: #F7F6F3;
}
```

#### Block Card

```css
.block-card {
  background: #FFFFFF;
  border: 1px solid #E9E9E7;
  border-radius: 4px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.block-card:hover {
  background: #F7F6F3;
  border-color: #D3D1CB;
}

.block-card.selected {
  background: rgba(35, 131, 226, 0.1);
  border-color: #2383E2;
}
```

### Navigation

#### Sidebar

```css
.sidebar {
  background: #F7F6F3;
  width: 240px;
  height: 100vh;
  padding: 12px;
  border-right: 1px solid #E9E9E7;
}

.nav-item {
  padding: 4px 8px;
  border-radius: 4px;
  color: #787774;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.nav-item:hover {
  background: rgba(55, 53, 47, 0.08);
  color: #191919;
}

.nav-item.active {
  background: rgba(55, 53, 47, 0.08);
  color: #191919;
  font-weight: 500;
}
```

---

## 5. Layout Principles

### Spacing Scale

| Name | Value | Usage |
|------|-------|-------|
| `xs` | 4px | Tight spacing, icon gaps |
| `sm` | 8px | Small gaps, inline spacing |
| `md` | 12px | Default spacing, list items |
| `lg` | 16px | Card padding, block spacing |
| `xl` | 24px | Section padding |
| `2xl` | 32px | Page sections |
| `3xl` | 48px | Major sections |

### Grid System

- **Columns**: Flexible, content-driven
- **Gutter**: 16px
- **Max width**: 900px (content area)
- **Container padding**: 96px (sidebar width: 240px)

### Breakpoints

```css
--breakpoint-sm: 640px;   /* Mobile */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Large desktop */
```

### Layout Patterns

- **Sidebar + Content**: Fixed sidebar, flexible content
- **Editor**: Full-height editor area
- **Kanban**: Horizontal scrolling columns
- **Table**: Full-width data tables
- **Gallery**: Grid of cover images

### Whitespace Philosophy

- **Comfortable**: Not too tight, not too loose
- **Content-driven**: Whitespace follows content
- **Consistent**: Use spacing scale
- **Breathing room**: Each block needs space

---

## 6. Depth & Elevation

### Shadow System

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.08);
--shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.12);
--shadow-xl: 0 16px 32px rgba(0, 0, 0, 0.16);
```

### Z-Index Scale

| Name | Value | Usage |
|------|-------|-------|
| `base` | 0 | Default layer |
| `dropdown` | 10 | Dropdowns, menus |
| `sticky` | 20 | Sticky headers |
| `modal` | 30 | Modal dialogs |
| `popover` | 40 | Popovers, tooltips |
| `toast` | 50 | Toast notifications |

### Elevation Principles

- **Minimal shadows**: Notion uses subtle elevation
- **Border-focused**: Use borders over shadows
- **Flat design**: Mostly flat with subtle depth
- **Hover feedback**: Light background changes

---

## 7. Do's and Don'ts

### ✅ Do

- Use warm, friendly colors
- Keep UI minimal and content-focused
- Use serif fonts for headings
- Maintain comfortable spacing
- Use subtle borders and shadows
- Keep components simple and functional
- Test accessibility for all text
- Prioritize readability
- Use emoji and icons naturally
- Keep interactions subtle

### ❌ Don't

- Use harsh colors or heavy shadows
- Overcrowd interfaces
- Use sharp corners (use subtle rounding)
- Overuse animations
- Mix design languages
- Sacrifice usability for aesthetics
- Use low-contrast text
- Skip hover states
- Add unnecessary decoration
- Complicate simple interfaces

### Common Mistakes

1. **Too much chrome**: UI should be minimal
2. **Wrong font pairing**: Use serif + sans-serif correctly
3. **Insufficient whitespace**: Content needs breathing room
4. **Harsh shadows**: Use subtle elevation only
5. **Missing hover states**: All interactive elements need feedback

---

## 8. Responsive Behavior

### Breakpoints

| Name | Min Width | Max Width | Target Devices |
|------|-----------|-----------|----------------|
| `mobile` | 0px | 639px | Mobile phones |
| `tablet` | 640px | 1023px | Tablets |
| `desktop` | 1024px | ∞ | Desktops |

### Touch Targets

- **Minimum size**: 44px × 44px
- **Spacing between**: 8px minimum

### Responsive Patterns

#### Sidebar

```css
/* Desktop: Show sidebar */
@media (min-width: 1024px) {
  .sidebar { display: block; }
}

/* Mobile: Hide sidebar */
@media (max-width: 1023px) {
  .sidebar { display: none; }
}
```

### Collapsing Strategy

- **Hide sidebar** on mobile
- **Simplify navigation**
- **Full-width content**
- **Reduce padding** on smaller screens

---

## 9. Agent Prompt Guide

### Quick Reference

```css
/* Colors */
--color-text: #191919;
--color-secondary: #787774;
--color-background: #FFFFFF;
--color-surface: #F7F6F3;
--color-border: #E9E9E7;

/* Fonts */
--font-heading: 'Lyon Text', serif;
--font-body: 'Inter', sans-serif;
--font-code: 'iawriter-mono', monospace;

/* Spacing */
--spacing-base: 4px;
--border-radius: 4px;
```

### Common Prompts

**创建页面**:
```
创建一个 [页面名称] 页面，使用 Notion 设计风格：
- 白色背景 #FFFFFF
- 深色文本 #191919
- Lyon Text 衬线字体标题，Inter 无衬线正文
- 小圆角（4px）
- 温暖极简，内容至上
```

**创建组件**:
```
创建一个 [组件名称] 组件，遵循 Notion 设计规范：
- 背景: #FFFFFF
- 边框: 1px solid #E9E9E7
- 圆角: 4px
- 悬停: background 变为 #F7F6F3
- 过渡: all 0.15s ease
```

### Code Templates

#### React Component

```tsx
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
}

export function Button({ 
  children, 
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick 
}: ButtonProps) {
  return (
    <button 
      className={`${styles.btn} ${styles[variant]} ${styles[size]}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

#### CSS Module

```css
.btn {
  border-radius: 4px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.15s ease;
  border: none;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn.md {
  padding: 8px 16px;
}

.btn.primary {
  background: var(--color-text);
  color: white;
}

.btn.primary:hover:not(:disabled) {
  background: #000000;
}

.btn.secondary {
  background: transparent;
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.btn.secondary:hover:not(:disabled) {
  background: var(--color-surface);
}
```

### AI Agent Instructions

When generating UI code based on this DESIGN.md:

1. **Always use CSS custom properties** from the quick reference
2. **Use serif fonts for headings** - Lyon Text
3. **Maintain warm, friendly colors** - Notion's signature warmth
4. **Keep UI minimal** - Content over chrome
5. **Implement all states** - hover, active, disabled, focus
6. **Test responsiveness** - check all breakpoints
7. **Ensure accessibility** - contrast ratios, touch targets
8. **Use subtle interactions** - 0.15s ease transitions
9. **Keep borders subtle** - Notion uses gentle borders
10. **Prioritize readability** - Comfortable spacing

### Component Generation Checklist

Before generating a component, verify:

- [ ] Uses defined color tokens
- [ ] Follows typography scale
- [ ] Implements all interaction states
- [ ] Responsive across breakpoints
- [ ] Accessible (contrast, touch targets)
- [ ] Minimal and functional
- [ ] Consistent with design language
- [ ] Proper transitions
- [ ] Subtle borders
- [ ] Warm, friendly feel

---

**Notion Design System v2.0.0**  
**Last Updated**: 2026-04-09  
**License**: MIT
