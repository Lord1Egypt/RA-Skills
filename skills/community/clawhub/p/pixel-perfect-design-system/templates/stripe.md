# DESIGN.md - Stripe Style

> 渐变丰富，优雅精致，金融科技标杆

---

## 1. Visual Theme & Atmosphere

**Design Philosophy**: Premium, trustworthy, elegant - setting the standard for fintech design  
**Mood**: Sophisticated innovation meets financial security  
**Density**: Generous whitespace, breathing room for premium feel  
**Design Language**: Modern fintech aesthetic with signature purple gradients  
**Target Audience**: Developers, businesses, financial professionals  
**Brand Personality**: Trustworthy, innovative, premium, sophisticated

### Design Principles

1. **Trust through transparency** - Clear, honest communication in design
2. **Elegance in simplicity** - Sophisticated yet easy to understand
3. **Developer-first** - Built for developers, beautiful for everyone

### Visual Metaphors

- **Purple gradients**: Innovation, creativity, premium quality
- **Generous whitespace**: Confidence, clarity, premium positioning
- **Smooth curves**: Fluidity, modernity, approachability

---

## 2. Color Palette & Roles

### Primary Colors

| Name | Hex | RGB | Role |
|------|-----|-----|------|
| `stripe-purple` | #635BFF | rgb(99, 91, 255) | Primary brand color, CTAs, highlights |
| `stripe-dark` | #0A2540 | rgb(10, 37, 64) | Headings, primary text |
| `stripe-light` | #F6F9FC | rgb(246, 249, 252) | Background |
| `stripe-teal` | #00D4FF | rgb(0, 212, 255) | Accent, secondary highlights |

### Secondary Colors

| Name | Hex | Role |
|------|-----|------|
| `gray-900` | #1A1F36 | Primary text on light backgrounds |
| `gray-700` | #424770 | Secondary text |
| `gray-500` | #8898AA | Muted text, descriptions |
| `gray-200` | #E3E8EE | Borders, dividers |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| `success` | #00D4AA | Success states, confirmations |
| `warning` | #F5A623 | Warnings, cautions |
| `error` | #E25D5D | Errors, destructive actions |
| `info` | #635BFF | Informational, primary actions |

### Gradients

```css
/* Primary gradient */
background: linear-gradient(135deg, #635BFF 0%, #7C3AED 100%);

/* Hero gradient */
background: linear-gradient(180deg, #F6F9FC 0%, #FFFFFF 100%);

/* Button gradient */
background: linear-gradient(135deg, #635BFF 0%, #8B5CF6 100%);

/* Card gradient */
background: linear-gradient(135deg, 
  rgba(99, 91, 255, 0.05) 0%, 
  rgba(0, 212, 255, 0.05) 100%);
```

### Accessibility

- **Contrast ratio**: 4.5:1 (AA) for text
- **Color blind safe**: Yes (tested with Coblis)
- **Focus indicators**: Purple outline on all interactive elements

---

## 3. Typography Rules

### Font Families

```css
--font-heading: 'Stripe-Font', -apple-system, BlinkMacSystemFont, sans-serif;
--font-body: 'Stripe-Font', -apple-system, BlinkMacSystemFont, sans-serif;
--font-code: 'Roboto Mono', 'Consolas', monospace;
```

### Type Scale

| Element | Font | Size | Weight | Line Height | Letter Spacing |
|---------|------|------|--------|-------------|----------------|
| `h1` | Stripe-Font | 56px | 300 | 1.1 | -0.02em |
| `h2` | Stripe-Font | 40px | 300 | 1.2 | -0.01em |
| `h3` | Stripe-Font | 28px | 300 | 1.3 | 0 |
| `h4` | Stripe-Font | 20px | 400 | 1.4 | 0 |
| `body-large` | Stripe-Font | 18px | 400 | 1.6 | 0 |
| `body` | Stripe-Font | 16px | 400 | 1.6 | 0 |
| `body-small` | Stripe-Font | 14px | 400 | 1.5 | 0 |
| `caption` | Stripe-Font | 12px | 400 | 1.4 | 0.02em |
| `code` | Roboto Mono | 14px | 400 | 1.6 | 0 |

