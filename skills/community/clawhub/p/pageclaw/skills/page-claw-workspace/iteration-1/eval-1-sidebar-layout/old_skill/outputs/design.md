# Design Document — Ying Xiao Academic Homepage

**Page story:** `skills/pageclaw-test/fixtures/page-story-test.md`
**Generated:** 2026-03-15
**Name slug:** `ying-xiao`

---

## User Choices

- **Q1 Visual direction:** Cool & minimal
- **Q2 Aesthetic style:** Structured Sidebar Scholar (see below)
- **Reference design:** Skip

---

## Design Context

### Users

- Academic peers, conference program committees, potential postdoc supervisors/hiring managers
- Visiting collaborators or prospective PhD students
- General scientific audience interested in AI fairness, SE4AI, AI4Healthcare

### Brand Personality

- Rigorous, trustworthy, quietly confident
- Research-forward — publications and news carry more weight than personal narrative
- Internationally situated (UK / China academic networks)
- Currently job-seeking: the job-market signal must be visible but not desperate

### Aesthetic Direction

**Cool & minimal** — clean white space, restrained palette (cool grays + one accent), precise typography, no decoration for its own sake. Every element earns its place through content value, not visual flair.

**Q2 chosen style: Structured Sidebar Scholar**

> A fixed left sidebar holds identity anchors (name, avatar, links, status badge) while the main content column scrolls freely through sections. Scholarly, organized, and scannable.
> `CSS signature: display: grid; grid-template-columns: 260px 1fr; position: sticky; top: 0; height: 100vh`

This style was chosen because it maps directly to the page-story's structure: a self-contained identity block (avatar, name, links) plus scrollable content sections (News, Publications, Preprints, Invited Talks). The sidebar anchors identity while the right column presents research output.

### Design Principles

1. **Content hierarchy first** — Publications and News sections are the primary value; they must be visually prominent.
2. **Typographic precision** — Size and weight alone carry hierarchy; no decorative dividers beyond subtle rules.
3. **Cool restraint** — Color used only for accent (links, badges, status indicator). No warm tones.
4. **Structural clarity** — The sidebar/main split must be immediately legible at first glance.
5. **Accessibility** — WCAG AA contrast throughout; focus states visible for keyboard navigation.

---

## Design System

### Palette

| Role | Value | Notes |
|------|-------|-------|
| Background | `#ffffff` | Pure white — maximum contrast |
| Surface | `#f8f9fa` | Sidebar background, subtle separation |
| Border | `#e5e7eb` | Dividers, sidebar border |
| Text primary | `#111827` | Body text, headings |
| Text secondary | `#6b7280` | Meta text, dates, secondary labels |
| Accent | `#2563eb` | Links, active states, status badge |
| Accent hover | `#1d4ed8` | Link hover |
| Status badge bg | `#eff6ff` | Light blue tint for job-market badge |
| Status badge text | `#1e40af` | Matches accent family |

### Typography

| Element | Font | Weight | Size | Line-height |
|---------|------|--------|------|-------------|
| Name / H1 | `Inter`, sans-serif | 700 | `1.5rem` | 1.2 |
| Section headings H2 | `Inter`, sans-serif | 600 | `1rem` | 1.3 |
| Body / publication entries | `Inter`, sans-serif | 400 | `0.9375rem` | 1.65 |
| Meta / secondary | `Inter`, sans-serif | 400 | `0.8125rem` | 1.5 |
| Links | Inherit | 500 | Inherit | — |

Import: `https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap`

### Spatial Rhythm

Base unit: `8px`. All spacing is multiples of this unit.

- Sidebar padding: `32px 24px`
- Main content padding: `48px 56px`
- Section gap: `48px`
- List item gap: `16px`
- Avatar size: `96px × 96px`, `border-radius: 50%`

### Layout Structure

**Two-column sticky sidebar layout:**

```
┌─────────────────┬────────────────────────────────────┐
│  Sidebar (260px)│  Main content (1fr)                │
│  position:sticky│  overflow-y: auto (page scroll)    │
│  top: 0         │                                    │
│  height: 100vh  │  ## About Me                       │
│                 │  ## News                           │
│  [Avatar]       │  ## Selected Publications          │
│  Ying Xiao      │  ## Preprints                      │
│  PhD @ KCL      │  ## Invited Talk                   │
│  [Status badge] │                                    │
│  [Icon links]   │                                    │
└─────────────────┴────────────────────────────────────┘
```

Breakpoint: below `768px`, collapses to single column (sidebar stacks above content).

### Aesthetic Implementation

**Style: Structured Sidebar Scholar**

#### Surface treatment
```css
/* Sidebar */
.sidebar {
  background: #f8f9fa;
  border-right: 1px solid #e5e7eb;
  padding: 32px 24px;
}

/* Content cards / publication entries */
.pub-entry {
  border: none;
  border-left: 3px solid #e5e7eb;
  padding-left: 16px;
  background: transparent;
  box-shadow: none;
  border-radius: 0;
}

.pub-entry:hover {
  border-left-color: #2563eb;
}
```

#### Typography expression
- H1 (name): `font-weight: 700; font-size: 1.5rem; letter-spacing: -0.02em`
- H2 (sections): `font-weight: 600; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.08em; color: #6b7280`
- Body: `font-weight: 400; font-size: 0.9375rem; line-height: 1.65`
- Weight ratio heading:body = 700:400 (clear contrast without size inflation)

#### Decorative rules
- **Allowed:** Subtle left-border accent on publication entries, section label uppercase tracking
- **Forbidden:** Drop shadows, gradients, rounded cards, background fills on content, decorative illustrations

#### Spatial rhythm
- Airy in main content column (generous padding, 48px section gaps)
- Compact in sidebar (identity block is dense but not crowded)
- No visual noise between list items — whitespace is the separator

#### Signature CSS
```css
/* The unmistakable fingerprint of Structured Sidebar Scholar */
body { display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }
.sidebar { position: sticky; top: 0; height: 100vh; overflow-y: auto; }
.main { overflow-y: auto; }
h2.section-label { text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.875rem; color: #6b7280; }
.pub-entry { border-left: 3px solid #e5e7eb; padding-left: 16px; }
```

### Anti-patterns (forbidden)

- No hero banners or full-width image headers
- No card grids with box-shadow
- No colored section backgrounds
- No animated entrance effects
- No icon bullet points
- No gradient backgrounds
- Do not promote bold text from About Me into a separate hero/badge outside its section
