# DESIGN.md - Vercel Style

> 黑白精准，极简主义，开发者的终极选择

---

## 1. Visual Theme & Atmosphere

**Design Philosophy**: Black and white precision, radical subtraction  
**Mood**: Technical, futuristic, minimal, powerful  
**Density**: Maximum information, minimal chrome  
**Design Language**: Geist design system, geometric minimalism  
**Target Audience**: Developers, technical teams, modern web builders  
**Brand Personality**: Precise, cutting-edge, minimalist, fast

### Design Principles

1. **Radical subtraction** - Remove everything unnecessary
2. **Black and white precision** - Perfect contrast, no noise
3. **Speed is the feature** - Performance in every pixel

### Visual Metaphors

- **Pure black**: Power, sophistication, technical excellence
- **White space**: Clarity, precision, breathing room
- **Geist font**: Modern, technical, developer-centric

---

## 2. Color Palette & Roles

### Primary Colors

| Name | Hex | RGB | Role |
|------|-----|-----|------|
| `vercel-black` | #000000 | rgb(0, 0, 0) | Primary, backgrounds, text |
| `vercel-white` | #FFFFFF | rgb(255, 255, 255) | Background (light mode), text on dark |
| `vercel-gray` | #888888 | rgb(136, 136, 136) | Secondary text |
| `vercel-blue` | #0070F3 | rgb(0, 112, 243) | Accent, links, CTAs |

### Secondary Colors

| Name | Hex | Role |
|------|-----|------|
| `gray-100` | #FAFAFA | Light background |
| `gray-200` | #EAEAEA | Borders, dividers |
| `gray-400` | #666666 | Body text |
| `gray-800` | #333333 | Dark surfaces |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| `success` | #0070F3 | Success states, deployments |
| `warning` | #F5A623 | Warnings |
| `error` | #EE5B5B | Errors, failed deployments |
| `info` | #0070F3 | Informational |

### Accessibility

- **Contrast ratio**: 7.5:1 (AAA) for black/white
- **Color blind safe**: Yes
- **Focus indicators**: Blue outline

---

## 3. Typography Rules

### Font Families

```css
--font-heading: 'Geist Sans', -apple-system, BlinkMacSystemFont, sans-serif;
--font-body: 'Geist Sans', -apple-system, BlinkMacSystemFont, sans-serif;
--font-code: 'Geist Mono', 'Fira Code', monospace;
```

### Type Scale

| Element | Font | Size | Weight | Line Height |
|---------|------|------|--------|-------------|
| `h1` | Geist Sans | 64px | 700 | 1.1 |
| `h2` | Geist Sans | 48px | 700 | 1.2 |
| `h3` | Geist Sans | 32px | 700 | 1.3 |
| `body` | Geist Sans | 16px | 400 | 1.6 |
| `code` | Geist Mono | 14px | 400 | 1.6 |

---

## 4. Component Stylings

### Buttons

```css
.btn-primary {
  background: #000000;
  color: #FFFFFF;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #333333;
  transform: translateY(-1px);
}

.btn-secondary {
  background: transparent;
  color: #000000;
  border: 1px solid #000000;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #000000;
  color: #FFFFFF;
}
```

### Inputs

```css
.input {
  background: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 6px;
  padding: 12px 16px;
  font-size: 16px;
  color: #000000;
  width: 100%;
  transition: all 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: #0070F3;
  box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.1);
}
```

### Cards

```css
.card {
  background: #FFFFFF;
  border: 1px solid #EAEAEA;
  border-radius: 8px;
  padding: 24px;
  transition: all 0.2s ease;
}

.card:hover {
  border-color: #000000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
```

---

## 5. Layout Principles

### Spacing Scale

| Name | Value | Usage |
|------|-------|-------|
| `xs` | 4px | Tight spacing |
| `sm` | 8px | Small gaps |
| `md` | 16px | Default spacing |
| `lg` | 24px | Section spacing |
| `xl` | 32px | Large spacing |

### Grid System

- **Columns**: 12
- **Gutter**: 24px
- **Max width**: 1200px

---

## 6. Depth & Elevation

### Shadow System

```css
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
--shadow-md: 0 4px 12px rgba(0, 0, 0, 0.12);
--shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.16);
```

---

## 7. Do's and Don'ts

### ✅ Do

- Use black and white primarily
- Maintain perfect contrast
- Keep components minimal
- Use Geist font family
- Implement smooth transitions

### ❌ Don't

- Use unnecessary colors
- Add decorative elements
- Use heavy shadows
- Mix design languages
- Sacrifice performance for aesthetics

---

## 8. Responsive Behavior

### Breakpoints

| Name | Min Width | Max Width |
|------|-----------|-----------|
| `mobile` | 0px | 639px |
| `tablet` | 640px | 1023px |
| `desktop` | 1024px | ∞ |

---

## 9. Agent Prompt Guide

### Quick Reference

```css
--color-primary: #000000;
--color-background: #FFFFFF;
--color-accent: #0070F3;
--font-body: 'Geist Sans';
--border-radius: 6px;
```

### Common Prompts

**创建页面**:
```
创建一个 [页面名称] 页面，使用 Vercel 设计风格：
- 黑白精准配色
- Geist Sans 字体
- 极简主义布局
- 圆角 6px
```

---

**Vercel Design System v2.0.0**  
**Last Updated**: 2026-04-09