### Typography Usage

#### Headings
- **H1**: Hero sections, landing pages, major announcements
- **H2**: Section titles, feature headers, page titles
- **H3**: Card titles, subsections, dialog titles
- **H4**: Small headings, form labels, minor sections

#### Body Text
- **Large**: Feature descriptions, important content
- **Regular**: Paragraphs, lists, general content
- **Small**: Secondary descriptions, helper text
- **Caption**: Timestamps, footnotes, labels

### Special Typography

```css
/* Code blocks */
code {
  font-family: var(--font-code);
  font-size: 14px;
  background: #F6F9FC;
  padding: 3px 8px;
  border-radius: 4px;
  color: #635BFF;
}

/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, #635BFF, #00D4FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Light font weight */
.light-text {
  font-weight: 300;
  letter-spacing: -0.01em;
}
```

---

## 4. Component Stylings

### Buttons

#### Primary Button

```css
.btn-primary {
  /* Base styles */
  background: linear-gradient(135deg, #635BFF 0%, #7C3AED 100%);
  color: #FFFFFF;
  padding: 14px 28px;
  border-radius: 24px; /* Pill shape */
  font-weight: 500;
  font-size: 16px;
  letter-spacing: -0.01em;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

/* Hover state */
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(99, 91, 255, 0.3);
}

/* Active state */
.btn-primary:active {
  transform: translateY(0);
}

/* Focus state */
.btn-primary:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(99, 91, 255, 0.3);
}

/* Disabled state */
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
```

#### Secondary Button

```css
.btn-secondary {
  background: #FFFFFF;
  color: #635BFF;
  border: 2px solid #635BFF;
  padding: 12px 26px;
  border-radius: 24px;
  font-weight: 500;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #635BFF;
  color: #FFFFFF;
}
```

#### Ghost Button

```css
.btn-ghost {
  background: transparent;
  color: #635BFF;
  padding: 12px 20px;
  border-radius: 24px;
  font-weight: 500;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-ghost:hover {
  background: rgba(99, 91, 255, 0.1);
}
```

### Inputs

#### Text Input

```css
.input {
  /* Base styles */
  background: #FFFFFF;
  border: 2px solid #E3E8EE;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 16px;
  color: #1A1F36;
  width: 100%;
  transition: all 0.2s ease;
  font-family: var(--font-body);
}

/* Placeholder */
.input::placeholder {
  color: #8898AA;
}

/* Focus state */
.input:focus {
  outline: none;
  border-color: #635BFF;
  box-shadow: 0 0 0 3px rgba(99, 91, 255, 0.1);
}

/* Error state */
.input.error {
  border-color: #E25D5D;
}

/* Success state */
.input.success {
  border-color: #00D4AA;
}

/* Disabled state */
.input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #F6F9FC;
}
```

### Cards

#### Default Card

```css
.card {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E3E8EE;
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}
```

#### Gradient Card

```css
.card-gradient {
  background: linear-gradient(135deg, 
    rgba(99, 91, 255, 0.05) 0%, 
    rgba(0, 212, 255, 0.05) 100%);
  border: 1px solid rgba(99, 91, 255, 0.1);
  border-radius: 16px;
  padding: 32px;
  transition: all 0.2s ease;
}

.card-gradient:hover {
  border-color: rgba(99, 91, 255, 0.2);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(99, 91, 255, 0.15);
}
```

### Navigation

#### Header

```css
.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #E3E8EE;
  padding: 16px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-item {
  color: #1A1F36;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: rgba(99, 91, 255, 0.1);
  color: #635BFF;
}

.nav-item.active {
  color: #635BFF;
}
```

---

## 5. Layout Principles

### Spacing Scale

| Name | Value | Usage |
|------|-------|-------|
| `xs` | 4px | Micro-adjustments, tight spacing |
| `sm` | 8px | Small gaps, inline elements |
| `md` | 16px | Default spacing, component padding |
| `lg` | 24px | Section padding, card padding |
| `xl` | 32px | Large sections, feature areas |
| `2xl` | 48px | Major sections, hero areas |
| `3xl` | 64px | Page sections, significant whitespace |

### Grid System

- **Columns**: 12
- **Gutter**: 24px
- **Max width**: 1280px
- **Container padding**: 48px

### Breakpoints

```css
--breakpoint-sm: 640px;   /* Mobile */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Large desktop */
--breakpoint-2xl: 1536px; /* Extra large */
```

### Layout Patterns

- **Hero**: Full-width hero with gradient background
- **Feature Grid**: 3-column grid for features
- **Split**: Two-column with image and text
- **Pricing**: 3-column pricing cards
- **CTA**: Full-width call-to-action sections

### Whitespace Philosophy

- **Generous**: Premium feel through breathing room
- **Consistent**: Use spacing scale always
- **Purposeful**: Every pixel of whitespace serves clarity
- **Hierarchical**: More whitespace = more importance

---

## 6. Depth & Elevation

### Shadow System

```css
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
--shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
--shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
--shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.16);
--shadow-purple: 0 8px 24px rgba(99, 91, 255, 0.2);
```

### Z-Index Scale

| Name | Value | Usage |
|------|-------|-------|
| `base` | 0 | Default layer |
| `dropdown` | 10 | Dropdown menus |
| `sticky` | 20 | Sticky headers |
| `modal` | 30 | Modal dialogs |
| `popover` | 40 | Popovers, tooltips |
| `toast` | 50 | Toast notifications |

### Elevation Principles

- **Soft shadows**: Gentle elevation, premium feel
- **Purple-tinted**: Purple shadows for branded elements
- **Subtle borders**: Light borders with soft shadows
- **Glassmorphism**: Subtle backdrop blur for overlays

### Gradient Borders

```css
.border-gradient {
  background: linear-gradient(white, white) padding-box,
              linear-gradient(135deg, #635BFF, #00D4FF) border-box;
  border: 2px solid transparent;
}
```

---

## 7. Do's and Don'ts

### ✅ Do

- Use generous whitespace for premium feel
- Implement smooth animations (0.2s ease)
- Use gradient buttons for primary actions
- Test accessibility for all color combinations
- Follow typography hierarchy with light weights
- Keep components reusable and modular
- Use pill-shaped buttons for CTAs
- Add subtle shadows for depth
- Prioritize content over decoration
- Use semantic color names in code

### ❌ Don't

- Use harsh shadows or heavy borders
- Overcrowd interfaces with too many elements
- Use arbitrary spacing values
- Hardcode color hex values in components
- Ignore responsive breakpoints
- Use heavy font weights (stick to 300-500)
- Skip hover and focus states
- Mix design languages inconsistently
- Use low-contrast text combinations
- Sacrifice usability for aesthetics

### Common Mistakes

1. **Insufficient whitespace**: Cramming too much content
2. **Wrong shadows**: Using too dark or too large shadows
3. **Heavy fonts**: Using 600+ weights when 300-400 is specified
4. **Sharp corners**: Using square corners instead of rounded
5. **Missing gradients**: Using solid colors when gradients are needed

---

## 8. Responsive Behavior

### Breakpoints

| Name | Min Width | Max Width | Target Devices |
|------|-----------|-----------|----------------|
| `mobile` | 0px | 639px | Mobile phones |
| `tablet` | 640px | 1023px | Tablets |
| `desktop` | 1024px | 1279px | Laptops |
| `large` | 1280px | ∞ | Desktops, monitors |

### Touch Targets

- **Minimum size**: 44px × 44px (Apple HIG)
- **Recommended**: 48px × 48px (Material Design)
- **Spacing between targets**: 8px minimum

### Responsive Patterns

#### Navigation

```css
/* Desktop: Horizontal nav */
@media (min-width: 1024px) {
  .nav { display: flex; }
  .nav-mobile-toggle { display: none; }
}

/* Mobile: Hamburger menu */
@media (max-width: 1023px) {
  .nav { display: none; }
  .nav-mobile-toggle { display: block; }
}
```

#### Grid

```css
/* Mobile: 1 column */
.grid { grid-template-columns: 1fr; }

/* Tablet: 2 columns */
@media (min-width: 640px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop: 3 columns */
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}
```

### Collapsing Strategy

- **Stack vertically** on mobile
- **Simplify navigation** to hamburger menu
- **Reduce padding/margins** on smaller screens
- **Hide secondary information** on mobile
- **Prioritize primary actions** in mobile view

---

## 9. Agent Prompt Guide

### Quick Reference

```css
/* Colors */
--color-primary: #635BFF;
--color-background: #F6F9FC;
--color-text: #0A2540;
--color-accent: #00D4FF;

/* Fonts */
--font-heading: 'Stripe-Font';
--font-body: 'Stripe-Font';
--font-code: 'Roboto Mono';

/* Spacing */
--spacing-base: 8px;
--border-radius: 8px;
--border-radius-pill: 24px;

/* Shadows */
--shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
--shadow-purple: 0 8px 24px rgba(99, 91, 255, 0.2);
```

### Common Prompts

**创建页面**:
```
创建一个 [页面名称] 页面，使用 Stripe 设计风格：
- 浅色背景 #F6F9FC
- 紫色主色 #635BFF，青色点缀 #00D4FF
- Stripe-Font 字体，300 超细字重
- 药丸形状按钮（border-radius: 24px）
- 大量留白，优雅渐变
```

**创建组件**:
```
创建一个 [组件名称] 组件，遵循 Stripe 设计规范：
- 背景: #FFFFFF
- 边框: 1px solid #E3E8EE
- 圆角: 12px
- 阴影: 0 2px 8px rgba(0, 0, 0, 0.08)
- 悬停: 增强阴影，transform: translateY(-2px)
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
  font-weight: 500;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn.md {
  padding: 14px 28px;
}

.btn.primary {
  background: linear-gradient(135deg, var(--color-primary) 0%, #7C3AED 100%);
  color: white;
  border-radius: 24px;
}

.btn.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(99, 91, 255, 0.3);
}

.btn.secondary {
  background: white;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  border-radius: 24px;
}

.btn.secondary:hover:not(:disabled) {
  background: var(--color-primary);
  color: white;
}
```

### AI Agent Instructions

When generating UI code based on this DESIGN.md:

1. **Always use CSS custom properties** from the quick reference
2. **Use gradient backgrounds** for primary buttons and accents
3. **Maintain generous whitespace** - Stripe is known for premium spacing
4. **Follow typography hierarchy** - use light weights (300-400)
5. **Implement all states** - hover, active, disabled, focus
6. **Test responsiveness** - check all breakpoints
7. **Ensure accessibility** - contrast ratios, touch targets
8. **Use smooth animations** - 0.2s ease transitions
9. **Add subtle shadows** - soft, not harsh
10. **Keep it elegant** - premium, trustworthy feel

### Component Generation Checklist

Before generating a component, verify:

- [ ] Uses defined color tokens
- [ ] Follows typography scale (light weights)
- [ ] Implements all interaction states
- [ ] Responsive across breakpoints
- [ ] Accessible (contrast, touch targets)
- [ ] Premium, elegant feel
- [ ] Consistent with design language
- [ ] Proper gradients where needed
- [ ] Subtle shadows
- [ ] Smooth transitions

---

**Stripe Design System v2.0.0**  
**Last Updated**: 2026-04-09  
**License**: MIT
