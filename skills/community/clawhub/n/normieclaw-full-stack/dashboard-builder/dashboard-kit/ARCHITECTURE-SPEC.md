# NormieClaw Dashboard Architecture Specification

**Version:** 1.0.0
**Date:** 2026-03-08
**Status:** Canonical — this is the single source of truth for building the NormieClaw unified dashboard.

> **Who reads this document?** An AI agent (Claude, Codex, etc.) tasked with scaffolding, building, and deploying a complete dashboard from scratch. Every value is exact. Every schema is copy-paste ready. No hand-waving.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Unified Design System](#2-unified-design-system)
3. [Shared Shell Architecture](#3-shared-shell-architecture)
4. [Plugin Registration System](#4-plugin-registration-system)
5. [Database Architecture](#5-database-architecture)
6. [Shared Component Library](#6-shared-component-library)
7. [Data Sync Strategy](#7-data-sync-strategy)
8. [Skill Page Template](#8-skill-page-template)
9. [Home Overview Page](#9-home-overview-page)
10. [Auth & Security](#10-auth--security)
11. [Deployment Guide](#11-deployment-guide)
12. [Complete Manifest Definitions](#12-complete-manifest-definitions)

---

## 1. Architecture Overview

### Tech Stack (Non-Negotiable)

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Framework | Next.js (App Router) | 14.2+ | Pages router NOT supported |
| Database | Supabase (PostgreSQL 15+) | Latest | Auth + Storage + Realtime |
| ORM/Client | `@supabase/supabase-js` | 2.x | Server-side: service role; client-side: anon key |
| Styling | Tailwind CSS | 3.4+ | With `tailwind.config.ts` |
| Components | shadcn/ui | Latest | Cherry-pick components, do not install all |
| Charts | Recharts | 2.12+ | Composable React charts |
| Drag & Drop | @dnd-kit/core + @dnd-kit/sortable | 6.x | For Kanban, widget reorder |
| Icons | Lucide React | Latest | Consistent icon set |
| Date | date-fns | 3.x | Lightweight date utils |
| State | React Server Components + `useState`/`useReducer` | — | No Redux, no Zustand |
| Validation | Zod | 3.x | Schema validation for API routes |
| Deployment | Vercel (primary) / Docker (self-hosted) | — | See §11 |

### Application Structure

```
normieclaw-dashboard/
├── app/
│   ├── layout.tsx                    # Root layout (shell + providers)
│   ├── page.tsx                      # Home overview (§9)
│   ├── login/
│   │   └── page.tsx                  # Auth page
│   ├── settings/
│   │   └── page.tsx                  # Global settings
│   ├── notifications/
│   │   └── page.tsx                  # Cross-skill notifications
│   ├── [skill-slug]/                 # Dynamic skill routes
│   │   ├── page.tsx                  # Skill main page
│   │   └── [sub-page]/
│   │       └── page.tsx              # Skill sub-pages
│   └── api/
│       ├── sync/
│       │   └── route.ts             # Generic sync endpoint
│       └── [skill-slug]/
│           └── [...path]/
│               └── route.ts         # Skill-specific API routes
├── components/
│   ├── shell/                        # Layout components (§3)
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   ├── mobile-nav.tsx
│   │   └── notification-center.tsx
│   ├── shared/                       # Shared component library (§6)
│   │   ├── stat-card.tsx
│   │   ├── data-table.tsx
│   │   ├── charts/
│   │   │   ├── line-chart.tsx
│   │   │   ├── bar-chart.tsx
│   │   │   └── donut-chart.tsx
│   │   ├── kanban-board.tsx
│   │   ├── calendar-view.tsx
│   │   ├── timeline.tsx
│   │   ├── card-grid.tsx
│   │   ├── empty-state.tsx
│   │   ├── page-header.tsx
│   │   ├── search-bar.tsx
│   │   ├── progress-ring.tsx
│   │   ├── progress-bar.tsx
│   │   ├── badge-pill.tsx
│   │   ├── detail-modal.tsx
│   │   ├── checklist.tsx
│   │   ├── heatmap.tsx
│   │   ├── tag-cloud.tsx
│   │   └── loading-skeleton.tsx
│   ├── ui/                           # shadcn/ui primitives (auto-generated)
│   └── skills/                       # Skill-specific components
│       ├── expense-report/
│       ├── meal-planner/
│       └── ... (21 directories)
├── lib/
│   ├── supabase/
│   │   ├── client.ts                 # Browser client (anon key)
│   │   ├── server.ts                 # Server client (service role)
│   │   └── middleware.ts             # Auth middleware
│   ├── registry.ts                   # Skill manifest registry (§4)
│   ├── types/
│   │   ├── skill.ts                  # SkillManifest type
│   │   ├── database.ts               # Generated DB types
│   │   └── components.ts             # Shared component prop types
│   └── utils/
│       ├── format.ts                 # Number/date/currency formatting
│       ├── cn.ts                     # clsx + tailwind-merge
│       └── sync.ts                   # Sync adapter utilities
├── skills/                           # Skill manifest + page definitions
│   ├── expense-report/
│   │   ├── manifest.ts
│   │   ├── pages/
│   │   ├── widgets/
│   │   └── migrations/
│   └── ... (21 directories)
├── supabase/
│   └── migrations/                   # All SQL migrations
├── public/
│   ├── noise.svg                     # Noise texture overlay
│   └── logo.svg                      # NormieClaw logo
├── styles/
│   └── globals.css                   # Design tokens + base styles
├── tailwind.config.ts
├── next.config.mjs
├── middleware.ts                      # Auth redirect middleware
└── package.json
```

### Key Architectural Principles

1. **Plugin-first.** Every skill is a self-contained plugin. The shell knows nothing about individual skills — it reads manifests.
2. **One database, prefixed tables.** All 21 skills share one Supabase project. Table collisions prevented by mandatory prefixes.
3. **Server Components by default.** Data fetching happens server-side. Client components only where interactivity requires it (`"use client"`).
4. **No global state library.** React Server Components + URL state (search params) + Supabase Realtime subscriptions.
5. **Dark mode only.** The NormieClaw brand is dark. No light mode toggle in v1.

---

## 2. Unified Design System

### 2.1 Color Tokens

These are the **exact** values from the NormieClaw production site. Use these verbatim.

```css
/* styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Backgrounds */
    --bg-950: #050816;          /* Deepest background (body) */
    --bg-900: #0a1220;          /* Page background */
    --bg-850: #101826;          /* Elevated background (sidebar, header) */

    /* Surfaces */
    --surface-1: #0d1320cc;     /* Cards, panels (80% opacity) */
    --surface-2: #ffffff0d;     /* Subtle surface (5% white) */
    --surface-3: #ffffff14;     /* Hover states (8% white) */

    /* Borders */
    --border-soft: #ffffff17;   /* Subtle borders (9% white) */
    --border-strong: #ffffff29; /* Visible borders (16% white) */

    /* Text */
    --text-1: #f6f7fb;          /* Primary text */
    --text-2: #ecf0f7d6;       /* Secondary text (84% opacity) */
    --text-3: #c9d0e09e;       /* Muted text (62% opacity) */

    /* Accent — Teal (Primary) */
    --teal-500: #14b8a6;        /* Primary accent */
    --teal-400: #2dd4bf;        /* Accent hover */
    --teal-300: #5eead4;        /* Accent light */

    /* Accent — Orange (Secondary / Warnings) */
    --orange-500: #f97316;      /* Secondary accent, warnings */
    --orange-400: #fb923c;      /* Secondary hover */

    /* Status Colors */
    --status-success: #22c55e;  /* Green 500 */
    --status-warning: #eab308;  /* Yellow 500 */
    --status-error: #ef4444;    /* Red 500 */
    --status-info: #3b82f6;     /* Blue 500 */

    /* Shadows */
    --shadow-card: 0 0 0 1px rgba(20, 184, 166, 0.14), 0 20px 60px rgba(6, 182, 212, 0.16);
    --shadow-card-hover: 0 0 0 1px rgba(20, 184, 166, 0.25), 0 25px 70px rgba(6, 182, 212, 0.22);
    --shadow-orange: 0 0 0 1px rgba(249, 115, 22, 0.14), 0 20px 60px rgba(249, 115, 22, 0.16);
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 12px 40px rgba(0, 0, 0, 0.5);
  }
}
```

### 2.2 Tailwind Config

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: 'class',
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './skills/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          950: '#050816',
          900: '#0a1220',
          850: '#101826',
        },
        surface: {
          1: '#0d1320cc',
          2: '#ffffff0d',
          3: '#ffffff14',
        },
        border: {
          soft: '#ffffff17',
          strong: '#ffffff29',
        },
        text: {
          1: '#f6f7fb',
          2: '#ecf0f7d6',
          3: '#c9d0e09e',
        },
        teal: {
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#14b8a6',
        },
        orange: {
          400: '#fb923c',
          500: '#f97316',
        },
        status: {
          success: '#22c55e',
          warning: '#eab308',
          error: '#ef4444',
          info: '#3b82f6',
        },
      },
      fontFamily: {
        sans: ['Manrope', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      fontSize: {
        'display': ['3rem', { lineHeight: '1.1', fontWeight: '800' }],
        'h1': ['2rem', { lineHeight: '1.2', fontWeight: '700' }],
        'h2': ['1.5rem', { lineHeight: '1.3', fontWeight: '600' }],
        'h3': ['1.25rem', { lineHeight: '1.4', fontWeight: '600' }],
        'h4': ['1.125rem', { lineHeight: '1.4', fontWeight: '600' }],
        'body': ['0.9375rem', { lineHeight: '1.6', fontWeight: '400' }],
        'body-sm': ['0.8125rem', { lineHeight: '1.5', fontWeight: '400' }],
        'caption': ['0.75rem', { lineHeight: '1.4', fontWeight: '400' }],
        'mono-data': ['0.875rem', { lineHeight: '1.5', fontWeight: '500' }],
      },
      borderRadius: {
        'xs': '4px',
        'sm': '6px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        '2xl': '20px',
      },
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '16px',
        'lg': '24px',
        'xl': '32px',
        '2xl': '48px',
        '3xl': '64px',
      },
      boxShadow: {
        'card': '0 0 0 1px rgba(20, 184, 166, 0.14), 0 20px 60px rgba(6, 182, 212, 0.16)',
        'card-hover': '0 0 0 1px rgba(20, 184, 166, 0.25), 0 25px 70px rgba(6, 182, 212, 0.22)',
        'orange': '0 0 0 1px rgba(249, 115, 22, 0.14), 0 20px 60px rgba(249, 115, 22, 0.16)',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateX(-12px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 0 1px rgba(20, 184, 166, 0.14)' },
          '50%': { boxShadow: '0 0 0 1px rgba(20, 184, 166, 0.3), 0 0 20px rgba(20, 184, 166, 0.1)' },
        },
      },
      backgroundImage: {
        'noise': "url('/noise.svg')",
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}

export default config
```

### 2.3 Typography Rules

| Element | Font | Weight | Size | Color |
|---------|------|--------|------|-------|
| Page title (h1) | Manrope | 700 | 2rem / 32px | `--text-1` |
| Section heading (h2) | Manrope | 600 | 1.5rem / 24px | `--text-1` |
| Subsection (h3) | Manrope | 600 | 1.25rem / 20px | `--text-1` |
| Body text | Manrope | 400 | 0.9375rem / 15px | `--text-2` |
| Small body | Manrope | 400 | 0.8125rem / 13px | `--text-2` |
| Caption/label | Manrope | 400 | 0.75rem / 12px | `--text-3` |
| Data/numbers | JetBrains Mono | 500 | 0.875rem / 14px | `--text-1` |
| Large metric | JetBrains Mono | 700 | 2rem / 32px | `--text-1` |
| Code/paths | JetBrains Mono | 400 | 0.8125rem / 13px | `--teal-300` |

### 2.4 Spacing Scale

All spacing uses a 4px base unit:

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 4px | Tight gaps (icon-to-label, inline spacing) |
| `sm` | 8px | Small gaps (between related items) |
| `md` | 16px | Default padding (card content, form fields) |
| `lg` | 24px | Section padding (card outer padding) |
| `xl` | 32px | Section gaps (between card groups) |
| `2xl` | 48px | Page sections |
| `3xl` | 64px | Major page divisions |

### 2.5 Border Radius

| Element | Radius | Tailwind Class |
|---------|--------|---------------|
| Buttons | 8px | `rounded-md` |
| Inputs | 8px | `rounded-md` |
| Cards | 12px | `rounded-lg` |
| Modals | 16px | `rounded-xl` |
| Badges/Pills | 9999px | `rounded-full` |
| Avatars | 9999px | `rounded-full` |
| Sidebar | 0px (flush) | `rounded-none` |

### 2.6 Transitions

All interactive elements use:

```css
transition: all 0.2s ease;
```

Specific transitions:
- **Hover color:** `transition-colors duration-200`
- **Sidebar expand/collapse:** `transition-all duration-300 ease-in-out`
- **Modal appear:** `transition-opacity duration-200` + `transition-transform duration-300`
- **Card hover lift:** `transition-shadow duration-200`

### 2.7 Noise Texture Overlay

Apply to all surface-level containers (cards, sidebar, header):

```css
.noise-overlay {
  position: relative;
}
.noise-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('/noise.svg');
  background-repeat: repeat;
  opacity: 0.03;
  pointer-events: none;
  border-radius: inherit;
  z-index: 1;
}
```

Generate `/public/noise.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <filter id="noise">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  <rect width="100%" height="100%" filter="url(#noise)" opacity="1"/>
</svg>
```

### 2.8 Responsive Breakpoints

| Breakpoint | Width | Behavior |
|------------|-------|----------|
| `sm` | 640px | Stack cards, single column |
| `md` | 768px | Sidebar collapses to icons only |
| `lg` | 1024px | Full sidebar + 2-column grid |
| `xl` | 1280px | Full sidebar + 3-column grid |
| `2xl` | 1536px | Full sidebar + 4-column grid |

Mobile (< 768px):
- Sidebar hidden completely
- Bottom navigation bar with 5 pinned skills + "More" menu
- Full-width cards, single column
- Header simplified (title + hamburger menu)

### 2.9 Component Design Variants

#### Card Variants

```
Default Card:     bg-surface-1, border border-soft, rounded-lg, shadow-card
Hover Card:       bg-surface-1, border border-strong, rounded-lg, shadow-card-hover
Accent Card:      bg-surface-1, border-l-4 border-l-teal-500, rounded-lg
Warning Card:     bg-surface-1, border-l-4 border-l-orange-500, rounded-lg, shadow-orange
Interactive Card: hover:bg-surface-3, cursor-pointer, transition-all duration-200
```

#### Button Variants

```
Primary:    bg-teal-500 text-bg-950 hover:bg-teal-400 rounded-md px-4 py-2 font-semibold
Secondary:  bg-surface-2 text-text-1 hover:bg-surface-3 border border-soft rounded-md px-4 py-2
Ghost:      text-text-2 hover:text-text-1 hover:bg-surface-2 rounded-md px-4 py-2
Danger:     bg-status-error text-white hover:bg-red-600 rounded-md px-4 py-2
Icon:       p-2 rounded-md hover:bg-surface-2 text-text-3 hover:text-text-1
```

#### Badge Variants

```
Default:  bg-surface-2 text-text-2 rounded-full px-2.5 py-0.5 text-caption
Teal:     bg-teal-500/15 text-teal-400 rounded-full px-2.5 py-0.5
Orange:   bg-orange-500/15 text-orange-400 rounded-full px-2.5 py-0.5
Success:  bg-status-success/15 text-green-400 rounded-full px-2.5 py-0.5
Error:    bg-status-error/15 text-red-400 rounded-full px-2.5 py-0.5
Warning:  bg-status-warning/15 text-yellow-400 rounded-full px-2.5 py-0.5
```

---

## 3. Shared Shell Architecture

### 3.1 Root Layout

```tsx
// app/layout.tsx
import { Manrope, JetBrains_Mono } from 'next/font/google'
import { Sidebar } from '@/components/shell/sidebar'
import { Header } from '@/components/shell/header'
import { MobileNav } from '@/components/shell/mobile-nav'
import { createServerClient } from '@/lib/supabase/server'
import { registry } from '@/lib/registry'
import '@/styles/globals.css'

const manrope = Manrope({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
})

export const metadata = {
  title: 'NormieClaw Dashboard',
  description: 'Your unified AI skill dashboard',
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return (
      <html lang="en" className="dark">
        <body className={`${manrope.variable} ${jetbrainsMono.variable} font-sans bg-bg-950 text-text-1`}>
          {children}
        </body>
      </html>
    )
  }

  const skills = registry.getEnabledSkills()

  return (
    <html lang="en" className="dark">
      <body className={`${manrope.variable} ${jetbrainsMono.variable} font-sans bg-bg-950 text-text-1`}>
        <div className="flex h-screen overflow-hidden">
          {/* Sidebar — hidden on mobile */}
          <Sidebar skills={skills} className="hidden md:flex" />

          {/* Main content area */}
          <div className="flex flex-1 flex-col overflow-hidden">
            <Header user={user} />
            <main className="flex-1 overflow-y-auto bg-bg-900 p-lg">
              {children}
            </main>
          </div>

          {/* Mobile bottom nav — visible only on mobile */}
          <MobileNav skills={skills} className="md:hidden" />
        </div>
      </body>
    </html>
  )
}
```

### 3.2 Sidebar Component

```tsx
// components/shell/sidebar.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { ChevronLeft, ChevronRight, Settings, Home, Bell } from 'lucide-react'
import { cn } from '@/lib/utils/cn'
import type { SkillManifest } from '@/lib/types/skill'

interface SidebarProps {
  skills: SkillManifest[]
  className?: string
}

export function Sidebar({ skills, className }: SidebarProps) {
  const [collapsed, setCollapsed] = useState(false)
  const [expandedSkill, setExpandedSkill] = useState<string | null>(null)
  const pathname = usePathname()

  return (
    <aside
      className={cn(
        'flex flex-col border-r border-soft bg-bg-850 noise-overlay',
        'transition-all duration-300 ease-in-out',
        collapsed ? 'w-[68px]' : 'w-[260px]',
        className
      )}
    >
      {/* Logo area */}
      <div className="flex h-16 items-center justify-between px-md border-b border-soft">
        {!collapsed && (
          <Link href="/" className="flex items-center gap-sm">
            <img src="/logo.svg" alt="NormieClaw" className="h-8 w-8" />
            <span className="text-h4 font-semibold text-text-1">NormieClaw</span>
          </Link>
        )}
        {collapsed && (
          <Link href="/" className="mx-auto">
            <img src="/logo.svg" alt="NormieClaw" className="h-8 w-8" />
          </Link>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1 rounded-md hover:bg-surface-2 text-text-3 hover:text-text-1 transition-colors"
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-sm px-sm">
        {/* Home */}
        <SidebarItem
          href="/"
          icon={<Home size={20} />}
          label="Dashboard"
          active={pathname === '/'}
          collapsed={collapsed}
        />

        {/* Notifications */}
        <SidebarItem
          href="/notifications"
          icon={<Bell size={20} />}
          label="Notifications"
          active={pathname === '/notifications'}
          collapsed={collapsed}
        />

        {/* Divider */}
        <div className="my-sm mx-md h-px bg-border-soft" />

        {/* Skill nav items */}
        {skills.map((skill) => (
          <SidebarSkillItem
            key={skill.id}
            skill={skill}
            collapsed={collapsed}
            expanded={expandedSkill === skill.id}
            onToggle={() =>
              setExpandedSkill(expandedSkill === skill.id ? null : skill.id)
            }
            pathname={pathname}
          />
        ))}
      </nav>

      {/* Footer — Settings */}
      <div className="border-t border-soft p-sm">
        <SidebarItem
          href="/settings"
          icon={<Settings size={20} />}
          label="Settings"
          active={pathname.startsWith('/settings')}
          collapsed={collapsed}
        />
      </div>
    </aside>
  )
}
```

**Sidebar behavior rules:**
- Default: expanded (260px wide)
- Collapsed: 68px wide, icons only, tooltip on hover shows label
- Skills with sub-pages: chevron expander, sub-items indented 36px
- Active state: `bg-surface-3` background + `text-teal-400` text + left border `border-l-2 border-l-teal-500`
- Hover state: `bg-surface-2`
- Scroll: vertical overflow scrolls within nav area, header and footer pinned

### 3.3 Header Component

```tsx
// components/shell/header.tsx
'use client'

import { usePathname } from 'next/navigation'
import { Bell, Search, User } from 'lucide-react'
import { registry } from '@/lib/registry'
import type { User as SupabaseUser } from '@supabase/supabase-js'

interface HeaderProps {
  user: SupabaseUser
}

export function Header({ user }: HeaderProps) {
  const pathname = usePathname()
  const breadcrumbs = registry.getBreadcrumbs(pathname)

  return (
    <header className="flex h-16 items-center justify-between border-b border-soft bg-bg-850 px-lg noise-overlay">
      {/* Left: Breadcrumbs */}
      <div className="flex items-center gap-xs text-body-sm">
        {breadcrumbs.map((crumb, i) => (
          <span key={i} className="flex items-center gap-xs">
            {i > 0 && <span className="text-text-3">/</span>}
            <span className={i === breadcrumbs.length - 1 ? 'text-text-1' : 'text-text-3'}>
              {crumb.label}
            </span>
          </span>
        ))}
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-sm">
        {/* Global search */}
        <button className="flex items-center gap-xs rounded-md bg-surface-2 px-3 py-1.5 text-body-sm text-text-3 hover:bg-surface-3 transition-colors">
          <Search size={14} />
          <span>Search...</span>
          <kbd className="ml-4 rounded bg-surface-3 px-1.5 py-0.5 text-caption font-mono">⌘K</kbd>
        </button>

        {/* Notifications */}
        <button className="relative p-2 rounded-md hover:bg-surface-2 text-text-3 hover:text-text-1 transition-colors">
          <Bell size={20} />
          {/* Unread dot */}
          <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-orange-500" />
        </button>

        {/* User avatar */}
        <button className="flex items-center gap-sm rounded-md px-2 py-1 hover:bg-surface-2 transition-colors">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-teal-500/20 text-teal-400">
            <User size={16} />
          </div>
        </button>
      </div>
    </header>
  )
}
```

### 3.4 Mobile Navigation

```tsx
// components/shell/mobile-nav.tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Home, MoreHorizontal } from 'lucide-react'
import { cn } from '@/lib/utils/cn'
import type { SkillManifest } from '@/lib/types/skill'

interface MobileNavProps {
  skills: SkillManifest[]
  className?: string
}

export function MobileNav({ skills, className }: MobileNavProps) {
  const pathname = usePathname()
  // Show first 4 skills + More button
  const pinnedSkills = skills.slice(0, 4)

  return (
    <nav
      className={cn(
        'fixed bottom-0 left-0 right-0 z-50',
        'flex items-center justify-around',
        'h-16 border-t border-soft bg-bg-850 noise-overlay',
        'safe-area-inset-bottom',
        className
      )}
    >
      <MobileNavItem href="/" icon={<Home size={22} />} label="Home" active={pathname === '/'} />
      {pinnedSkills.map((skill) => (
        <MobileNavItem
          key={skill.id}
          href={skill.nav.defaultRoute}
          icon={<span className="text-xl">{skill.icon}</span>}
          label={skill.nav.label}
          active={pathname.startsWith(skill.nav.defaultRoute)}
        />
      ))}
      <MobileNavItem href="/more" icon={<MoreHorizontal size={22} />} label="More" active={false} />
    </nav>
  )
}
```

### 3.5 Settings Page Structure

```
/settings
├── Profile         — Name, email, avatar, timezone
├── Skills          — Enable/disable installed skills, reorder sidebar
├── Notifications   — Per-skill notification preferences
├── Data            — Export data, sync status per skill
├── Theme           — Accent color override (future), density
└── Account         — Password change, sign out, delete account
```

### 3.6 Notification Center

Cross-skill notification aggregation:

```typescript
// lib/types/notification.ts
interface Notification {
  id: string
  skill_id: string           // Which skill generated it
  user_id: string
  type: 'info' | 'warning' | 'success' | 'error'
  title: string
  message: string
  action_url?: string        // Deep link to relevant page
  read: boolean
  created_at: string
}
```

Notifications appear in:
1. **Bell icon badge** (unread count, header)
2. **Dropdown panel** (clicking bell, last 20 notifications)
3. **Full page** (`/notifications`) with filters and pagination
4. **Home overview** (critical alerts section)

---

## 4. Plugin Registration System

### 4.1 SkillManifest Type Definition

```typescript
// lib/types/skill.ts

export interface SkillManifest {
  /** Unique skill identifier. Kebab-case. e.g. 'expense-report' */
  id: string

  /** Display name shown in sidebar and headings. e.g. 'Expense Report Pro' */
  displayName: string

  /** Emoji icon for the skill. Used in sidebar and mobile nav. */
  icon: string

  /** Lucide icon name for sidebar (takes precedence over emoji when rendered). */
  lucideIcon: string

  /** 2-4 char lowercase prefix for DB tables. e.g. 'exp' */
  dbPrefix: string

  /** Skill accent color (hex). Used for skill-specific highlights. */
  accentColor: string

  /** Skill version. Semver string. */
  version: string

  /** Sidebar navigation configuration. */
  nav: {
    /** Sidebar label. Keep to ≤14 characters. */
    label: string
    /** Default route when clicking the skill. */
    defaultRoute: string
    /** Sub-pages. Omit for single-page skills. */
    children?: {
      label: string
      route: string
      lucideIcon?: string
    }[]
  }

  /** Sidebar group for organizing skills. */
  category: 'finance' | 'productivity' | 'health' | 'lifestyle' | 'learning' | 'work'

  /** Home overview widgets provided by this skill. Max 2 per skill. */
  homeWidgets: {
    /** Unique widget ID within the skill. */
    id: string
    /** Widget component name (resolved from skills/{id}/widgets/). */
    component: string
    /** Grid column span: 1 = small stat, 2 = medium chart, 3 = wide panel. */
    span: 1 | 2 | 3
    /** Data query function name or table to read from. */
    dataSource: string
  }[]

  /** Database tables this skill owns. Used for migration generation and RLS. */
  tables: {
    /** Full table name with prefix. e.g. 'exp_expenses' */
    name: string
    /** Short description for documentation. */
    description: string
  }[]

  /** Settings fields this skill adds to the global settings page. */
  settings: {
    key: string
    label: string
    type: 'text' | 'number' | 'toggle' | 'select' | 'color'
    defaultValue: string | number | boolean
    options?: { label: string; value: string }[]
    description?: string
  }[]

  /** Data sync configuration. */
  sync: {
    /** How data arrives: 'direct' = API/Supabase, 'json' = local files, 'webhook' = push endpoint. */
    strategy: 'direct' | 'json' | 'webhook'
    /** For JSON strategy: directory where agent writes data files. */
    sourceDir?: string
    /** For webhook strategy: endpoint path (registered under /api/{skill-id}/). */
    webhookPath?: string
  }
}
```

### 4.2 Registry Implementation

```typescript
// lib/registry.ts

import type { SkillManifest } from '@/lib/types/skill'

// Import all skill manifests
import { manifest as expenseReport } from '@/skills/expense-report/manifest'
import { manifest as mealPlanner } from '@/skills/meal-planner/manifest'
import { manifest as superchargedMemory } from '@/skills/supercharged-memory/manifest'
import { manifest as stockWatcher } from '@/skills/stock-watcher/manifest'
import { manifest as travelPlanner } from '@/skills/travel-planner/manifest'
import { manifest as securityTeam } from '@/skills/security-team/manifest'
import { manifest as contentCreator } from '@/skills/content-creator/manifest'
import { manifest as dailyBriefing } from '@/skills/daily-briefing/manifest'
import { manifest as knowledgeVault } from '@/skills/knowledge-vault/manifest'
import { manifest as trainerBuddy } from '@/skills/trainer-buddy/manifest'
import { manifest as emailAssistant } from '@/skills/email-assistant/manifest'
import { manifest as hireMe } from '@/skills/hireme/manifest'
import { manifest as healthBuddy } from '@/skills/health-buddy/manifest'
import { manifest as noteTaker } from '@/skills/notetaker/manifest'
import { manifest as relationshipBuddy } from '@/skills/relationship-buddy/manifest'
import { manifest as tutorBuddy } from '@/skills/tutor-buddy/manifest'
import { manifest as budgetBuddy } from '@/skills/budget-buddy/manifest'
import { manifest as plantDoctor } from '@/skills/plant-doctor/manifest'
import { manifest as docuScan } from '@/skills/docuscan/manifest'
import { manifest as homeFixIt } from '@/skills/home-fix-it/manifest'
import { manifest as invoiceGen } from '@/skills/invoicegen/manifest'

const ALL_SKILLS: SkillManifest[] = [
  expenseReport,
  mealPlanner,
  superchargedMemory,
  stockWatcher,
  travelPlanner,
  securityTeam,
  contentCreator,
  dailyBriefing,
  knowledgeVault,
  trainerBuddy,
  emailAssistant,
  hireMe,
  healthBuddy,
  noteTaker,
  relationshipBuddy,
  tutorBuddy,
  budgetBuddy,
  plantDoctor,
  docuScan,
  homeFixIt,
  invoiceGen,
]

// Category display order for sidebar grouping
const CATEGORY_ORDER: Record<string, number> = {
  finance: 1,
  productivity: 2,
  work: 3,
  health: 4,
  learning: 5,
  lifestyle: 6,
}

const CATEGORY_LABELS: Record<string, string> = {
  finance: 'Finance',
  productivity: 'Productivity',
  work: 'Work',
  health: 'Health & Wellness',
  learning: 'Learning',
  lifestyle: 'Lifestyle',
}

class SkillRegistry {
  private skills: SkillManifest[]

  constructor(skills: SkillManifest[]) {
    this.skills = skills
    this.validateNoDuplicates()
  }

  private validateNoDuplicates() {
    const ids = this.skills.map(s => s.id)
    const prefixes = this.skills.map(s => s.dbPrefix)
    const routes = this.skills.flatMap(s => [
      s.nav.defaultRoute,
      ...(s.nav.children?.map(c => c.route) || []),
    ])
    if (new Set(ids).size !== ids.length) throw new Error('Duplicate skill IDs')
    if (new Set(prefixes).size !== prefixes.length) throw new Error('Duplicate DB prefixes')
    if (new Set(routes).size !== routes.length) throw new Error('Duplicate routes')
  }

  getEnabledSkills(): SkillManifest[] {
    // In v1, all installed skills are enabled.
    // Future: read user preferences from `settings` table.
    return this.skills
  }

  getSkillById(id: string): SkillManifest | undefined {
    return this.skills.find(s => s.id === id)
  }

  getSkillByRoute(pathname: string): SkillManifest | undefined {
    return this.skills.find(s =>
      pathname === s.nav.defaultRoute || pathname.startsWith(s.nav.defaultRoute + '/')
    )
  }

  getGroupedSkills(): { category: string; label: string; skills: SkillManifest[] }[] {
    const groups: Record<string, SkillManifest[]> = {}
    for (const skill of this.skills) {
      if (!groups[skill.category]) groups[skill.category] = []
      groups[skill.category].push(skill)
    }
    return Object.entries(groups)
      .sort(([a], [b]) => (CATEGORY_ORDER[a] || 99) - (CATEGORY_ORDER[b] || 99))
      .map(([category, skills]) => ({
        category,
        label: CATEGORY_LABELS[category] || category,
        skills,
      }))
  }

  getBreadcrumbs(pathname: string): { label: string; href?: string }[] {
    const crumbs: { label: string; href?: string }[] = [{ label: 'Dashboard', href: '/' }]
    const skill = this.getSkillByRoute(pathname)
    if (!skill) return crumbs

    crumbs.push({ label: skill.nav.label, href: skill.nav.defaultRoute })

    const subPage = skill.nav.children?.find(c => pathname === c.route || pathname.startsWith(c.route + '/'))
    if (subPage) {
      crumbs.push({ label: subPage.label })
    }

    return crumbs
  }

  getAllHomeWidgets(): (SkillManifest['homeWidgets'][0] & { skillId: string; skillIcon: string })[] {
    return this.skills.flatMap(s =>
      s.homeWidgets.map(w => ({ ...w, skillId: s.id, skillIcon: s.icon }))
    )
  }

  getAllTables(): { skillId: string; prefix: string; tables: SkillManifest['tables'] }[] {
    return this.skills.map(s => ({
      skillId: s.id,
      prefix: s.dbPrefix,
      tables: s.tables,
    }))
  }
}

export const registry = new SkillRegistry(ALL_SKILLS)
```

### 4.3 Adding/Removing Skills

To add a new skill:
1. Create `skills/{skill-id}/manifest.ts` exporting a `SkillManifest`
2. Create `skills/{skill-id}/pages/` with page components
3. Create `skills/{skill-id}/widgets/` with home overview widget components
4. Create `skills/{skill-id}/migrations/` with SQL migration file
5. Add the import + array entry in `lib/registry.ts`
6. Create `app/{skill-slug}/page.tsx` that renders the skill's main page
7. Run `supabase db push` to apply migrations

To remove a skill:
1. Remove the import and array entry from `lib/registry.ts`
2. Delete the `skills/{skill-id}/` directory
3. Delete the `app/{skill-slug}/` route directory
4. Optionally: run the skill's `down.sql` migration to drop tables

---

## 5. Database Architecture

### 5.1 Overview

- **One Supabase project.** All skills coexist in a single PostgreSQL database.
- **Table naming:** `{prefix}_{entity_plural}` — always lowercase snake_case.
- **Shared tables:** `users`, `settings`, `notifications` — no prefix.
- **Every table** gets `user_id`, `created_at`, `updated_at`, and RLS.

### 5.2 Skill Prefix Registry

| Skill | Prefix | Example Table |
|-------|--------|--------------|
| Expense Report Pro | `exp` | `exp_expenses` |
| Meal Planner Pro | `mp` | `mp_recipes` |
| Supercharged Memory | `mem` | `mem_memories` |
| Stock Watcher Pro | `sw` | `sw_holdings` |
| Travel Planner Pro | `tp` | `tp_trips` |
| Security Team | `sec` | `sec_audits` |
| Content Creator Pro | `cc` | `cc_posts` |
| Daily Briefing | `dbr` | `dbr_briefings` |
| Knowledge Vault | `kv` | `kv_entries` |
| Trainer Buddy Pro | `tb` | `tb_workouts` |
| Email Assistant | `ea` | `ea_email_triage` |
| HireMe Pro | `hm` | `hm_applications` |
| Health Buddy Pro | `hb` | `hb_nutrition_entries` |
| NoteTaker Pro | `nt` | `nt_notes` |
| Relationship Buddy | `rb` | `rb_contacts` |
| Tutor Buddy Pro | `tu` | `tu_sessions` |
| Budget Buddy Pro | `bb` | `bb_transactions` |
| Plant Doctor | `pd` | `pd_plants` |
| DocuScan | `ds` | `ds_scans` |
| Home Fix-It | `hf` | `hf_repair_logs` |
| InvoiceGen | `ig` | `ig_invoices` |

> **Note:** Daily Briefing uses `dbr` (not `db`) to avoid collision with common database abbreviations.

### 5.3 Shared Tables Schema

```sql
-- supabase/migrations/00000_core_setup.sql

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Shared: User profiles (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name TEXT,
  avatar_url TEXT,
  timezone TEXT DEFAULT 'UTC',
  pinned_skills TEXT[] DEFAULT '{}',
  sidebar_order TEXT[] DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can read own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- Shared: Skill-specific settings (key-value per user per skill)
CREATE TABLE IF NOT EXISTS settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  skill_id TEXT NOT NULL,
  key TEXT NOT NULL,
  value JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, skill_id, key)
);

ALTER TABLE settings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can read own settings" ON settings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own settings" ON settings FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own settings" ON settings FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own settings" ON settings FOR DELETE USING (auth.uid() = user_id);

-- Shared: Cross-skill notifications
CREATE TABLE IF NOT EXISTS notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  skill_id TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('info', 'warning', 'success', 'error')),
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  action_url TEXT,
  read BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notifications_user_unread ON notifications(user_id, read) WHERE read = FALSE;
CREATE INDEX idx_notifications_user_created ON notifications(user_id, created_at DESC);

ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can read own notifications" ON notifications FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own notifications" ON notifications FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own notifications" ON notifications FOR DELETE USING (auth.uid() = user_id);
-- INSERT is service-role only (agents/webhooks write notifications, not users directly)

-- Helper: Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to shared tables
CREATE TRIGGER profiles_updated_at BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER settings_updated_at BEFORE UPDATE ON settings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Auto-create profile on user signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, display_name) VALUES (NEW.id, NEW.raw_user_meta_data->>'name');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();
```

### 5.4 Standard Column Requirements

**Every skill table MUST include these columns:**

```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

**Every skill table MUST have:**
1. RLS enabled: `ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;`
2. Per-operation policies (SELECT, INSERT, UPDATE, DELETE)
3. An `updated_at` trigger
4. An index on `user_id`

**Exceptions:**
- Junction/join tables (e.g., `mp_meal_slot_members`) may omit `user_id` if the parent table has it and the relationship is through a FK
- Lookup/reference tables (e.g., `tb_exercises`) shared across users may omit `user_id` and use `FOR ALL` RLS

### 5.5 RLS Policy Template

Apply this template to every skill-owned table:

```sql
-- Template: RLS for {TABLE_NAME}
ALTER TABLE {TABLE_NAME} ENABLE ROW LEVEL SECURITY;

CREATE POLICY "{TABLE_NAME}_select" ON {TABLE_NAME}
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "{TABLE_NAME}_insert" ON {TABLE_NAME}
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "{TABLE_NAME}_update" ON {TABLE_NAME}
  FOR UPDATE USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "{TABLE_NAME}_delete" ON {TABLE_NAME}
  FOR DELETE USING (auth.uid() = user_id);
```

For tables accessed by service role (sync scripts, webhooks):
- Service role key bypasses RLS automatically
- Never expose the service role key to client-side code

### 5.6 Migration File Convention

```
supabase/migrations/
├── 00000_core_setup.sql              # Shared tables (profiles, settings, notifications)
├── 00001_exp_tables.sql              # Expense Report Pro
├── 00002_mp_tables.sql               # Meal Planner Pro
├── 00003_mem_tables.sql              # Supercharged Memory
├── 00004_sw_tables.sql               # Stock Watcher Pro
├── 00005_tp_tables.sql               # Travel Planner Pro
├── 00006_sec_tables.sql              # Security Team
├── 00007_cc_tables.sql               # Content Creator Pro
├── 00008_dbr_tables.sql              # Daily Briefing
├── 00009_kv_tables.sql               # Knowledge Vault
├── 00010_tb_tables.sql               # Trainer Buddy Pro
├── 00011_ea_tables.sql               # Email Assistant
├── 00012_hm_tables.sql               # HireMe Pro
├── 00013_hb_tables.sql               # Health Buddy Pro
├── 00014_nt_tables.sql               # NoteTaker Pro
├── 00015_rb_tables.sql               # Relationship Buddy
├── 00016_tu_tables.sql               # Tutor Buddy Pro
├── 00017_bb_tables.sql               # Budget Buddy Pro
├── 00018_pd_tables.sql               # Plant Doctor
├── 00019_ds_tables.sql               # DocuScan
├── 00020_hf_tables.sql               # Home Fix-It
├── 00021_ig_tables.sql               # InvoiceGen
├── 00022_views.sql                   # Cross-skill views
└── 00023_seed.sql                    # Optional seed data
```

Each migration file must be idempotent (use `CREATE TABLE IF NOT EXISTS`).

### 5.7 Complete Schema — All 21 Skills

#### Expense Report Pro (prefix: `exp`)

```sql
-- 00001_exp_tables.sql
CREATE TABLE IF NOT EXISTS exp_expenses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  vendor TEXT NOT NULL,
  category TEXT NOT NULL,
  subcategory TEXT,
  amount_cents INTEGER NOT NULL,
  currency TEXT NOT NULL DEFAULT 'USD',
  payment_method TEXT,
  receipt_url TEXT,
  notes TEXT,
  tags TEXT[] DEFAULT '{}',
  is_reimbursable BOOLEAN NOT NULL DEFAULT FALSE,
  status TEXT NOT NULL DEFAULT 'logged' CHECK (status IN ('logged', 'submitted', 'approved', 'reimbursed')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_exp_expenses_user_date ON exp_expenses(user_id, date DESC);
CREATE INDEX idx_exp_expenses_category ON exp_expenses(user_id, category);

ALTER TABLE exp_expenses ENABLE ROW LEVEL SECURITY;
CREATE POLICY "exp_expenses_select" ON exp_expenses FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "exp_expenses_insert" ON exp_expenses FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "exp_expenses_update" ON exp_expenses FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "exp_expenses_delete" ON exp_expenses FOR DELETE USING (auth.uid() = user_id);

CREATE TRIGGER exp_expenses_updated_at BEFORE UPDATE ON exp_expenses
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Meal Planner Pro (prefix: `mp`)

```sql
-- 00002_mp_tables.sql
CREATE TABLE IF NOT EXISTS mp_households (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL DEFAULT 'My Household',
  budget_preference TEXT DEFAULT 'moderate' CHECK (budget_preference IN ('budget', 'moderate', 'premium')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mp_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID NOT NULL REFERENCES mp_households(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  role TEXT DEFAULT 'member',
  allergies TEXT[] DEFAULT '{}',
  dislikes TEXT[] DEFAULT '{}',
  adventurousness INTEGER DEFAULT 5 CHECK (adventurousness BETWEEN 1 AND 10),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mp_dietary_preferences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID NOT NULL REFERENCES mp_households(id) ON DELETE CASCADE,
  key TEXT NOT NULL,
  label TEXT NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mp_recipes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  instructions JSONB DEFAULT '[]',
  prep_time_minutes INTEGER,
  cook_time_minutes INTEGER,
  servings INTEGER DEFAULT 4,
  cuisine TEXT,
  difficulty TEXT DEFAULT 'medium' CHECK (difficulty IN ('easy', 'medium', 'hard')),
  image_url TEXT,
  source_url TEXT,
  tags TEXT[] DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mp_recipe_ingredients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  recipe_id UUID NOT NULL REFERENCES mp_recipes(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  quantity NUMERIC(10,2),
  unit TEXT,
  notes TEXT,
  sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS mp_meal_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID NOT NULL REFERENCES mp_households(id) ON DELETE CASCADE,
  week_start DATE NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'archived')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mp_meal_slots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  meal_plan_id UUID NOT NULL REFERENCES mp_meal_plans(id) ON DELETE CASCADE,
  day INTEGER NOT NULL CHECK (day BETWEEN 0 AND 6),
  meal_type TEXT NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
  recipe_id UUID REFERENCES mp_recipes(id) ON DELETE SET NULL,
  custom_meal TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS mp_meal_slot_members (
  meal_slot_id UUID NOT NULL REFERENCES mp_meal_slots(id) ON DELETE CASCADE,
  member_id UUID NOT NULL REFERENCES mp_members(id) ON DELETE CASCADE,
  PRIMARY KEY (meal_slot_id, member_id)
);

CREATE TABLE IF NOT EXISTS mp_ratings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  meal_slot_id UUID NOT NULL REFERENCES mp_meal_slots(id) ON DELETE CASCADE,
  member_id UUID NOT NULL REFERENCES mp_members(id) ON DELETE CASCADE,
  recipe_id UUID REFERENCES mp_recipes(id) ON DELETE SET NULL,
  score INTEGER NOT NULL CHECK (score BETWEEN 1 AND 5),
  comment TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(meal_slot_id, member_id)
);

CREATE TABLE IF NOT EXISTS mp_grocery_lists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  meal_plan_id UUID NOT NULL REFERENCES mp_meal_plans(id) ON DELETE CASCADE,
  estimated_total_cents INTEGER,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'shopping', 'completed')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mp_grocery_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  grocery_list_id UUID NOT NULL REFERENCES mp_grocery_lists(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  quantity NUMERIC(10,2),
  unit TEXT,
  store TEXT,
  category TEXT,
  checked BOOLEAN NOT NULL DEFAULT FALSE,
  sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS mp_stores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID NOT NULL REFERENCES mp_households(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  role TEXT DEFAULT 'general',
  color TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mp_freezer_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID NOT NULL REFERENCES mp_households(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  quantity TEXT,
  added_date DATE NOT NULL DEFAULT CURRENT_DATE,
  expiry_date DATE,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mp_flagged_recipes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID NOT NULL REFERENCES mp_households(id) ON DELETE CASCADE,
  recipe_id UUID NOT NULL REFERENCES mp_recipes(id) ON DELETE CASCADE,
  match_score NUMERIC(3,2),
  source TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mp_chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  meal_plan_id UUID NOT NULL REFERENCES mp_meal_plans(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mp_pantry_staples (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  household_id UUID NOT NULL REFERENCES mp_households(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  times_marked_have INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- RLS for all mp_ tables (household-based access)
-- Households: direct user_id check
ALTER TABLE mp_households ENABLE ROW LEVEL SECURITY;
CREATE POLICY "mp_households_select" ON mp_households FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "mp_households_insert" ON mp_households FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "mp_households_update" ON mp_households FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "mp_households_delete" ON mp_households FOR DELETE USING (auth.uid() = user_id);

-- Child tables: access through household ownership
ALTER TABLE mp_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY "mp_members_select" ON mp_members FOR SELECT
  USING (household_id IN (SELECT id FROM mp_households WHERE user_id = auth.uid()));
CREATE POLICY "mp_members_insert" ON mp_members FOR INSERT
  WITH CHECK (household_id IN (SELECT id FROM mp_households WHERE user_id = auth.uid()));
CREATE POLICY "mp_members_update" ON mp_members FOR UPDATE
  USING (household_id IN (SELECT id FROM mp_households WHERE user_id = auth.uid()));
CREATE POLICY "mp_members_delete" ON mp_members FOR DELETE
  USING (household_id IN (SELECT id FROM mp_households WHERE user_id = auth.uid()));

-- Recipes: direct user_id
ALTER TABLE mp_recipes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "mp_recipes_select" ON mp_recipes FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "mp_recipes_insert" ON mp_recipes FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "mp_recipes_update" ON mp_recipes FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "mp_recipes_delete" ON mp_recipes FOR DELETE USING (auth.uid() = user_id);

-- Apply same household-based RLS pattern to: mp_dietary_preferences, mp_meal_plans,
-- mp_stores, mp_freezer_items, mp_flagged_recipes, mp_pantry_staples
-- Apply meal_plan->household chain for: mp_meal_slots, mp_grocery_lists, mp_chat_messages
-- Apply recipe->user chain for: mp_recipe_ingredients
-- Apply meal_slot->meal_plan->household chain for: mp_meal_slot_members, mp_ratings
-- Apply grocery_list->meal_plan->household chain for: mp_grocery_items

-- [Agent: Generate the remaining RLS policies following the ownership chain patterns above]

-- Indexes
CREATE INDEX idx_mp_recipes_user ON mp_recipes(user_id);
CREATE INDEX idx_mp_meal_plans_household ON mp_meal_plans(household_id, week_start DESC);
CREATE INDEX idx_mp_meal_slots_plan ON mp_meal_slots(meal_plan_id);
CREATE INDEX idx_mp_grocery_items_list ON mp_grocery_items(grocery_list_id);

-- Updated_at triggers
CREATE TRIGGER mp_households_updated_at BEFORE UPDATE ON mp_households FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER mp_recipes_updated_at BEFORE UPDATE ON mp_recipes FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER mp_meal_plans_updated_at BEFORE UPDATE ON mp_meal_plans FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER mp_grocery_lists_updated_at BEFORE UPDATE ON mp_grocery_lists FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Supercharged Memory (prefix: `mem`)

```sql
-- 00003_mem_tables.sql
CREATE TABLE IF NOT EXISTS mem_memories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  category TEXT NOT NULL DEFAULT 'general',
  source_file TEXT,
  tags TEXT[] DEFAULT '{}',
  importance NUMERIC(3,2) DEFAULT 0.5 CHECK (importance BETWEEN 0 AND 1),
  embedding VECTOR(1536),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS mem_stats (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  total_memories INTEGER NOT NULL DEFAULT 0,
  vector_count INTEGER NOT NULL DEFAULT 0,
  categories_breakdown JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, date)
);

CREATE INDEX idx_mem_memories_user ON mem_memories(user_id);
CREATE INDEX idx_mem_memories_category ON mem_memories(user_id, category);
CREATE INDEX idx_mem_stats_user_date ON mem_stats(user_id, date DESC);

-- Note: VECTOR type requires pgvector extension
-- CREATE EXTENSION IF NOT EXISTS vector;
-- CREATE INDEX idx_mem_memories_embedding ON mem_memories USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

ALTER TABLE mem_memories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "mem_memories_select" ON mem_memories FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "mem_memories_insert" ON mem_memories FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "mem_memories_update" ON mem_memories FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "mem_memories_delete" ON mem_memories FOR DELETE USING (auth.uid() = user_id);

ALTER TABLE mem_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "mem_stats_select" ON mem_stats FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "mem_stats_insert" ON mem_stats FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "mem_stats_update" ON mem_stats FOR UPDATE USING (auth.uid() = user_id);

CREATE TRIGGER mem_memories_updated_at BEFORE UPDATE ON mem_memories FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Stock Watcher Pro (prefix: `sw`)

```sql
-- 00004_sw_tables.sql
CREATE TABLE IF NOT EXISTS sw_portfolios (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL DEFAULT 'Default Portfolio',
  description TEXT,
  is_default BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sw_holdings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  portfolio_id UUID NOT NULL REFERENCES sw_portfolios(id) ON DELETE CASCADE,
  ticker TEXT NOT NULL,
  company_name TEXT NOT NULL,
  shares NUMERIC(12,4) NOT NULL DEFAULT 0,
  avg_cost_cents INTEGER,
  thesis TEXT,
  sector TEXT,
  added_date DATE NOT NULL DEFAULT CURRENT_DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sw_briefings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  type TEXT NOT NULL DEFAULT 'daily' CHECK (type IN ('daily', 'weekly', 'alert')),
  content_md TEXT NOT NULL,
  market_sentiment TEXT CHECK (market_sentiment IN ('bullish', 'bearish', 'neutral', 'mixed')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sw_filing_summaries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  ticker TEXT NOT NULL,
  form_type TEXT NOT NULL,
  filing_date DATE NOT NULL,
  ai_summary TEXT NOT NULL,
  impact_score INTEGER CHECK (impact_score BETWEEN 1 AND 10),
  filing_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sw_news_links (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  ticker TEXT,
  title TEXT NOT NULL,
  source TEXT NOT NULL,
  url TEXT NOT NULL,
  ai_summary TEXT,
  sentiment TEXT CHECK (sentiment IN ('positive', 'negative', 'neutral')),
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sw_source_network (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  ticker TEXT,
  source_name TEXT NOT NULL,
  feed_url TEXT NOT NULL,
  health_status TEXT NOT NULL DEFAULT 'healthy' CHECK (health_status IN ('healthy', 'degraded', 'dead')),
  last_checked_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sw_thesis_tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  ticker TEXT NOT NULL,
  thesis_state TEXT NOT NULL DEFAULT 'active' CHECK (thesis_state IN ('active', 'paused', 'invalidated', 'realized')),
  original_thesis TEXT NOT NULL,
  catalyst_noted TEXT,
  price_at_entry_cents INTEGER,
  price_at_time_cents INTEGER,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_sw_portfolios_user ON sw_portfolios(user_id);
CREATE INDEX idx_sw_holdings_portfolio ON sw_holdings(portfolio_id);
CREATE INDEX idx_sw_holdings_ticker ON sw_holdings(ticker);
CREATE INDEX idx_sw_briefings_user_date ON sw_briefings(user_id, date DESC);
CREATE INDEX idx_sw_filing_summaries_ticker ON sw_filing_summaries(user_id, ticker, filing_date DESC);
CREATE INDEX idx_sw_news_links_ticker ON sw_news_links(user_id, ticker, created_at DESC);

-- RLS (standard user_id pattern for all sw_ tables)
ALTER TABLE sw_portfolios ENABLE ROW LEVEL SECURITY;
CREATE POLICY "sw_portfolios_select" ON sw_portfolios FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "sw_portfolios_insert" ON sw_portfolios FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "sw_portfolios_update" ON sw_portfolios FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "sw_portfolios_delete" ON sw_portfolios FOR DELETE USING (auth.uid() = user_id);

-- sw_holdings: access through portfolio ownership
ALTER TABLE sw_holdings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "sw_holdings_select" ON sw_holdings FOR SELECT
  USING (portfolio_id IN (SELECT id FROM sw_portfolios WHERE user_id = auth.uid()));
CREATE POLICY "sw_holdings_insert" ON sw_holdings FOR INSERT
  WITH CHECK (portfolio_id IN (SELECT id FROM sw_portfolios WHERE user_id = auth.uid()));
CREATE POLICY "sw_holdings_update" ON sw_holdings FOR UPDATE
  USING (portfolio_id IN (SELECT id FROM sw_portfolios WHERE user_id = auth.uid()));
CREATE POLICY "sw_holdings_delete" ON sw_holdings FOR DELETE
  USING (portfolio_id IN (SELECT id FROM sw_portfolios WHERE user_id = auth.uid()));

-- [Apply standard user_id RLS to: sw_briefings, sw_filing_summaries, sw_news_links, sw_source_network, sw_thesis_tracking]

CREATE TRIGGER sw_portfolios_updated_at BEFORE UPDATE ON sw_portfolios FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER sw_holdings_updated_at BEFORE UPDATE ON sw_holdings FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER sw_source_network_updated_at BEFORE UPDATE ON sw_source_network FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER sw_thesis_tracking_updated_at BEFORE UPDATE ON sw_thesis_tracking FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Travel Planner Pro (prefix: `tp`)

```sql
-- 00005_tp_tables.sql
CREATE TABLE IF NOT EXISTS tp_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  pace_preference TEXT DEFAULT 'moderate' CHECK (pace_preference IN ('relaxed', 'moderate', 'packed')),
  budget_style TEXT DEFAULT 'mid-range' CHECK (budget_style IN ('budget', 'mid-range', 'luxury')),
  home_airport TEXT,
  travel_style TEXT[] DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS tp_trips (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id UUID NOT NULL REFERENCES tp_profiles(id) ON DELETE CASCADE,
  destination TEXT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  budget_total_cents INTEGER,
  currency TEXT DEFAULT 'USD',
  status TEXT NOT NULL DEFAULT 'planning' CHECK (status IN ('planning', 'booked', 'active', 'completed', 'cancelled')),
  cover_image_url TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tp_trip_days (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  trip_id UUID NOT NULL REFERENCES tp_trips(id) ON DELETE CASCADE,
  day_number INTEGER NOT NULL,
  date DATE NOT NULL,
  theme TEXT,
  weather JSONB,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS tp_activities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  day_id UUID NOT NULL REFERENCES tp_trip_days(id) ON DELETE CASCADE,
  time_slot TEXT,
  title TEXT NOT NULL,
  location TEXT,
  cost_estimate_cents INTEGER,
  booked BOOLEAN NOT NULL DEFAULT FALSE,
  confirmation_number TEXT,
  notes TEXT,
  sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tp_trip_budgets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  trip_id UUID NOT NULL REFERENCES tp_trips(id) ON DELETE CASCADE,
  category TEXT NOT NULL,
  estimated_cents INTEGER NOT NULL DEFAULT 0,
  booked_cents INTEGER NOT NULL DEFAULT 0,
  actual_cents INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tp_packing_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  trip_id UUID NOT NULL REFERENCES tp_trips(id) ON DELETE CASCADE,
  category TEXT NOT NULL,
  item TEXT NOT NULL,
  packed BOOLEAN NOT NULL DEFAULT FALSE,
  sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tp_companions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id UUID NOT NULL REFERENCES tp_profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  relationship TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tp_loyalty_programs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id UUID NOT NULL REFERENCES tp_profiles(id) ON DELETE CASCADE,
  program TEXT NOT NULL,
  tier TEXT,
  member_number TEXT,
  points INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tp_profiles_user ON tp_profiles(user_id);
CREATE INDEX idx_tp_trips_profile ON tp_trips(profile_id, start_date DESC);
CREATE INDEX idx_tp_trip_days_trip ON tp_trip_days(trip_id, day_number);

-- RLS: tp_profiles uses user_id, children chain through profile_id -> user_id
ALTER TABLE tp_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "tp_profiles_select" ON tp_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "tp_profiles_insert" ON tp_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "tp_profiles_update" ON tp_profiles FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "tp_profiles_delete" ON tp_profiles FOR DELETE USING (auth.uid() = user_id);

-- [Apply chain-based RLS for child tables through tp_profiles.user_id]

CREATE TRIGGER tp_profiles_updated_at BEFORE UPDATE ON tp_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tp_trips_updated_at BEFORE UPDATE ON tp_trips FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tp_loyalty_programs_updated_at BEFORE UPDATE ON tp_loyalty_programs FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Security Team (prefix: `sec`)

```sql
-- 00006_sec_tables.sql
CREATE TABLE IF NOT EXISTS sec_audits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  run_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  overall_score NUMERIC(4,1) NOT NULL CHECK (overall_score BETWEEN 0 AND 10),
  findings_count INTEGER NOT NULL DEFAULT 0,
  critical_count INTEGER NOT NULL DEFAULT 0,
  raw_log JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sec_issues (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  audit_id UUID REFERENCES sec_audits(id) ON DELETE SET NULL,
  council TEXT NOT NULL,
  severity TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  remediation TEXT,
  status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'wont_fix')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sec_audits_user ON sec_audits(user_id, run_date DESC);
CREATE INDEX idx_sec_issues_user ON sec_issues(user_id, status);

ALTER TABLE sec_audits ENABLE ROW LEVEL SECURITY;
CREATE POLICY "sec_audits_select" ON sec_audits FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "sec_audits_insert" ON sec_audits FOR INSERT WITH CHECK (auth.uid() = user_id);

ALTER TABLE sec_issues ENABLE ROW LEVEL SECURITY;
CREATE POLICY "sec_issues_select" ON sec_issues FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "sec_issues_insert" ON sec_issues FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "sec_issues_update" ON sec_issues FOR UPDATE USING (auth.uid() = user_id);

CREATE TRIGGER sec_issues_updated_at BEFORE UPDATE ON sec_issues FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Content Creator Pro (prefix: `cc`)

```sql
-- 00007_cc_tables.sql
CREATE TABLE IF NOT EXISTS cc_brand_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  brand_name TEXT NOT NULL,
  voice JSONB DEFAULT '{}',
  platforms JSONB DEFAULT '[]',
  target_audience TEXT,
  is_default BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cc_content_pillars (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID NOT NULL REFERENCES cc_brand_profiles(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  target_ratio NUMERIC(3,2) DEFAULT 0.25,
  color TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cc_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID NOT NULL REFERENCES cc_brand_profiles(id) ON DELETE CASCADE,
  pillar_id UUID REFERENCES cc_content_pillars(id) ON DELETE SET NULL,
  platform TEXT NOT NULL,
  topic TEXT NOT NULL,
  content TEXT,
  media_urls TEXT[] DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'idea' CHECK (status IN ('idea', 'draft', 'review', 'scheduled', 'published')),
  scheduled_date TIMESTAMPTZ,
  published_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cc_engagement_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES cc_posts(id) ON DELETE CASCADE,
  impressions INTEGER DEFAULT 0,
  likes INTEGER DEFAULT 0,
  comments INTEGER DEFAULT 0,
  shares INTEGER DEFAULT 0,
  clicks INTEGER DEFAULT 0,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cc_idea_bank (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID NOT NULL REFERENCES cc_brand_profiles(id) ON DELETE CASCADE,
  idea TEXT NOT NULL,
  pillar_id UUID REFERENCES cc_content_pillars(id) ON DELETE SET NULL,
  used BOOLEAN NOT NULL DEFAULT FALSE,
  priority INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cc_voice_learnings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID NOT NULL REFERENCES cc_brand_profiles(id) ON DELETE CASCADE,
  original_snippet TEXT NOT NULL,
  edited_snippet TEXT NOT NULL,
  learning TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cc_competitor_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID NOT NULL REFERENCES cc_brand_profiles(id) ON DELETE CASCADE,
  competitor_name TEXT NOT NULL,
  insights TEXT NOT NULL,
  platform TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_cc_brand_profiles_user ON cc_brand_profiles(user_id);
CREATE INDEX idx_cc_posts_brand ON cc_posts(brand_id, status);
CREATE INDEX idx_cc_posts_scheduled ON cc_posts(scheduled_date) WHERE status = 'scheduled';

-- RLS: cc_brand_profiles uses user_id, children chain through brand_id
ALTER TABLE cc_brand_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "cc_brand_profiles_select" ON cc_brand_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "cc_brand_profiles_insert" ON cc_brand_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "cc_brand_profiles_update" ON cc_brand_profiles FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "cc_brand_profiles_delete" ON cc_brand_profiles FOR DELETE USING (auth.uid() = user_id);

-- [Apply chain-based RLS for all cc_ child tables through cc_brand_profiles.user_id]

CREATE TRIGGER cc_brand_profiles_updated_at BEFORE UPDATE ON cc_brand_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER cc_posts_updated_at BEFORE UPDATE ON cc_posts FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Daily Briefing (prefix: `dbr`)

```sql
-- 00008_dbr_tables.sql
CREATE TABLE IF NOT EXISTS dbr_briefings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  executive_summary TEXT,
  stories_count INTEGER NOT NULL DEFAULT 0,
  raw_markdown TEXT,
  delivered BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, date)
);

CREATE TABLE IF NOT EXISTS dbr_stories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  briefing_id UUID NOT NULL REFERENCES dbr_briefings(id) ON DELETE CASCADE,
  topic TEXT NOT NULL,
  headline TEXT NOT NULL,
  synthesis TEXT NOT NULL,
  sources JSONB DEFAULT '[]',
  importance INTEGER DEFAULT 5 CHECK (importance BETWEEN 1 AND 10),
  sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS dbr_sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  url TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('rss', 'api', 'scrape', 'email')),
  topic TEXT,
  reliability_score NUMERIC(3,2) DEFAULT 1.0,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dbr_feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  briefing_id UUID REFERENCES dbr_briefings(id) ON DELETE SET NULL,
  date DATE NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('thumbs_up', 'thumbs_down', 'comment')),
  comment TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dbr_source_fetch_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID NOT NULL REFERENCES dbr_sources(id) ON DELETE CASCADE,
  fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  success BOOLEAN NOT NULL,
  items_found INTEGER DEFAULT 0,
  error_message TEXT
);

-- Indexes
CREATE INDEX idx_dbr_briefings_user_date ON dbr_briefings(user_id, date DESC);
CREATE INDEX idx_dbr_stories_briefing ON dbr_stories(briefing_id);
CREATE INDEX idx_dbr_sources_user ON dbr_sources(user_id, is_active);
CREATE INDEX idx_dbr_source_fetch_log_source ON dbr_source_fetch_log(source_id, fetched_at DESC);

-- RLS
ALTER TABLE dbr_briefings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "dbr_briefings_select" ON dbr_briefings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "dbr_briefings_insert" ON dbr_briefings FOR INSERT WITH CHECK (auth.uid() = user_id);

ALTER TABLE dbr_sources ENABLE ROW LEVEL SECURITY;
CREATE POLICY "dbr_sources_select" ON dbr_sources FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "dbr_sources_insert" ON dbr_sources FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "dbr_sources_update" ON dbr_sources FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "dbr_sources_delete" ON dbr_sources FOR DELETE USING (auth.uid() = user_id);

-- [Apply chain-based RLS for dbr_stories, dbr_feedback, dbr_source_fetch_log]

CREATE TRIGGER dbr_sources_updated_at BEFORE UPDATE ON dbr_sources FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Knowledge Vault (prefix: `kv`)

```sql
-- 00009_kv_tables.sql
CREATE TABLE IF NOT EXISTS kv_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  url TEXT,
  content_type TEXT NOT NULL DEFAULT 'article' CHECK (content_type IN ('article', 'paper', 'book', 'video', 'podcast', 'tweet', 'note', 'other')),
  executive_summary TEXT,
  full_text TEXT,
  tags TEXT[] DEFAULT '{}',
  collection TEXT DEFAULT 'general',
  status TEXT NOT NULL DEFAULT 'unread' CHECK (status IN ('unread', 'reading', 'read', 'archived')),
  importance INTEGER DEFAULT 5 CHECK (importance BETWEEN 1 AND 10),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS kv_collections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  color TEXT,
  icon TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, name)
);

CREATE INDEX idx_kv_entries_user ON kv_entries(user_id, created_at DESC);
CREATE INDEX idx_kv_entries_collection ON kv_entries(user_id, collection);
CREATE INDEX idx_kv_entries_tags ON kv_entries USING gin(tags);
CREATE INDEX idx_kv_entries_status ON kv_entries(user_id, status);

ALTER TABLE kv_entries ENABLE ROW LEVEL SECURITY;
CREATE POLICY "kv_entries_select" ON kv_entries FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "kv_entries_insert" ON kv_entries FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "kv_entries_update" ON kv_entries FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "kv_entries_delete" ON kv_entries FOR DELETE USING (auth.uid() = user_id);

ALTER TABLE kv_collections ENABLE ROW LEVEL SECURITY;
CREATE POLICY "kv_collections_select" ON kv_collections FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "kv_collections_insert" ON kv_collections FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "kv_collections_update" ON kv_collections FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "kv_collections_delete" ON kv_collections FOR DELETE USING (auth.uid() = user_id);

CREATE TRIGGER kv_entries_updated_at BEFORE UPDATE ON kv_entries FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Trainer Buddy Pro (prefix: `tb`)

```sql
-- 00010_tb_tables.sql
CREATE TABLE IF NOT EXISTS tb_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT,
  weight_lbs NUMERIC(5,1),
  height_inches INTEGER,
  experience_level TEXT DEFAULT 'intermediate' CHECK (experience_level IN ('beginner', 'intermediate', 'advanced')),
  primary_goal TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS tb_injuries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  area TEXT NOT NULL,
  severity TEXT NOT NULL DEFAULT 'moderate' CHECK (severity IN ('mild', 'moderate', 'severe')),
  movements_to_avoid TEXT[] DEFAULT '{}',
  onset_date DATE,
  resolved BOOLEAN NOT NULL DEFAULT FALSE,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_exercises (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  muscle_group TEXT NOT NULL,
  movement_type TEXT NOT NULL CHECK (movement_type IN ('compound', 'isolation', 'cardio', 'flexibility')),
  equipment TEXT,
  instructions TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_workouts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  split_day TEXT,
  duration_minutes INTEGER,
  rating INTEGER CHECK (rating BETWEEN 1 AND 5),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tb_workout_sets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workout_id UUID NOT NULL REFERENCES tb_workouts(id) ON DELETE CASCADE,
  exercise_name TEXT NOT NULL,
  set_number INTEGER NOT NULL,
  weight_lbs NUMERIC(6,1),
  reps INTEGER,
  rpe NUMERIC(3,1) CHECK (rpe BETWEEN 1 AND 10),
  is_warmup BOOLEAN NOT NULL DEFAULT FALSE,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS tb_body_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  weight_lbs NUMERIC(5,1),
  body_fat_pct NUMERIC(4,1),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, date)
);

CREATE TABLE IF NOT EXISTS tb_personal_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  exercise_name TEXT NOT NULL,
  weight_pr_lbs NUMERIC(6,1),
  reps_at_pr INTEGER,
  estimated_1rm_lbs NUMERIC(6,1),
  achieved_date DATE NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tb_workouts_user_date ON tb_workouts(user_id, date DESC);
CREATE INDEX idx_tb_workout_sets_workout ON tb_workout_sets(workout_id);
CREATE INDEX idx_tb_body_metrics_user ON tb_body_metrics(user_id, date DESC);
CREATE INDEX idx_tb_personal_records_user ON tb_personal_records(user_id, exercise_name);

-- RLS (standard user_id pattern)
ALTER TABLE tb_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "tb_profiles_select" ON tb_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "tb_profiles_insert" ON tb_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "tb_profiles_update" ON tb_profiles FOR UPDATE USING (auth.uid() = user_id);

-- tb_exercises: shared lookup table, readable by all authenticated users
ALTER TABLE tb_exercises ENABLE ROW LEVEL SECURITY;
CREATE POLICY "tb_exercises_select" ON tb_exercises FOR SELECT USING (auth.role() = 'authenticated');

-- [Apply standard user_id RLS to: tb_injuries, tb_workouts, tb_body_metrics, tb_personal_records]
-- [Apply chain RLS for tb_workout_sets through tb_workouts.user_id]

CREATE TRIGGER tb_profiles_updated_at BEFORE UPDATE ON tb_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tb_workouts_updated_at BEFORE UPDATE ON tb_workouts FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tb_injuries_updated_at BEFORE UPDATE ON tb_injuries FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tb_personal_records_updated_at BEFORE UPDATE ON tb_personal_records FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Email Assistant (prefix: `ea`)

```sql
-- 00011_ea_tables.sql
CREATE TABLE IF NOT EXISTS ea_email_triage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  message_id TEXT NOT NULL,
  sender_email TEXT NOT NULL,
  sender_name TEXT,
  subject TEXT NOT NULL,
  summary TEXT,
  priority TEXT NOT NULL DEFAULT 'normal' CHECK (priority IN ('urgent', 'high', 'normal', 'low', 'spam')),
  category TEXT,
  action_needed TEXT,
  status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'triaged', 'actioned', 'archived')),
  received_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ea_email_drafts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  triage_id UUID REFERENCES ea_email_triage(id) ON DELETE SET NULL,
  to_address TEXT NOT NULL,
  subject TEXT NOT NULL,
  draft_body TEXT NOT NULL,
  tone_score NUMERIC(3,2),
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'reviewed', 'sent')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ea_vip_senders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  domain TEXT,
  label TEXT NOT NULL DEFAULT 'VIP',
  escalation TEXT DEFAULT 'notify' CHECK (escalation IN ('notify', 'urgent', 'auto-reply')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, email)
);

CREATE TABLE IF NOT EXISTS ea_email_digests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  digest_date DATE NOT NULL,
  total_received INTEGER NOT NULL DEFAULT 0,
  urgent_count INTEGER NOT NULL DEFAULT 0,
  triaged_count INTEGER NOT NULL DEFAULT 0,
  summary TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, digest_date)
);

-- Indexes
CREATE INDEX idx_ea_email_triage_user ON ea_email_triage(user_id, priority, created_at DESC);
CREATE INDEX idx_ea_email_triage_status ON ea_email_triage(user_id, status);
CREATE INDEX idx_ea_email_drafts_user ON ea_email_drafts(user_id, status);

-- RLS (standard user_id)
ALTER TABLE ea_email_triage ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ea_email_triage_select" ON ea_email_triage FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "ea_email_triage_insert" ON ea_email_triage FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "ea_email_triage_update" ON ea_email_triage FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "ea_email_triage_delete" ON ea_email_triage FOR DELETE USING (auth.uid() = user_id);

-- [Apply standard user_id RLS to: ea_email_drafts, ea_vip_senders, ea_email_digests]

CREATE TRIGGER ea_email_triage_updated_at BEFORE UPDATE ON ea_email_triage FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER ea_email_drafts_updated_at BEFORE UPDATE ON ea_email_drafts FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### HireMe Pro (prefix: `hm`)

```sql
-- 00012_hm_tables.sql
CREATE TABLE IF NOT EXISTS hm_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT NOT NULL,
  email TEXT,
  target_role TEXT,
  target_industries TEXT[] DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS hm_resumes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  version_label TEXT,
  json_content JSONB NOT NULL DEFAULT '{}',
  is_master BOOLEAN NOT NULL DEFAULT FALSE,
  file_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hm_applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  company TEXT NOT NULL,
  role TEXT NOT NULL,
  url TEXT,
  resume_id UUID REFERENCES hm_resumes(id) ON DELETE SET NULL,
  status TEXT NOT NULL DEFAULT 'wishlist' CHECK (status IN ('wishlist', 'applied', 'phone_screen', 'interview', 'offer', 'rejected', 'withdrawn')),
  date_applied DATE,
  salary_range TEXT,
  notes TEXT,
  contacts JSONB DEFAULT '[]',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hm_prep_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id UUID NOT NULL REFERENCES hm_applications(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  session_type TEXT NOT NULL DEFAULT 'behavioral' CHECK (session_type IN ('behavioral', 'technical', 'case', 'general')),
  questions JSONB DEFAULT '[]',
  mock_results JSONB DEFAULT '{}',
  score_pct INTEGER,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hm_activity_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  application_id UUID REFERENCES hm_applications(id) ON DELETE SET NULL,
  action TEXT NOT NULL,
  details JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_hm_applications_user ON hm_applications(user_id, status);
CREATE INDEX idx_hm_applications_date ON hm_applications(user_id, date_applied DESC);
CREATE INDEX idx_hm_activity_log_user ON hm_activity_log(user_id, created_at DESC);

-- RLS (standard user_id)
ALTER TABLE hm_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "hm_profiles_select" ON hm_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "hm_profiles_insert" ON hm_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "hm_profiles_update" ON hm_profiles FOR UPDATE USING (auth.uid() = user_id);

-- [Apply standard user_id RLS to all hm_ tables]

CREATE TRIGGER hm_profiles_updated_at BEFORE UPDATE ON hm_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER hm_resumes_updated_at BEFORE UPDATE ON hm_resumes FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER hm_applications_updated_at BEFORE UPDATE ON hm_applications FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Health Buddy Pro (prefix: `hb`)

```sql
-- 00013_hb_tables.sql
CREATE TABLE IF NOT EXISTS hb_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  calorie_target INTEGER,
  protein_target_g INTEGER,
  carbs_target_g INTEGER,
  fat_target_g INTEGER,
  hydration_target_oz INTEGER DEFAULT 64,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS hb_nutrition_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  meal_type TEXT NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
  description TEXT NOT NULL,
  calories INTEGER,
  protein_g NUMERIC(6,1),
  carbs_g NUMERIC(6,1),
  fat_g NUMERIC(6,1),
  fiber_g NUMERIC(5,1),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hb_hydration_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  amount_oz NUMERIC(5,1) NOT NULL,
  beverage_type TEXT DEFAULT 'water',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hb_supplement_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  supplement_name TEXT NOT NULL,
  dosage TEXT,
  taken BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hb_activity_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  activity TEXT NOT NULL,
  duration_minutes INTEGER NOT NULL,
  calories_burned INTEGER,
  intensity TEXT DEFAULT 'moderate' CHECK (intensity IN ('low', 'moderate', 'high', 'extreme')),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hb_custom_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  metric_name TEXT NOT NULL,
  value NUMERIC(10,2) NOT NULL,
  unit TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hb_daily_summaries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  total_calories INTEGER,
  total_protein_g NUMERIC(6,1),
  total_carbs_g NUMERIC(6,1),
  total_fat_g NUMERIC(6,1),
  total_water_oz NUMERIC(5,1),
  activity_minutes INTEGER,
  streak_days INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, date)
);

-- Indexes
CREATE INDEX idx_hb_nutrition_user_date ON hb_nutrition_entries(user_id, date DESC);
CREATE INDEX idx_hb_hydration_user_date ON hb_hydration_entries(user_id, date DESC);
CREATE INDEX idx_hb_daily_summaries_user ON hb_daily_summaries(user_id, date DESC);

-- RLS (standard user_id for all hb_ tables)
ALTER TABLE hb_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "hb_profiles_select" ON hb_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "hb_profiles_insert" ON hb_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "hb_profiles_update" ON hb_profiles FOR UPDATE USING (auth.uid() = user_id);

-- [Apply standard user_id RLS to all other hb_ tables]

CREATE TRIGGER hb_profiles_updated_at BEFORE UPDATE ON hb_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER hb_daily_summaries_updated_at BEFORE UPDATE ON hb_daily_summaries FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### NoteTaker Pro (prefix: `nt`)

```sql
-- 00014_nt_tables.sql
CREATE TABLE IF NOT EXISTS nt_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content_full TEXT,
  content_preview TEXT,
  category TEXT DEFAULT 'general',
  tags TEXT[] DEFAULT '{}',
  priority TEXT DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
  source_type TEXT DEFAULT 'manual' CHECK (source_type IN ('manual', 'voice', 'chat', 'import', 'web-clip')),
  is_pinned BOOLEAN NOT NULL DEFAULT FALSE,
  is_archived BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS nt_tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  tag_name TEXT NOT NULL,
  color TEXT,
  usage_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, tag_name)
);

CREATE TABLE IF NOT EXISTS nt_note_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  fields JSONB NOT NULL DEFAULT '[]',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_nt_notes_user ON nt_notes(user_id, updated_at DESC);
CREATE INDEX idx_nt_notes_tags ON nt_notes USING gin(tags);
CREATE INDEX idx_nt_notes_category ON nt_notes(user_id, category);
CREATE INDEX idx_nt_notes_search ON nt_notes USING gin(to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content_full, '')));

-- RLS (standard user_id)
ALTER TABLE nt_notes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "nt_notes_select" ON nt_notes FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "nt_notes_insert" ON nt_notes FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "nt_notes_update" ON nt_notes FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "nt_notes_delete" ON nt_notes FOR DELETE USING (auth.uid() = user_id);

ALTER TABLE nt_tags ENABLE ROW LEVEL SECURITY;
CREATE POLICY "nt_tags_select" ON nt_tags FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "nt_tags_insert" ON nt_tags FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "nt_tags_update" ON nt_tags FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "nt_tags_delete" ON nt_tags FOR DELETE USING (auth.uid() = user_id);

ALTER TABLE nt_note_templates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "nt_note_templates_select" ON nt_note_templates FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "nt_note_templates_insert" ON nt_note_templates FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "nt_note_templates_update" ON nt_note_templates FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "nt_note_templates_delete" ON nt_note_templates FOR DELETE USING (auth.uid() = user_id);

CREATE TRIGGER nt_notes_updated_at BEFORE UPDATE ON nt_notes FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER nt_note_templates_updated_at BEFORE UPDATE ON nt_note_templates FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Relationship Buddy (prefix: `rb`)

```sql
-- 00015_rb_tables.sql
CREATE TABLE IF NOT EXISTS rb_contacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  relationship TEXT,
  category TEXT DEFAULT 'friend' CHECK (category IN ('family', 'friend', 'colleague', 'acquaintance', 'mentor', 'other')),
  email TEXT,
  phone TEXT,
  photo_url TEXT,
  preferences JSONB DEFAULT '{}',
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rb_key_dates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  label TEXT NOT NULL,
  date DATE NOT NULL,
  is_annual BOOLEAN NOT NULL DEFAULT TRUE,
  remind_days_before INTEGER DEFAULT 7,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rb_interactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  interaction_date DATE NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('call', 'text', 'email', 'in_person', 'social', 'gift', 'other')),
  summary TEXT,
  sentiment TEXT CHECK (sentiment IN ('positive', 'neutral', 'negative')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rb_follow_ups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  action TEXT NOT NULL,
  due_date DATE,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'done', 'skipped')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rb_life_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  event_date DATE NOT NULL,
  description TEXT NOT NULL,
  category TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rb_gifts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  gift_date DATE NOT NULL,
  description TEXT NOT NULL,
  price_cents INTEGER,
  reaction TEXT,
  occasion TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rb_reminders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  type TEXT NOT NULL,
  trigger_date DATE NOT NULL,
  message TEXT,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'dismissed')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rb_health_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID NOT NULL REFERENCES rb_contacts(id) ON DELETE CASCADE,
  score INTEGER NOT NULL CHECK (score BETWEEN 0 AND 100),
  level TEXT NOT NULL CHECK (level IN ('thriving', 'healthy', 'neutral', 'fading', 'at_risk')),
  calculated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_rb_contacts_user ON rb_contacts(user_id);
CREATE INDEX idx_rb_interactions_contact ON rb_interactions(contact_id, interaction_date DESC);
CREATE INDEX idx_rb_follow_ups_user ON rb_follow_ups(user_id, status, due_date);
CREATE INDEX idx_rb_key_dates_date ON rb_key_dates(date);
CREATE INDEX idx_rb_reminders_user ON rb_reminders(user_id, status, trigger_date);

-- RLS
ALTER TABLE rb_contacts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "rb_contacts_select" ON rb_contacts FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "rb_contacts_insert" ON rb_contacts FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "rb_contacts_update" ON rb_contacts FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "rb_contacts_delete" ON rb_contacts FOR DELETE USING (auth.uid() = user_id);

-- Child tables with user_id: use direct user_id check
-- Child tables without user_id: chain through rb_contacts.user_id
ALTER TABLE rb_key_dates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "rb_key_dates_select" ON rb_key_dates FOR SELECT
  USING (contact_id IN (SELECT id FROM rb_contacts WHERE user_id = auth.uid()));
CREATE POLICY "rb_key_dates_insert" ON rb_key_dates FOR INSERT
  WITH CHECK (contact_id IN (SELECT id FROM rb_contacts WHERE user_id = auth.uid()));
CREATE POLICY "rb_key_dates_update" ON rb_key_dates FOR UPDATE
  USING (contact_id IN (SELECT id FROM rb_contacts WHERE user_id = auth.uid()));
CREATE POLICY "rb_key_dates_delete" ON rb_key_dates FOR DELETE
  USING (contact_id IN (SELECT id FROM rb_contacts WHERE user_id = auth.uid()));

-- [Apply user_id RLS to: rb_interactions, rb_follow_ups, rb_gifts, rb_reminders]
-- [Apply chain RLS through contact_id for: rb_life_events, rb_health_scores]

CREATE TRIGGER rb_contacts_updated_at BEFORE UPDATE ON rb_contacts FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER rb_follow_ups_updated_at BEFORE UPDATE ON rb_follow_ups FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER rb_reminders_updated_at BEFORE UPDATE ON rb_reminders FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Tutor Buddy Pro (prefix: `tu`)

```sql
-- 00016_tu_tables.sql
CREATE TABLE IF NOT EXISTS tu_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT,
  role TEXT DEFAULT 'student' CHECK (role IN ('student', 'parent', 'teacher')),
  grade_level TEXT,
  learning_style TEXT,
  subjects TEXT[] DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS tu_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  subject TEXT NOT NULL,
  topic TEXT NOT NULL,
  duration_minutes INTEGER,
  session_type TEXT DEFAULT 'tutoring' CHECK (session_type IN ('tutoring', 'quiz', 'review', 'practice')),
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tu_queries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES tu_sessions(id) ON DELETE CASCADE,
  raw_text TEXT NOT NULL,
  understanding_score INTEGER CHECK (understanding_score BETWEEN 1 AND 10),
  hint_levels_used INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tu_quiz_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  subject TEXT NOT NULL,
  topic TEXT NOT NULL,
  score_pct INTEGER NOT NULL CHECK (score_pct BETWEEN 0 AND 100),
  total_questions INTEGER,
  weak_areas TEXT[] DEFAULT '{}',
  strong_areas TEXT[] DEFAULT '{}',
  date DATE NOT NULL DEFAULT CURRENT_DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tu_mastery_tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  subject TEXT NOT NULL,
  topic_name TEXT NOT NULL,
  proficiency_pct INTEGER NOT NULL DEFAULT 0 CHECK (proficiency_pct BETWEEN 0 AND 100),
  trend TEXT DEFAULT 'stable' CHECK (trend IN ('improving', 'stable', 'declining')),
  last_assessed DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, subject, topic_name)
);

CREATE TABLE IF NOT EXISTS tu_study_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  plan_name TEXT NOT NULL,
  exam_date DATE,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'paused', 'abandoned')),
  plan_data JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tu_achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  achievement_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  unlocked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, achievement_id)
);

-- Indexes
CREATE INDEX idx_tu_sessions_user ON tu_sessions(user_id, date DESC);
CREATE INDEX idx_tu_quiz_results_user ON tu_quiz_results(user_id, date DESC);
CREATE INDEX idx_tu_mastery_user ON tu_mastery_tracking(user_id, subject);

-- RLS (standard user_id)
-- [Apply standard user_id RLS to all tu_ tables]
-- [Apply chain RLS for tu_queries through tu_sessions.user_id]

CREATE TRIGGER tu_profiles_updated_at BEFORE UPDATE ON tu_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tu_mastery_tracking_updated_at BEFORE UPDATE ON tu_mastery_tracking FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tu_study_plans_updated_at BEFORE UPDATE ON tu_study_plans FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Budget Buddy Pro (prefix: `bb`)

```sql
-- 00017_bb_tables.sql
-- NOTE: Budget Buddy originally had no database schema (JSON-only).
-- This schema was created for the unified dashboard.

CREATE TABLE IF NOT EXISTS bb_budgets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL DEFAULT 'Monthly Budget',
  framework TEXT DEFAULT '50-30-20' CHECK (framework IN ('50-30-20', 'zero-based', 'envelope', 'custom')),
  monthly_income_cents INTEGER NOT NULL DEFAULT 0,
  categories JSONB NOT NULL DEFAULT '[]',
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bb_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  vendor TEXT NOT NULL,
  category TEXT NOT NULL,
  subcategory TEXT,
  amount_cents INTEGER NOT NULL,
  type TEXT NOT NULL DEFAULT 'expense' CHECK (type IN ('income', 'expense', 'transfer')),
  account TEXT,
  tags TEXT[] DEFAULT '{}',
  notes TEXT,
  is_recurring BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bb_recurring (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  amount_cents INTEGER NOT NULL,
  type TEXT NOT NULL DEFAULT 'expense' CHECK (type IN ('income', 'expense')),
  category TEXT NOT NULL,
  frequency TEXT NOT NULL CHECK (frequency IN ('weekly', 'biweekly', 'monthly', 'quarterly', 'annual')),
  next_due DATE NOT NULL,
  auto_pay BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bb_savings_goals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  target_cents INTEGER NOT NULL,
  current_cents INTEGER NOT NULL DEFAULT 0,
  monthly_contribution_cents INTEGER DEFAULT 0,
  target_date DATE,
  color TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bb_net_worth_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  total_assets_cents BIGINT NOT NULL DEFAULT 0,
  total_liabilities_cents BIGINT NOT NULL DEFAULT 0,
  breakdown JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, date)
);

-- Indexes
CREATE INDEX idx_bb_transactions_user_date ON bb_transactions(user_id, date DESC);
CREATE INDEX idx_bb_transactions_category ON bb_transactions(user_id, category);
CREATE INDEX idx_bb_recurring_user ON bb_recurring(user_id, next_due);
CREATE INDEX idx_bb_net_worth_user ON bb_net_worth_snapshots(user_id, date DESC);

-- RLS (standard user_id for all bb_ tables)
-- [Apply standard user_id RLS to all bb_ tables]

CREATE TRIGGER bb_budgets_updated_at BEFORE UPDATE ON bb_budgets FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER bb_transactions_updated_at BEFORE UPDATE ON bb_transactions FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER bb_recurring_updated_at BEFORE UPDATE ON bb_recurring FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER bb_savings_goals_updated_at BEFORE UPDATE ON bb_savings_goals FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Plant Doctor (prefix: `pd`)

```sql
-- 00018_pd_tables.sql
CREATE TABLE IF NOT EXISTS pd_locations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  light_level TEXT DEFAULT 'medium' CHECK (light_level IN ('low', 'medium', 'bright_indirect', 'direct_sun')),
  humidity TEXT DEFAULT 'normal',
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pd_plants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  species TEXT,
  location_id UUID REFERENCES pd_locations(id) ON DELETE SET NULL,
  image_url TEXT,
  acquired_date DATE,
  status TEXT DEFAULT 'healthy' CHECK (status IN ('healthy', 'needs_attention', 'sick', 'dormant', 'deceased')),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pd_care_schedules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID NOT NULL REFERENCES pd_plants(id) ON DELETE CASCADE,
  action_type TEXT NOT NULL CHECK (action_type IN ('water', 'fertilize', 'repot', 'prune', 'mist', 'rotate', 'inspect')),
  frequency_days INTEGER NOT NULL,
  next_due DATE NOT NULL,
  last_done DATE,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pd_health_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plant_id UUID NOT NULL REFERENCES pd_plants(id) ON DELETE CASCADE,
  log_date DATE NOT NULL DEFAULT CURRENT_DATE,
  diagnosis TEXT,
  symptoms TEXT[] DEFAULT '{}',
  treatment_applied TEXT,
  image_url TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_pd_plants_user ON pd_plants(user_id);
CREATE INDEX idx_pd_care_schedules_due ON pd_care_schedules(next_due);
CREATE INDEX idx_pd_health_logs_plant ON pd_health_logs(plant_id, log_date DESC);

-- RLS
ALTER TABLE pd_locations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "pd_locations_select" ON pd_locations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "pd_locations_insert" ON pd_locations FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "pd_locations_update" ON pd_locations FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "pd_locations_delete" ON pd_locations FOR DELETE USING (auth.uid() = user_id);

ALTER TABLE pd_plants ENABLE ROW LEVEL SECURITY;
CREATE POLICY "pd_plants_select" ON pd_plants FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "pd_plants_insert" ON pd_plants FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "pd_plants_update" ON pd_plants FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "pd_plants_delete" ON pd_plants FOR DELETE USING (auth.uid() = user_id);

-- pd_care_schedules and pd_health_logs: chain through pd_plants.user_id
ALTER TABLE pd_care_schedules ENABLE ROW LEVEL SECURITY;
CREATE POLICY "pd_care_schedules_select" ON pd_care_schedules FOR SELECT
  USING (plant_id IN (SELECT id FROM pd_plants WHERE user_id = auth.uid()));
CREATE POLICY "pd_care_schedules_insert" ON pd_care_schedules FOR INSERT
  WITH CHECK (plant_id IN (SELECT id FROM pd_plants WHERE user_id = auth.uid()));
CREATE POLICY "pd_care_schedules_update" ON pd_care_schedules FOR UPDATE
  USING (plant_id IN (SELECT id FROM pd_plants WHERE user_id = auth.uid()));
CREATE POLICY "pd_care_schedules_delete" ON pd_care_schedules FOR DELETE
  USING (plant_id IN (SELECT id FROM pd_plants WHERE user_id = auth.uid()));

-- [Apply same chain RLS for pd_health_logs]

CREATE TRIGGER pd_locations_updated_at BEFORE UPDATE ON pd_locations FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER pd_plants_updated_at BEFORE UPDATE ON pd_plants FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER pd_care_schedules_updated_at BEFORE UPDATE ON pd_care_schedules FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### DocuScan (prefix: `ds`)

```sql
-- 00019_ds_tables.sql
CREATE TABLE IF NOT EXISTS ds_scans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  document_type TEXT DEFAULT 'other' CHECK (document_type IN ('receipt', 'contract', 'letter', 'form', 'id', 'medical', 'tax', 'other')),
  extracted_markdown TEXT,
  extracted_text TEXT,
  ai_summary TEXT,
  pdf_path TEXT,
  storage_path TEXT,
  tags JSONB DEFAULT '[]',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ds_scans_user ON ds_scans(user_id, created_at DESC);
CREATE INDEX idx_ds_scans_type ON ds_scans(user_id, document_type);
CREATE INDEX idx_ds_scans_search ON ds_scans USING gin(to_tsvector('english', coalesce(extracted_text, '') || ' ' || coalesce(ai_summary, '')));

ALTER TABLE ds_scans ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ds_scans_select" ON ds_scans FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "ds_scans_insert" ON ds_scans FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "ds_scans_update" ON ds_scans FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "ds_scans_delete" ON ds_scans FOR DELETE USING (auth.uid() = user_id);

CREATE TRIGGER ds_scans_updated_at BEFORE UPDATE ON ds_scans FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Home Fix-It (prefix: `hf`)

```sql
-- 00020_hf_tables.sql
CREATE TABLE IF NOT EXISTS hf_home_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  home_type TEXT DEFAULT 'house' CHECK (home_type IN ('house', 'apartment', 'condo', 'townhouse', 'other')),
  year_built INTEGER,
  sqft INTEGER,
  skill_level TEXT DEFAULT 'intermediate' CHECK (skill_level IN ('beginner', 'intermediate', 'advanced')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS hf_tool_inventory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  tool_name TEXT NOT NULL,
  category TEXT NOT NULL,
  has_tool BOOLEAN NOT NULL DEFAULT FALSE,
  brand TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hf_appliances (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  appliance_type TEXT NOT NULL,
  brand TEXT,
  model_number TEXT,
  serial_number TEXT,
  purchase_date DATE,
  warranty_expiry DATE,
  manual_url TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hf_repair_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  appliance_id UUID REFERENCES hf_appliances(id) ON DELETE SET NULL,
  issue_title TEXT NOT NULL,
  category TEXT NOT NULL,
  description TEXT,
  diy_cost_cents INTEGER,
  pro_quote_cents INTEGER,
  actual_cost_cents INTEGER,
  approach TEXT CHECK (approach IN ('diy', 'professional', 'pending')),
  status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'completed', 'deferred')),
  completed_date DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hf_maintenance_tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  task_name TEXT NOT NULL,
  category TEXT NOT NULL,
  frequency_days INTEGER NOT NULL,
  next_due DATE NOT NULL,
  last_completed DATE,
  difficulty TEXT DEFAULT 'easy' CHECK (difficulty IN ('easy', 'moderate', 'hard')),
  estimated_minutes INTEGER,
  status TEXT NOT NULL DEFAULT 'upcoming' CHECK (status IN ('upcoming', 'overdue', 'completed')),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_hf_repair_logs_user ON hf_repair_logs(user_id, status);
CREATE INDEX idx_hf_maintenance_tasks_due ON hf_maintenance_tasks(user_id, next_due);

-- RLS (standard user_id for all hf_ tables)
-- [Apply standard user_id RLS to all hf_ tables]

CREATE TRIGGER hf_home_profiles_updated_at BEFORE UPDATE ON hf_home_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER hf_appliances_updated_at BEFORE UPDATE ON hf_appliances FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER hf_repair_logs_updated_at BEFORE UPDATE ON hf_repair_logs FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER hf_maintenance_tasks_updated_at BEFORE UPDATE ON hf_maintenance_tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### InvoiceGen (prefix: `ig`)

```sql
-- 00021_ig_tables.sql
CREATE TABLE IF NOT EXISTS ig_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  business_name TEXT NOT NULL,
  email TEXT,
  address TEXT,
  phone TEXT,
  logo_url TEXT,
  brand_color TEXT DEFAULT '#14b8a6',
  payment_details JSONB DEFAULT '{}',
  default_terms_days INTEGER DEFAULT 30,
  invoice_prefix TEXT DEFAULT 'INV',
  next_invoice_number INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS ig_clients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  email TEXT,
  company TEXT,
  address TEXT,
  default_terms_days INTEGER,
  currency TEXT DEFAULT 'USD',
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ig_invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  client_id UUID NOT NULL REFERENCES ig_clients(id) ON DELETE RESTRICT,
  invoice_number TEXT NOT NULL,
  issue_date DATE NOT NULL DEFAULT CURRENT_DATE,
  due_date DATE NOT NULL,
  subtotal_cents INTEGER NOT NULL DEFAULT 0,
  tax_rate NUMERIC(5,2) DEFAULT 0,
  tax_cents INTEGER NOT NULL DEFAULT 0,
  total_cents INTEGER NOT NULL DEFAULT 0,
  currency TEXT DEFAULT 'USD',
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'sent', 'viewed', 'paid', 'overdue', 'cancelled')),
  notes TEXT,
  pdf_url TEXT,
  paid_date DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ig_line_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES ig_invoices(id) ON DELETE CASCADE,
  description TEXT NOT NULL,
  quantity NUMERIC(10,2) NOT NULL DEFAULT 1,
  rate_cents INTEGER NOT NULL,
  amount_cents INTEGER NOT NULL,
  sort_order INTEGER DEFAULT 0
);

-- Indexes
CREATE INDEX idx_ig_invoices_user ON ig_invoices(user_id, status);
CREATE INDEX idx_ig_invoices_client ON ig_invoices(client_id);
CREATE INDEX idx_ig_invoices_date ON ig_invoices(user_id, issue_date DESC);
CREATE INDEX idx_ig_clients_user ON ig_clients(user_id);

-- RLS (standard user_id)
ALTER TABLE ig_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ig_profiles_select" ON ig_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "ig_profiles_insert" ON ig_profiles FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "ig_profiles_update" ON ig_profiles FOR UPDATE USING (auth.uid() = user_id);

ALTER TABLE ig_clients ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ig_clients_select" ON ig_clients FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "ig_clients_insert" ON ig_clients FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "ig_clients_update" ON ig_clients FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "ig_clients_delete" ON ig_clients FOR DELETE USING (auth.uid() = user_id);

ALTER TABLE ig_invoices ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ig_invoices_select" ON ig_invoices FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "ig_invoices_insert" ON ig_invoices FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "ig_invoices_update" ON ig_invoices FOR UPDATE USING (auth.uid() = user_id);

-- ig_line_items: chain through ig_invoices.user_id
ALTER TABLE ig_line_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ig_line_items_select" ON ig_line_items FOR SELECT
  USING (invoice_id IN (SELECT id FROM ig_invoices WHERE user_id = auth.uid()));
CREATE POLICY "ig_line_items_insert" ON ig_line_items FOR INSERT
  WITH CHECK (invoice_id IN (SELECT id FROM ig_invoices WHERE user_id = auth.uid()));
CREATE POLICY "ig_line_items_update" ON ig_line_items FOR UPDATE
  USING (invoice_id IN (SELECT id FROM ig_invoices WHERE user_id = auth.uid()));
CREATE POLICY "ig_line_items_delete" ON ig_line_items FOR DELETE
  USING (invoice_id IN (SELECT id FROM ig_invoices WHERE user_id = auth.uid()));

CREATE TRIGGER ig_profiles_updated_at BEFORE UPDATE ON ig_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER ig_clients_updated_at BEFORE UPDATE ON ig_clients FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER ig_invoices_updated_at BEFORE UPDATE ON ig_invoices FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

---

## 6. Shared Component Library

All shared components live in `components/shared/`. They use the NormieClaw design tokens exclusively.

### 6.1 StatCard

```tsx
// components/shared/stat-card.tsx
'use client'

import { cn } from '@/lib/utils/cn'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface StatCardProps {
  /** The metric value to display prominently. */
  value: string | number
  /** Label below the value. */
  label: string
  /** Trend: positive number = up, negative = down, 0 or undefined = neutral. */
  trend?: number
  /** Trend label text (e.g., "vs last month"). */
  trendLabel?: string
  /** Lucide icon component to render. */
  icon?: React.ReactNode
  /** Accent color: 'teal' | 'orange' | 'blue' | 'green' | 'red' | 'yellow'. Default: 'teal'. */
  color?: 'teal' | 'orange' | 'blue' | 'green' | 'red' | 'yellow'
  /** Optional click handler. */
  onClick?: () => void
  className?: string
}

const colorMap = {
  teal: { bg: 'bg-teal-500/10', text: 'text-teal-400', border: 'border-teal-500/20' },
  orange: { bg: 'bg-orange-500/10', text: 'text-orange-400', border: 'border-orange-500/20' },
  blue: { bg: 'bg-blue-500/10', text: 'text-blue-400', border: 'border-blue-500/20' },
  green: { bg: 'bg-green-500/10', text: 'text-green-400', border: 'border-green-500/20' },
  red: { bg: 'bg-red-500/10', text: 'text-red-400', border: 'border-red-500/20' },
  yellow: { bg: 'bg-yellow-500/10', text: 'text-yellow-400', border: 'border-yellow-500/20' },
}

export function StatCard({
  value,
  label,
  trend,
  trendLabel,
  icon,
  color = 'teal',
  onClick,
  className,
}: StatCardProps) {
  const colors = colorMap[color]
  const TrendIcon = trend && trend > 0 ? TrendingUp : trend && trend < 0 ? TrendingDown : Minus

  return (
    <div
      className={cn(
        'relative rounded-lg border border-soft bg-surface-1 p-lg noise-overlay',
        'transition-all duration-200',
        onClick && 'cursor-pointer hover:border-strong hover:shadow-card',
        className
      )}
      onClick={onClick}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-caption text-text-3 uppercase tracking-wider">{label}</p>
          <p className="mt-xs text-h1 font-mono font-bold text-text-1">{value}</p>
          {trend !== undefined && (
            <div className="mt-sm flex items-center gap-xs">
              <TrendIcon size={14} className={trend > 0 ? 'text-green-400' : trend < 0 ? 'text-red-400' : 'text-text-3'} />
              <span className={cn('text-caption font-mono', trend > 0 ? 'text-green-400' : trend < 0 ? 'text-red-400' : 'text-text-3')}>
                {trend > 0 ? '+' : ''}{trend}%
              </span>
              {trendLabel && <span className="text-caption text-text-3">{trendLabel}</span>}
            </div>
          )}
        </div>
        {icon && (
          <div className={cn('flex h-10 w-10 items-center justify-center rounded-lg', colors.bg, colors.text)}>
            {icon}
          </div>
        )}
      </div>
    </div>
  )
}
```

### 6.2 DataTable

```tsx
// components/shared/data-table.tsx
'use client'

import { useState, useMemo } from 'react'
import { cn } from '@/lib/utils/cn'
import { ChevronUp, ChevronDown, ChevronsUpDown, ChevronLeft, ChevronRight } from 'lucide-react'

interface Column<T> {
  /** Unique column key (maps to data field). */
  key: string
  /** Display header. */
  header: string
  /** Custom render function. */
  render?: (row: T) => React.ReactNode
  /** Enable sorting. Default: true. */
  sortable?: boolean
  /** Column width class. e.g. 'w-32', 'w-48', 'flex-1'. */
  width?: string
  /** Text alignment. Default: 'left'. */
  align?: 'left' | 'center' | 'right'
}

interface DataTableProps<T> {
  columns: Column<T>[]
  data: T[]
  /** Unique key for each row. */
  rowKey: keyof T | ((row: T) => string)
  /** Rows per page. Default: 10. */
  pageSize?: number
  /** Enable search filter. Default: true. */
  searchable?: boolean
  /** Search placeholder. */
  searchPlaceholder?: string
  /** Columns to search across (by key). Default: all. */
  searchColumns?: string[]
  /** Called when a row is clicked. */
  onRowClick?: (row: T) => void
  /** Empty state message. */
  emptyMessage?: string
  /** Actions slot (rendered above the table, right side). */
  actions?: React.ReactNode
  className?: string
}

export function DataTable<T extends Record<string, any>>({
  columns,
  data,
  rowKey,
  pageSize = 10,
  searchable = true,
  searchPlaceholder = 'Search...',
  searchColumns,
  onRowClick,
  emptyMessage = 'No data found',
  actions,
  className,
}: DataTableProps<T>) {
  const [search, setSearch] = useState('')
  const [sortKey, setSortKey] = useState<string | null>(null)
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc')
  const [page, setPage] = useState(0)

  const getRowKey = (row: T) =>
    typeof rowKey === 'function' ? rowKey(row) : String(row[rowKey])

  const filteredData = useMemo(() => {
    if (!search) return data
    const lower = search.toLowerCase()
    const cols = searchColumns || columns.map(c => c.key)
    return data.filter(row =>
      cols.some(col => String(row[col] ?? '').toLowerCase().includes(lower))
    )
  }, [data, search, searchColumns, columns])

  const sortedData = useMemo(() => {
    if (!sortKey) return filteredData
    return [...filteredData].sort((a, b) => {
      const aVal = a[sortKey]
      const bVal = b[sortKey]
      if (aVal == null) return 1
      if (bVal == null) return -1
      const cmp = aVal < bVal ? -1 : aVal > bVal ? 1 : 0
      return sortDir === 'asc' ? cmp : -cmp
    })
  }, [filteredData, sortKey, sortDir])

  const totalPages = Math.ceil(sortedData.length / pageSize)
  const pagedData = sortedData.slice(page * pageSize, (page + 1) * pageSize)

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortDir(d => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortKey(key)
      setSortDir('asc')
    }
  }

  return (
    <div className={cn('rounded-lg border border-soft bg-surface-1 noise-overlay', className)}>
      {/* Toolbar */}
      {(searchable || actions) && (
        <div className="flex items-center justify-between border-b border-soft px-md py-sm">
          {searchable && (
            <input
              type="text"
              value={search}
              onChange={e => { setSearch(e.target.value); setPage(0) }}
              placeholder={searchPlaceholder}
              className="w-64 rounded-md border border-soft bg-surface-2 px-3 py-1.5 text-body-sm text-text-1 placeholder:text-text-3 focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500/30"
            />
          )}
          {actions && <div className="flex items-center gap-sm">{actions}</div>}
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-soft">
              {columns.map(col => (
                <th
                  key={col.key}
                  className={cn(
                    'px-md py-sm text-caption font-medium uppercase tracking-wider text-text-3',
                    col.width,
                    col.align === 'center' && 'text-center',
                    col.align === 'right' && 'text-right',
                    col.sortable !== false && 'cursor-pointer select-none hover:text-text-2'
                  )}
                  onClick={() => col.sortable !== false && handleSort(col.key)}
                >
                  <div className={cn('flex items-center gap-xs', col.align === 'right' && 'justify-end')}>
                    {col.header}
                    {col.sortable !== false && (
                      sortKey === col.key
                        ? sortDir === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                        : <ChevronsUpDown size={14} className="opacity-30" />
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {pagedData.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="px-md py-xl text-center text-text-3">
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              pagedData.map(row => (
                <tr
                  key={getRowKey(row)}
                  className={cn(
                    'border-b border-soft last:border-0 transition-colors',
                    onRowClick && 'cursor-pointer hover:bg-surface-2'
                  )}
                  onClick={() => onRowClick?.(row)}
                >
                  {columns.map(col => (
                    <td
                      key={col.key}
                      className={cn(
                        'px-md py-sm text-body-sm text-text-2',
                        col.align === 'center' && 'text-center',
                        col.align === 'right' && 'text-right font-mono'
                      )}
                    >
                      {col.render ? col.render(row) : String(row[col.key] ?? '')}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between border-t border-soft px-md py-sm">
          <span className="text-caption text-text-3">
            {sortedData.length} result{sortedData.length !== 1 ? 's' : ''} · Page {page + 1} of {totalPages}
          </span>
          <div className="flex items-center gap-xs">
            <button
              onClick={() => setPage(p => Math.max(0, p - 1))}
              disabled={page === 0}
              className="p-1 rounded-md hover:bg-surface-2 disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <ChevronLeft size={16} />
            </button>
            <button
              onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
              disabled={page >= totalPages - 1}
              className="p-1 rounded-md hover:bg-surface-2 disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
```

### 6.3 Charts (Recharts Wrappers)

```tsx
// components/shared/charts/line-chart.tsx
'use client'

import { ResponsiveContainer, LineChart as RechartsLine, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

interface LineChartProps {
  /** Array of data points. Each object has the x-axis key + one or more series keys. */
  data: Record<string, any>[]
  /** X-axis data key. */
  xKey: string
  /** Series definitions. */
  series: {
    key: string
    label: string
    color: string
    strokeWidth?: number
    dashed?: boolean
  }[]
  /** Chart height in pixels. Default: 300. */
  height?: number
  /** Show grid lines. Default: true. */
  showGrid?: boolean
  /** Show legend. Default: true. */
  showLegend?: boolean
  /** Custom tooltip formatter. */
  tooltipFormatter?: (value: number, name: string) => string
  className?: string
}

const chartTheme = {
  grid: '#ffffff0d',
  axis: '#c9d0e09e',
  tooltip: {
    bg: '#101826',
    border: '#ffffff29',
    text: '#f6f7fb',
  },
}

export function LineChart({
  data,
  xKey,
  series,
  height = 300,
  showGrid = true,
  showLegend = true,
  tooltipFormatter,
  className,
}: LineChartProps) {
  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={height}>
        <RechartsLine data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
          {showGrid && <CartesianGrid stroke={chartTheme.grid} strokeDasharray="3 3" />}
          <XAxis
            dataKey={xKey}
            stroke={chartTheme.axis}
            tick={{ fill: chartTheme.axis, fontSize: 12, fontFamily: 'JetBrains Mono' }}
            tickLine={false}
            axisLine={{ stroke: chartTheme.grid }}
          />
          <YAxis
            stroke={chartTheme.axis}
            tick={{ fill: chartTheme.axis, fontSize: 12, fontFamily: 'JetBrains Mono' }}
            tickLine={false}
            axisLine={false}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: chartTheme.tooltip.bg,
              border: `1px solid ${chartTheme.tooltip.border}`,
              borderRadius: '8px',
              color: chartTheme.tooltip.text,
              fontFamily: 'JetBrains Mono',
              fontSize: '13px',
            }}
            formatter={tooltipFormatter}
          />
          {showLegend && (
            <Legend
              wrapperStyle={{ fontFamily: 'Manrope', fontSize: '13px', color: chartTheme.axis }}
            />
          )}
          {series.map(s => (
            <Line
              key={s.key}
              type="monotone"
              dataKey={s.key}
              name={s.label}
              stroke={s.color}
              strokeWidth={s.strokeWidth ?? 2}
              strokeDasharray={s.dashed ? '5 5' : undefined}
              dot={false}
              activeDot={{ r: 4, fill: s.color }}
            />
          ))}
        </RechartsLine>
      </ResponsiveContainer>
    </div>
  )
}
```

```tsx
// components/shared/charts/bar-chart.tsx
'use client'

import { ResponsiveContainer, BarChart as RechartsBar, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

interface BarChartProps {
  data: Record<string, any>[]
  xKey: string
  series: {
    key: string
    label: string
    color: string
    stackId?: string
  }[]
  height?: number
  showGrid?: boolean
  showLegend?: boolean
  /** Bar corner radius. Default: 4. */
  barRadius?: number
  tooltipFormatter?: (value: number, name: string) => string
  className?: string
}

export function BarChart({
  data, xKey, series, height = 300, showGrid = true, showLegend = true,
  barRadius = 4, tooltipFormatter, className,
}: BarChartProps) {
  // Same pattern as LineChart with <Bar> elements instead of <Line>
  // Use radius={[barRadius, barRadius, 0, 0]} for top rounding
  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={height}>
        <RechartsBar data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
          {showGrid && <CartesianGrid stroke="#ffffff0d" strokeDasharray="3 3" />}
          <XAxis dataKey={xKey} stroke="#c9d0e09e" tick={{ fill: '#c9d0e09e', fontSize: 12, fontFamily: 'JetBrains Mono' }} tickLine={false} />
          <YAxis stroke="#c9d0e09e" tick={{ fill: '#c9d0e09e', fontSize: 12, fontFamily: 'JetBrains Mono' }} tickLine={false} axisLine={false} />
          <Tooltip contentStyle={{ backgroundColor: '#101826', border: '1px solid #ffffff29', borderRadius: '8px', color: '#f6f7fb', fontFamily: 'JetBrains Mono', fontSize: '13px' }} formatter={tooltipFormatter} />
          {showLegend && <Legend wrapperStyle={{ fontFamily: 'Manrope', fontSize: '13px' }} />}
          {series.map(s => (
            <Bar key={s.key} dataKey={s.key} name={s.label} fill={s.color} stackId={s.stackId} radius={[barRadius, barRadius, 0, 0]} />
          ))}
        </RechartsBar>
      </ResponsiveContainer>
    </div>
  )
}
```

```tsx
// components/shared/charts/donut-chart.tsx
'use client'

import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'

interface DonutChartProps {
  data: { name: string; value: number; color: string }[]
  height?: number
  /** Inner radius percentage. Default: 60. */
  innerRadius?: number
  /** Outer radius percentage. Default: 80. */
  outerRadius?: number
  /** Show labels on segments. Default: false. */
  showLabels?: boolean
  showLegend?: boolean
  /** Center text (e.g., total value). */
  centerLabel?: string
  centerValue?: string
  className?: string
}

export function DonutChart({
  data, height = 300, innerRadius = 60, outerRadius = 80,
  showLabels = false, showLegend = true, centerLabel, centerValue, className,
}: DonutChartProps) {
  return (
    <div className={cn('relative', className)}>
      <ResponsiveContainer width="100%" height={height}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={`${innerRadius}%`}
            outerRadius={`${outerRadius}%`}
            dataKey="value"
            stroke="none"
            label={showLabels ? ({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%` : undefined}
          >
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip contentStyle={{ backgroundColor: '#101826', border: '1px solid #ffffff29', borderRadius: '8px', color: '#f6f7fb', fontFamily: 'JetBrains Mono', fontSize: '13px' }} />
          {showLegend && <Legend wrapperStyle={{ fontFamily: 'Manrope', fontSize: '13px' }} />}
        </PieChart>
      </ResponsiveContainer>
      {(centerLabel || centerValue) && (
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          {centerValue && <span className="text-h2 font-mono font-bold text-text-1">{centerValue}</span>}
          {centerLabel && <span className="text-caption text-text-3">{centerLabel}</span>}
        </div>
      )}
    </div>
  )
}
```

### 6.4 KanbanBoard

```tsx
// components/shared/kanban-board.tsx
'use client'

import { DndContext, closestCenter, PointerSensor, useSensor, useSensors, DragEndEvent } from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'

interface KanbanColumn<T> {
  id: string
  title: string
  color: string    // Hex color for column header accent
  items: T[]
}

interface KanbanBoardProps<T> {
  columns: KanbanColumn<T>[]
  /** Unique key extractor for items. */
  itemKey: (item: T) => string
  /** Render function for each card. */
  renderCard: (item: T) => React.ReactNode
  /** Called when an item is moved. */
  onMove: (itemId: string, fromColumn: string, toColumn: string, newIndex: number) => void
  className?: string
}

export function KanbanBoard<T>({ columns, itemKey, renderCard, onMove, className }: KanbanBoardProps<T>) {
  const sensors = useSensors(useSensor(PointerSensor, { activationConstraint: { distance: 5 } }))

  // Implementation: Each column is a droppable zone.
  // Each card is a draggable + sortable item.
  // onDragEnd calls onMove with the item ID, source column, target column, and new index.

  return (
    <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
      <div className={cn('flex gap-md overflow-x-auto pb-sm', className)}>
        {columns.map(col => (
          <div key={col.id} className="flex-shrink-0 w-72">
            {/* Column header */}
            <div className="flex items-center gap-sm mb-sm px-sm">
              <div className="h-2 w-2 rounded-full" style={{ backgroundColor: col.color }} />
              <span className="text-body-sm font-semibold text-text-1">{col.title}</span>
              <span className="text-caption text-text-3 font-mono">{col.items.length}</span>
            </div>
            {/* Cards */}
            <SortableContext items={col.items.map(itemKey)} strategy={verticalListSortingStrategy}>
              <div className="flex flex-col gap-sm min-h-[200px] rounded-lg bg-surface-2 p-sm">
                {col.items.map(item => (
                  <SortableCard key={itemKey(item)} id={itemKey(item)}>
                    {renderCard(item)}
                  </SortableCard>
                ))}
              </div>
            </SortableContext>
          </div>
        ))}
      </div>
    </DndContext>
  )
}
```

### 6.5 Remaining Shared Components (API Signatures)

```tsx
// components/shared/calendar-view.tsx
interface CalendarViewProps {
  events: { date: string; title: string; color?: string; onClick?: () => void }[]
  onDateClick?: (date: string) => void
  /** Initial month (YYYY-MM). Default: current month. */
  initialMonth?: string
  className?: string
}

// components/shared/timeline.tsx
interface TimelineProps {
  items: {
    id: string
    date: string            // ISO date string
    title: string
    description?: string
    icon?: React.ReactNode
    color?: string          // Dot color
  }[]
  /** Max items to show before "Show more". Default: 10. */
  maxItems?: number
  className?: string
}

// components/shared/card-grid.tsx
interface CardGridProps<T> {
  items: T[]
  itemKey: (item: T) => string
  renderCard: (item: T) => React.ReactNode
  /** Grid columns at each breakpoint. Default: { sm: 1, md: 2, lg: 3, xl: 4 }. */
  columns?: { sm?: number; md?: number; lg?: number; xl?: number }
  className?: string
}

// components/shared/empty-state.tsx
interface EmptyStateProps {
  icon: React.ReactNode
  title: string
  message: string
  action?: { label: string; onClick: () => void }
  className?: string
}

// components/shared/page-header.tsx
interface PageHeaderProps {
  title: string
  description?: string
  /** Breadcrumbs array. Auto-generated from registry if omitted. */
  breadcrumbs?: { label: string; href?: string }[]
  /** Action buttons rendered on the right. */
  actions?: React.ReactNode
  className?: string
}

// components/shared/search-bar.tsx
interface SearchBarProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  /** Debounce delay in ms. Default: 300. */
  debounceMs?: number
  /** Filter chips. */
  filters?: { key: string; label: string; active: boolean; onToggle: () => void }[]
  className?: string
}

// components/shared/progress-ring.tsx
interface ProgressRingProps {
  /** Progress percentage (0-100). */
  value: number
  /** Ring diameter in pixels. Default: 80. */
  size?: number
  /** Ring stroke width. Default: 8. */
  strokeWidth?: number
  /** Ring color. Default: teal-500. */
  color?: string
  /** Background ring color. Default: surface-2. */
  trackColor?: string
  /** Center text. Default: value%. */
  label?: string
  className?: string
}

// components/shared/progress-bar.tsx
interface ProgressBarProps {
  value: number            // 0-100
  color?: string           // Tailwind color class
  height?: number          // px, default 8
  showLabel?: boolean      // Show percentage text
  thresholds?: { value: number; color: string }[]  // Color changes at thresholds
  className?: string
}

// components/shared/badge-pill.tsx
interface BadgePillProps {
  label: string
  variant?: 'default' | 'teal' | 'orange' | 'success' | 'error' | 'warning'
  size?: 'sm' | 'md'
  removable?: boolean
  onRemove?: () => void
  className?: string
}

// components/shared/detail-modal.tsx
interface DetailModalProps {
  open: boolean
  onClose: () => void
  title: string
  /** Width: 'sm' (480px) | 'md' (640px) | 'lg' (800px) | 'xl' (1024px). Default: 'md'. */
  size?: 'sm' | 'md' | 'lg' | 'xl'
  children: React.ReactNode
  /** Footer actions (Save, Cancel buttons). */
  footer?: React.ReactNode
}

// components/shared/checklist.tsx
interface ChecklistProps {
  items: { id: string; label: string; checked: boolean }[]
  onToggle: (id: string, checked: boolean) => void
  /** Allow adding new items. */
  addable?: boolean
  onAdd?: (label: string) => void
  className?: string
}

// components/shared/heatmap.tsx
interface HeatmapProps {
  /** Array of { date: 'YYYY-MM-DD', value: number }. */
  data: { date: string; value: number }[]
  /** Color scale from low to high. Default: ['#ffffff0d', '#14b8a6']. */
  colorScale?: [string, string]
  /** Number of weeks to show. Default: 52. */
  weeks?: number
  className?: string
}

// components/shared/tag-cloud.tsx
interface TagCloudProps {
  tags: { name: string; count: number; color?: string }[]
  onClick?: (tag: string) => void
  className?: string
}

// components/shared/loading-skeleton.tsx
interface LoadingSkeletonProps {
  /** Skeleton variant. */
  variant: 'card' | 'table' | 'stat' | 'chart' | 'text'
  /** Number of skeleton items. Default: 1. */
  count?: number
  className?: string
}
```

---

## 7. Data Sync Strategy

### 7.1 Overview

Data flows from agent → database → dashboard. Three sync modes are supported per-skill:

```
Mode 1: DIRECT                    Mode 2: JSON BRIDGE              Mode 3: WEBHOOK
┌──────┐   Supabase   ┌──────┐   ┌──────┐  JSON  ┌──────┐  DB   ┌──────┐   ┌──────┐  POST  ┌─────┐  DB   ┌──────┐
│Agent │ ──REST API──▶ │  DB  │   │Agent │ ─file─▶│Sync  │ ───▶ │  DB  │   │Agent │ ─────▶│ API │ ───▶ │  DB  │
└──────┘               └──────┘   └──────┘        │Script│       └──────┘   └──────┘       │Route│       └──────┘
    ▲                     │           ▲            └──────┘          │           ▲           └─────┘          │
    │                     ▼           │               ▲              ▼           │              ▲             ▼
    │               ┌──────────┐      │               │        ┌──────────┐     │              │        ┌──────────┐
    │               │Dashboard │      │           watches      │Dashboard │     │          Realtime     │Dashboard │
    │               └──────────┘      │           for changes  └──────────┘     │          subscription └──────────┘
    │                                 │                                         │
    └─── Realtime subscription ───────┘                                         └─── Realtime subscription ───┘
```

### 7.2 Mode 1: Direct Supabase (Recommended)

The agent writes directly to Supabase using the REST API with the service role key.

```bash
# Example: Agent creates an expense
curl -X POST "$SUPABASE_URL/rest/v1/exp_expenses" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "USER_UUID",
    "date": "2026-03-08",
    "vendor": "Whole Foods",
    "category": "Groceries",
    "amount_cents": 4750,
    "status": "logged"
  }'
```

### 7.3 Mode 2: JSON → Supabase Bridge

For skills that write local JSON files, a sync script watches for changes and upserts to Supabase.

```typescript
// lib/sync/json-bridge.ts

interface SyncConfig {
  skillId: string
  sourceDir: string          // Relative to skill data directory
  tableMappings: {
    sourceFile: string       // JSON filename (e.g., 'expenses.json')
    targetTable: string      // Supabase table (e.g., 'exp_expenses')
    transform: (raw: any) => Record<string, any>  // Transform each item
    upsertKey: string[]      // Columns for upsert conflict resolution
  }[]
}

// Usage in a sync script:
// node scripts/sync.ts --skill expense-report
```

### 7.4 Mode 3: Webhook Ingestion

Skills can expose API endpoints for real-time push:

```typescript
// app/api/[skill-slug]/ingest/route.ts

import { createServerClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'
import { registry } from '@/lib/registry'

export async function POST(
  request: NextRequest,
  { params }: { params: { 'skill-slug': string } }
) {
  // Validate API key from Authorization header
  const authHeader = request.headers.get('Authorization')
  if (!authHeader?.startsWith('Bearer ') || authHeader.slice(7) !== process.env.WEBHOOK_SECRET) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const skill = registry.getSkillById(params['skill-slug'])
  if (!skill) {
    return NextResponse.json({ error: 'Unknown skill' }, { status: 404 })
  }

  const body = await request.json()
  const supabase = createServerClient()

  // Skill-specific ingestion logic
  // Each skill defines its own ingest handler in skills/{id}/handlers/ingest.ts
  const handler = await import(`@/skills/${skill.id}/handlers/ingest`)
  const result = await handler.default(supabase, body)

  return NextResponse.json(result)
}
```

### 7.5 Supabase Realtime Subscriptions

Dashboard pages subscribe to real-time changes:

```typescript
// hooks/use-realtime.ts
'use client'

import { useEffect } from 'react'
import { createBrowserClient } from '@/lib/supabase/client'

export function useRealtime(
  table: string,
  filter: string,           // e.g., 'user_id=eq.UUID'
  onInsert?: (payload: any) => void,
  onUpdate?: (payload: any) => void,
  onDelete?: (payload: any) => void
) {
  useEffect(() => {
    const supabase = createBrowserClient()
    const channel = supabase
      .channel(`realtime:${table}`)
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table, filter }, (payload) => onInsert?.(payload.new))
      .on('postgres_changes', { event: 'UPDATE', schema: 'public', table, filter }, (payload) => onUpdate?.(payload.new))
      .on('postgres_changes', { event: 'DELETE', schema: 'public', table, filter }, (payload) => onDelete?.(payload.old))
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [table, filter])
}
```

---

## 8. Skill Page Template

### 8.1 File Structure

Every skill follows this exact structure:

```
skills/{skill-id}/
├── manifest.ts              # SkillManifest definition (§4)
├── pages/
│   ├── main-page.tsx        # Default skill page
│   ├── sub-page-a.tsx       # Sub-page (optional)
│   └── sub-page-b.tsx       # Sub-page (optional)
├── widgets/
│   ├── summary-widget.tsx   # Home overview widget
│   └── alert-widget.tsx     # Home overview widget (optional)
├── handlers/
│   └── ingest.ts            # Webhook handler (if sync.strategy === 'webhook')
├── hooks/
│   └── use-skill-data.ts    # Custom data hooks
├── components/
│   └── skill-specific.tsx   # Components only used by this skill
└── migrations/
    └── up.sql               # SQL migration for this skill's tables
```

### 8.2 Skill Page Routing

Each skill's pages are routed via the App Router:

```tsx
// app/expenses/page.tsx
import { MainPage } from '@/skills/expense-report/pages/main-page'

export const metadata = { title: 'Expenses | NormieClaw' }
export default function ExpensesPage() {
  return <MainPage />
}

// app/expenses/reports/page.tsx
import { ReportsPage } from '@/skills/expense-report/pages/reports-page'

export const metadata = { title: 'Expense Reports | NormieClaw' }
export default function ExpenseReportsPage() {
  return <ReportsPage />
}
```

### 8.3 Example Skill Page Implementation

```tsx
// skills/expense-report/pages/main-page.tsx
import { createServerClient } from '@/lib/supabase/server'
import { PageHeader } from '@/components/shared/page-header'
import { StatCard } from '@/components/shared/stat-card'
import { DataTable } from '@/components/shared/data-table'
import { Receipt, TrendingDown, Calendar, CreditCard } from 'lucide-react'
import { formatCents, formatDate } from '@/lib/utils/format'

export async function MainPage() {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  // Fetch expenses for current month
  const startOfMonth = new Date()
  startOfMonth.setDate(1)

  const { data: expenses } = await supabase
    .from('exp_expenses')
    .select('*')
    .eq('user_id', user!.id)
    .gte('date', startOfMonth.toISOString().split('T')[0])
    .order('date', { ascending: false })

  // Calculate summary stats
  const totalCents = expenses?.reduce((sum, e) => sum + e.amount_cents, 0) ?? 0
  const count = expenses?.length ?? 0

  const columns = [
    { key: 'date', header: 'Date', render: (row: any) => formatDate(row.date) },
    { key: 'vendor', header: 'Vendor' },
    { key: 'category', header: 'Category', render: (row: any) => (
      <BadgePill label={row.category} variant="teal" size="sm" />
    )},
    { key: 'amount_cents', header: 'Amount', align: 'right' as const, render: (row: any) => formatCents(row.amount_cents) },
    { key: 'status', header: 'Status', render: (row: any) => (
      <BadgePill label={row.status} variant={row.status === 'reimbursed' ? 'success' : 'default'} size="sm" />
    )},
  ]

  return (
    <div className="space-y-xl">
      <PageHeader
        title="Expenses"
        description="Track and manage your spending"
        actions={
          <button className="rounded-md bg-teal-500 px-4 py-2 text-bg-950 font-semibold hover:bg-teal-400 transition-colors">
            Add Expense
          </button>
        }
      />

      {/* Stats row */}
      <div className="grid grid-cols-1 gap-md sm:grid-cols-2 lg:grid-cols-4">
        <StatCard value={formatCents(totalCents)} label="This Month" icon={<Receipt size={20} />} color="teal" />
        <StatCard value={count} label="Transactions" icon={<CreditCard size={20} />} color="orange" />
        {/* More stat cards... */}
      </div>

      {/* Expenses table */}
      <DataTable
        columns={columns}
        data={expenses ?? []}
        rowKey="id"
        searchPlaceholder="Search expenses..."
        searchColumns={['vendor', 'category']}
        emptyMessage="No expenses this month. Your wallet thanks you."
      />
    </div>
  )
}
```

### 8.4 Home Widget Implementation

```tsx
// skills/expense-report/widgets/summary-widget.tsx
import { createServerClient } from '@/lib/supabase/server'
import { StatCard } from '@/components/shared/stat-card'
import { Receipt } from 'lucide-react'
import { formatCents } from '@/lib/utils/format'

export async function ExpenseSummaryWidget() {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  const startOfMonth = new Date()
  startOfMonth.setDate(1)

  const { data } = await supabase
    .from('exp_expenses')
    .select('amount_cents')
    .eq('user_id', user!.id)
    .gte('date', startOfMonth.toISOString().split('T')[0])

  const total = data?.reduce((sum, e) => sum + e.amount_cents, 0) ?? 0

  return (
    <StatCard
      value={formatCents(total)}
      label="Spent This Month"
      icon={<Receipt size={20} />}
      color="teal"
      onClick={() => window.location.href = '/expenses'}
    />
  )
}
```

---

## 9. Home Overview Page

### 9.1 Layout

```tsx
// app/page.tsx
import { createServerClient } from '@/lib/supabase/server'
import { registry } from '@/lib/registry'
import { PageHeader } from '@/components/shared/page-header'
import { formatDate } from '@/lib/utils/format'

export default async function HomePage() {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  const { data: profile } = await supabase
    .from('profiles')
    .select('display_name')
    .eq('id', user!.id)
    .single()

  const skills = registry.getEnabledSkills()
  const widgetDefs = registry.getAllHomeWidgets()

  return (
    <div className="space-y-xl">
      {/* Greeting */}
      <div>
        <h1 className="text-h1 text-text-1">
          Good {getTimeOfDay()}, {profile?.display_name || 'there'}
        </h1>
        <p className="text-body-sm text-text-3 mt-xs">
          {formatDate(new Date(), 'EEEE, MMMM d, yyyy')}
        </p>
      </div>

      {/* Quick Actions Strip */}
      <div className="flex gap-sm overflow-x-auto pb-sm">
        {skills.slice(0, 6).map(skill => (
          <a
            key={skill.id}
            href={skill.nav.defaultRoute}
            className="flex items-center gap-xs rounded-lg border border-soft bg-surface-1 px-md py-sm hover:border-strong hover:bg-surface-2 transition-all whitespace-nowrap"
          >
            <span>{skill.icon}</span>
            <span className="text-body-sm text-text-2">{skill.nav.label}</span>
          </a>
        ))}
      </div>

      {/* Widget Grid */}
      <div className="grid grid-cols-1 gap-md sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {widgetDefs.map(widget => {
          const WidgetComponent = getWidgetComponent(widget.skillId, widget.component)
          return (
            <div key={`${widget.skillId}-${widget.id}`} className={getSpanClass(widget.span)}>
              <WidgetComponent />
            </div>
          )
        })}
      </div>

      {/* Recent Activity (aggregated timeline) */}
      <section>
        <h2 className="text-h3 text-text-1 mb-md">Recent Activity</h2>
        <AggregatedTimeline userId={user!.id} limit={10} />
      </section>

      {/* Upcoming (from all skills that track dates) */}
      <section>
        <h2 className="text-h3 text-text-1 mb-md">Upcoming</h2>
        <UpcomingEvents userId={user!.id} days={7} />
      </section>
    </div>
  )
}

function getSpanClass(span: number): string {
  switch (span) {
    case 1: return 'col-span-1'
    case 2: return 'col-span-1 sm:col-span-2'
    case 3: return 'col-span-1 sm:col-span-2 lg:col-span-3'
    default: return 'col-span-1'
  }
}

function getTimeOfDay(): string {
  const hour = new Date().getHours()
  if (hour < 12) return 'morning'
  if (hour < 17) return 'afternoon'
  return 'evening'
}
```

### 9.2 Widget Grid Rules

1. Each skill provides 1-2 widgets (defined in `homeWidgets` in manifest)
2. Widgets span 1, 2, or 3 grid columns
3. Default layout: 4-column grid on desktop, 2 on tablet, 1 on mobile
4. Future: user can drag-to-reorder via `@dnd-kit` (store order in `profiles.sidebar_order`)
5. Widgets are React Server Components — they fetch their own data
6. If a widget's data source returns empty, it renders an `EmptyState` with a CTA

### 9.3 Aggregated Timeline

The home timeline pulls recent activity from the `notifications` table and presents it chronologically:

```typescript
// Each skill writes notifications when significant events occur:
// - Expense logged
// - Workout completed
// - Email triaged
// - Security scan finished
// - Plant needs water
// etc.

// The timeline reads notifications ORDER BY created_at DESC LIMIT 10
```

---

## 10. Auth & Security

### 10.1 Supabase Auth Configuration

```typescript
// lib/supabase/client.ts
import { createBrowserClient as createSupabaseBrowserClient } from '@supabase/ssr'

export function createBrowserClient() {
  return createSupabaseBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// lib/supabase/server.ts
import { createServerClient as createSupabaseServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export function createServerClient() {
  const cookieStore = cookies()
  return createSupabaseServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) { return cookieStore.get(name)?.value },
        set(name: string, value: string, options: any) { cookieStore.set({ name, value, ...options }) },
        remove(name: string, options: any) { cookieStore.set({ name, value: '', ...options }) },
      },
    }
  )
}
```

### 10.2 Auth Methods

1. **Email + Password** — standard registration and login
2. **Magic Link** — passwordless email login
3. **OAuth** (optional future) — Google, GitHub

### 10.3 Middleware (Route Protection)

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request: { headers: request.headers } })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) { return request.cookies.get(name)?.value },
        set(name: string, value: string, options: any) {
          request.cookies.set({ name, value, ...options })
          response = NextResponse.next({ request: { headers: request.headers } })
          response.cookies.set({ name, value, ...options })
        },
        remove(name: string, options: any) {
          request.cookies.set({ name, value: '', ...options })
          response = NextResponse.next({ request: { headers: request.headers } })
          response.cookies.set({ name, value: '', ...options })
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Redirect unauthenticated users to login
  if (!user && !request.nextUrl.pathname.startsWith('/login')) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  // Redirect authenticated users away from login
  if (user && request.nextUrl.pathname.startsWith('/login')) {
    const url = request.nextUrl.clone()
    url.pathname = '/'
    return NextResponse.redirect(url)
  }

  return response
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|noise.svg|logo.svg|api/sync).*)'],
}
```

### 10.4 Security Rules

1. **NEVER expose** `SUPABASE_SERVICE_ROLE_KEY` to client-side code. Only `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` are client-safe.
2. **RLS on every table.** No exceptions. See §5.5 for the template.
3. **API routes** that accept external input (webhooks, sync) must validate an auth token from the `Authorization` header.
4. **Environment variables** — all secrets in `.env.local` (never committed):
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
   SUPABASE_SERVICE_ROLE_KEY=eyJ...
   WEBHOOK_SECRET=your-webhook-secret
   ```
5. **Supabase Storage** buckets for file uploads (receipts, photos, PDFs) must be **private**. Use signed URLs with expiration for display.
6. **Input validation** via Zod schemas on all API route handlers.

---

## 11. Deployment Guide

### 11.1 Vercel (Primary)

**Prerequisites:**
- GitHub repo connected to Vercel
- Supabase project created

**Steps:**

1. **Create Supabase project:**
   - Go to https://supabase.com/dashboard
   - Create new project
   - Note: Project URL, anon key, service role key
   - Enable Realtime for tables that need it

2. **Run migrations:**
   ```bash
   npx supabase init
   npx supabase link --project-ref YOUR_PROJECT_REF
   npx supabase db push
   ```

3. **Configure Vercel:**
   - Import repo from GitHub
   - Framework: Next.js
   - Root directory: `/`
   - Build command: `next build`
   - Output directory: `.next`

4. **Environment variables (Vercel dashboard):**
   ```
   NEXT_PUBLIC_SUPABASE_URL        = https://xxx.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY   = eyJ...
   SUPABASE_SERVICE_ROLE_KEY       = eyJ... (not NEXT_PUBLIC!)
   WEBHOOK_SECRET                  = (generate: openssl rand -hex 32)
   ```

5. **Deploy:**
   ```bash
   git push origin main  # Vercel auto-deploys
   ```

6. **Custom domain (optional):**
   - Add domain in Vercel dashboard
   - Add CNAME record in DNS

### 11.2 Self-Hosted (Docker)

```dockerfile
# Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  dashboard:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_SUPABASE_URL=${SUPABASE_URL}
      - NEXT_PUBLIC_SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
      - SUPABASE_SERVICE_ROLE_KEY=${SUPABASE_SERVICE_ROLE_KEY}
      - WEBHOOK_SECRET=${WEBHOOK_SECRET}
    restart: unless-stopped
```

**next.config.mjs for standalone output:**
```javascript
// next.config.mjs
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '*.supabase.co' },
    ],
  },
}
export default nextConfig
```

---

## 12. Complete Manifest Definitions

Below are the full `manifest.ts` for all 21 skills. These are **copy-paste ready**.

### Expense Report Pro

```typescript
// skills/expense-report/manifest.ts
import type { SkillManifest } from '@/lib/types/skill'

export const manifest: SkillManifest = {
  id: 'expense-report',
  displayName: 'Expense Report Pro',
  icon: '💰',
  lucideIcon: 'Receipt',
  dbPrefix: 'exp',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'finance',
  nav: {
    label: 'Expenses',
    defaultRoute: '/expenses',
    children: [
      { label: 'All Expenses', route: '/expenses' },
      { label: 'Reports', route: '/expenses/reports', lucideIcon: 'FileBarChart' },
      { label: 'Budgets', route: '/expenses/budgets', lucideIcon: 'PiggyBank' },
    ],
  },
  homeWidgets: [
    { id: 'monthly-spend', component: 'ExpenseSummaryWidget', span: 1, dataSource: 'exp_expenses' },
  ],
  tables: [
    { name: 'exp_expenses', description: 'All expense records with category, amount, and status' },
  ],
  settings: [
    { key: 'default_currency', label: 'Default Currency', type: 'select', defaultValue: 'USD', options: [{ label: 'USD', value: 'USD' }, { label: 'EUR', value: 'EUR' }, { label: 'GBP', value: 'GBP' }] },
    { key: 'receipt_auto_scan', label: 'Auto-Scan Receipts', type: 'toggle', defaultValue: true, description: 'Automatically extract data from uploaded receipt images' },
  ],
  sync: { strategy: 'direct' },
}
```

### Meal Planner Pro

```typescript
// skills/meal-planner/manifest.ts
export const manifest: SkillManifest = {
  id: 'meal-planner',
  displayName: 'Meal Planner Pro',
  icon: '🍽️',
  lucideIcon: 'UtensilsCrossed',
  dbPrefix: 'mp',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'lifestyle',
  nav: {
    label: 'Meal Planner',
    defaultRoute: '/meals',
    children: [
      { label: 'Weekly Plan', route: '/meals' },
      { label: 'Calendar', route: '/meals/calendar', lucideIcon: 'Calendar' },
      { label: 'Grocery List', route: '/meals/grocery', lucideIcon: 'ShoppingCart' },
      { label: 'Recipes', route: '/meals/recipes', lucideIcon: 'BookOpen' },
      { label: 'Freezer', route: '/meals/freezer', lucideIcon: 'Snowflake' },
    ],
  },
  homeWidgets: [
    { id: 'todays-meals', component: 'TodaysMealsWidget', span: 2, dataSource: 'mp_meal_slots' },
  ],
  tables: [
    { name: 'mp_households', description: 'Household groups' },
    { name: 'mp_members', description: 'Household members with dietary info' },
    { name: 'mp_dietary_preferences', description: 'Household dietary preferences' },
    { name: 'mp_recipes', description: 'Recipe library' },
    { name: 'mp_recipe_ingredients', description: 'Recipe ingredients' },
    { name: 'mp_meal_plans', description: 'Weekly meal plans' },
    { name: 'mp_meal_slots', description: 'Individual meal assignments' },
    { name: 'mp_meal_slot_members', description: 'Who eats which meals' },
    { name: 'mp_ratings', description: 'Meal ratings from household members' },
    { name: 'mp_grocery_lists', description: 'Generated grocery lists' },
    { name: 'mp_grocery_items', description: 'Items on grocery lists' },
    { name: 'mp_stores', description: 'Preferred stores' },
    { name: 'mp_freezer_items', description: 'Freezer inventory' },
    { name: 'mp_flagged_recipes', description: 'AI-flagged recipe suggestions' },
    { name: 'mp_chat_messages', description: 'Meal planning chat history' },
    { name: 'mp_pantry_staples', description: 'Pantry staple items' },
  ],
  settings: [
    { key: 'household_size', label: 'Household Size', type: 'number', defaultValue: 2 },
    { key: 'budget_level', label: 'Budget Level', type: 'select', defaultValue: 'moderate', options: [{ label: 'Budget', value: 'budget' }, { label: 'Moderate', value: 'moderate' }, { label: 'Premium', value: 'premium' }] },
  ],
  sync: { strategy: 'direct' },
}
```

### Supercharged Memory

```typescript
// skills/supercharged-memory/manifest.ts
export const manifest: SkillManifest = {
  id: 'supercharged-memory',
  displayName: 'Supercharged Memory',
  icon: '🧠',
  lucideIcon: 'Brain',
  dbPrefix: 'mem',
  accentColor: '#38bdf8',
  version: '1.0.0',
  category: 'productivity',
  nav: {
    label: 'Memory',
    defaultRoute: '/memory',
    children: [
      { label: 'Browser', route: '/memory' },
      { label: 'Timeline', route: '/memory/timeline', lucideIcon: 'Clock' },
      { label: 'Topic Clusters', route: '/memory/clusters', lucideIcon: 'Network' },
      { label: 'Stats', route: '/memory/stats', lucideIcon: 'BarChart3' },
    ],
  },
  homeWidgets: [
    { id: 'memory-count', component: 'MemoryCountWidget', span: 1, dataSource: 'mem_stats' },
  ],
  tables: [
    { name: 'mem_memories', description: 'Stored memories with embeddings' },
    { name: 'mem_stats', description: 'Daily memory statistics' },
  ],
  settings: [
    { key: 'auto_categorize', label: 'Auto-Categorize', type: 'toggle', defaultValue: true },
  ],
  sync: { strategy: 'json', sourceDir: 'supercharged-memory/data/' },
}
```

### Stock Watcher Pro

```typescript
// skills/stock-watcher/manifest.ts
export const manifest: SkillManifest = {
  id: 'stock-watcher',
  displayName: 'Stock Watcher Pro',
  icon: '📈',
  lucideIcon: 'TrendingUp',
  dbPrefix: 'sw',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'finance',
  nav: {
    label: 'Stocks',
    defaultRoute: '/stocks',
    children: [
      { label: 'Portfolio', route: '/stocks' },
      { label: 'Briefings', route: '/stocks/briefings', lucideIcon: 'FileText' },
      { label: 'Intel Feed', route: '/stocks/intel', lucideIcon: 'Rss' },
      { label: 'Thesis Tracker', route: '/stocks/thesis', lucideIcon: 'Target' },
      { label: 'Source Health', route: '/stocks/sources', lucideIcon: 'Activity' },
    ],
  },
  homeWidgets: [
    { id: 'portfolio-summary', component: 'PortfolioSummaryWidget', span: 2, dataSource: 'sw_holdings' },
  ],
  tables: [
    { name: 'sw_portfolios', description: 'Investment portfolios' },
    { name: 'sw_holdings', description: 'Portfolio holdings/positions' },
    { name: 'sw_briefings', description: 'Market briefings' },
    { name: 'sw_filing_summaries', description: 'SEC filing AI summaries' },
    { name: 'sw_news_links', description: 'Curated news links' },
    { name: 'sw_source_network', description: 'Data source health tracking' },
    { name: 'sw_thesis_tracking', description: 'Investment thesis tracking' },
  ],
  settings: [
    { key: 'default_portfolio', label: 'Default Portfolio', type: 'text', defaultValue: '' },
    { key: 'briefing_time', label: 'Daily Briefing Time', type: 'text', defaultValue: '06:00', description: 'HH:MM format' },
  ],
  sync: { strategy: 'json', sourceDir: 'stock-watcher-pro/data/' },
}
```

### Travel Planner Pro

```typescript
// skills/travel-planner/manifest.ts
export const manifest: SkillManifest = {
  id: 'travel-planner',
  displayName: 'Travel Planner Pro',
  icon: '✈️',
  lucideIcon: 'Plane',
  dbPrefix: 'tp',
  accentColor: '#1e3a5f',
  version: '1.0.0',
  category: 'lifestyle',
  nav: {
    label: 'Travel',
    defaultRoute: '/travel',
    children: [
      { label: 'Trips', route: '/travel' },
      { label: 'Itinerary', route: '/travel/itinerary', lucideIcon: 'Map' },
      { label: 'Budget', route: '/travel/budget', lucideIcon: 'Wallet' },
      { label: 'Packing', route: '/travel/packing', lucideIcon: 'Luggage' },
      { label: 'Archive', route: '/travel/archive', lucideIcon: 'Archive' },
    ],
  },
  homeWidgets: [
    { id: 'next-trip', component: 'NextTripWidget', span: 2, dataSource: 'tp_trips' },
  ],
  tables: [
    { name: 'tp_profiles', description: 'Travel preferences' },
    { name: 'tp_trips', description: 'Trip records' },
    { name: 'tp_trip_days', description: 'Day-by-day itinerary' },
    { name: 'tp_activities', description: 'Planned activities' },
    { name: 'tp_trip_budgets', description: 'Trip budget by category' },
    { name: 'tp_packing_items', description: 'Packing checklist items' },
    { name: 'tp_companions', description: 'Travel companions' },
    { name: 'tp_loyalty_programs', description: 'Loyalty program memberships' },
  ],
  settings: [
    { key: 'home_airport', label: 'Home Airport Code', type: 'text', defaultValue: '' },
    { key: 'pace_preference', label: 'Travel Pace', type: 'select', defaultValue: 'moderate', options: [{ label: 'Relaxed', value: 'relaxed' }, { label: 'Moderate', value: 'moderate' }, { label: 'Packed', value: 'packed' }] },
  ],
  sync: { strategy: 'direct' },
}
```

### Security Team

```typescript
// skills/security-team/manifest.ts
export const manifest: SkillManifest = {
  id: 'security-team',
  displayName: 'Security Team',
  icon: '🔒',
  lucideIcon: 'Shield',
  dbPrefix: 'sec',
  accentColor: '#f97316',
  version: '1.0.0',
  category: 'productivity',
  nav: {
    label: 'Security',
    defaultRoute: '/security',
    children: [
      { label: 'Overview', route: '/security' },
      { label: 'Issues', route: '/security/issues', lucideIcon: 'AlertTriangle' },
      { label: 'Scan History', route: '/security/history', lucideIcon: 'History' },
    ],
  },
  homeWidgets: [
    { id: 'security-score', component: 'SecurityScoreWidget', span: 1, dataSource: 'sec_audits' },
  ],
  tables: [
    { name: 'sec_audits', description: 'Security audit results' },
    { name: 'sec_issues', description: 'Identified security issues' },
  ],
  settings: [
    { key: 'scan_frequency', label: 'Scan Frequency', type: 'select', defaultValue: 'weekly', options: [{ label: 'Daily', value: 'daily' }, { label: 'Weekly', value: 'weekly' }, { label: 'Monthly', value: 'monthly' }] },
  ],
  sync: { strategy: 'webhook', webhookPath: '/ingest' },
}
```

### Content Creator Pro

```typescript
// skills/content-creator/manifest.ts
export const manifest: SkillManifest = {
  id: 'content-creator',
  displayName: 'Content Creator Pro',
  icon: '📱',
  lucideIcon: 'Megaphone',
  dbPrefix: 'cc',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'work',
  nav: {
    label: 'Content',
    defaultRoute: '/content',
    children: [
      { label: 'Calendar', route: '/content' },
      { label: 'Drafts', route: '/content/drafts', lucideIcon: 'PenSquare' },
      { label: 'Analytics', route: '/content/analytics', lucideIcon: 'BarChart3' },
      { label: 'Brand Voice', route: '/content/voice', lucideIcon: 'Mic' },
      { label: 'Idea Bank', route: '/content/ideas', lucideIcon: 'Lightbulb' },
    ],
  },
  homeWidgets: [
    { id: 'content-pipeline', component: 'ContentPipelineWidget', span: 2, dataSource: 'cc_posts' },
  ],
  tables: [
    { name: 'cc_brand_profiles', description: 'Brand voice profiles' },
    { name: 'cc_content_pillars', description: 'Content strategy pillars' },
    { name: 'cc_posts', description: 'Content posts and drafts' },
    { name: 'cc_engagement_metrics', description: 'Post performance metrics' },
    { name: 'cc_idea_bank', description: 'Content idea backlog' },
    { name: 'cc_voice_learnings', description: 'Brand voice learning examples' },
    { name: 'cc_competitor_notes', description: 'Competitor content analysis' },
  ],
  settings: [
    { key: 'default_brand', label: 'Default Brand Profile', type: 'text', defaultValue: '' },
    { key: 'platforms', label: 'Active Platforms', type: 'text', defaultValue: 'twitter,linkedin', description: 'Comma-separated platform names' },
  ],
  sync: { strategy: 'direct' },
}
```

### Daily Briefing

```typescript
// skills/daily-briefing/manifest.ts
export const manifest: SkillManifest = {
  id: 'daily-briefing',
  displayName: 'Daily Briefing',
  icon: '☀️',
  lucideIcon: 'Sun',
  dbPrefix: 'dbr',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'productivity',
  nav: {
    label: 'Briefing',
    defaultRoute: '/briefing',
    children: [
      { label: "Today's Brief", route: '/briefing' },
      { label: 'Archive', route: '/briefing/archive', lucideIcon: 'Archive' },
      { label: 'Sources', route: '/briefing/sources', lucideIcon: 'Rss' },
    ],
  },
  homeWidgets: [
    { id: 'briefing-status', component: 'BriefingStatusWidget', span: 1, dataSource: 'dbr_briefings' },
  ],
  tables: [
    { name: 'dbr_briefings', description: 'Daily briefing documents' },
    { name: 'dbr_stories', description: 'Individual stories within briefings' },
    { name: 'dbr_sources', description: 'News sources configuration' },
    { name: 'dbr_feedback', description: 'Briefing quality feedback' },
    { name: 'dbr_source_fetch_log', description: 'Source fetch audit log' },
  ],
  settings: [
    { key: 'delivery_time', label: 'Delivery Time', type: 'text', defaultValue: '06:00' },
    { key: 'topics', label: 'Focus Topics', type: 'text', defaultValue: '', description: 'Comma-separated topics of interest' },
  ],
  sync: { strategy: 'webhook', webhookPath: '/ingest' },
}
```

### Knowledge Vault

```typescript
// skills/knowledge-vault/manifest.ts
export const manifest: SkillManifest = {
  id: 'knowledge-vault',
  displayName: 'Knowledge Vault',
  icon: '📚',
  lucideIcon: 'BookMarked',
  dbPrefix: 'kv',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'learning',
  nav: {
    label: 'Knowledge',
    defaultRoute: '/knowledge',
    children: [
      { label: 'Browse', route: '/knowledge' },
      { label: 'Collections', route: '/knowledge/collections', lucideIcon: 'FolderOpen' },
    ],
  },
  homeWidgets: [
    { id: 'vault-count', component: 'VaultCountWidget', span: 1, dataSource: 'kv_entries' },
  ],
  tables: [
    { name: 'kv_entries', description: 'Saved knowledge entries' },
    { name: 'kv_collections', description: 'Entry collections/folders' },
  ],
  settings: [
    { key: 'default_collection', label: 'Default Collection', type: 'text', defaultValue: 'general' },
  ],
  sync: { strategy: 'json', sourceDir: 'knowledge-vault/data/' },
}
```

### Trainer Buddy Pro

```typescript
// skills/trainer-buddy/manifest.ts
export const manifest: SkillManifest = {
  id: 'trainer-buddy',
  displayName: 'Trainer Buddy Pro',
  icon: '🏋️',
  lucideIcon: 'Dumbbell',
  dbPrefix: 'tb',
  accentColor: '#00f0ff',
  version: '1.0.0',
  category: 'health',
  nav: {
    label: 'Training',
    defaultRoute: '/training',
    children: [
      { label: 'Overview', route: '/training' },
      { label: 'Workout Log', route: '/training/log', lucideIcon: 'ClipboardList' },
      { label: 'Progress', route: '/training/progress', lucideIcon: 'TrendingUp' },
      { label: 'Exercises', route: '/training/exercises', lucideIcon: 'Dumbbell' },
      { label: 'PRs', route: '/training/prs', lucideIcon: 'Trophy' },
    ],
  },
  homeWidgets: [
    { id: 'workout-streak', component: 'WorkoutStreakWidget', span: 1, dataSource: 'tb_workouts' },
  ],
  tables: [
    { name: 'tb_profiles', description: 'Fitness profiles' },
    { name: 'tb_injuries', description: 'Injury tracking' },
    { name: 'tb_exercises', description: 'Exercise library (shared)' },
    { name: 'tb_workouts', description: 'Workout sessions' },
    { name: 'tb_workout_sets', description: 'Individual exercise sets' },
    { name: 'tb_body_metrics', description: 'Body measurements over time' },
    { name: 'tb_personal_records', description: 'Personal bests' },
  ],
  settings: [
    { key: 'weight_unit', label: 'Weight Unit', type: 'select', defaultValue: 'lbs', options: [{ label: 'Pounds', value: 'lbs' }, { label: 'Kilograms', value: 'kg' }] },
    { key: 'training_days', label: 'Training Days/Week', type: 'number', defaultValue: 4 },
  ],
  sync: { strategy: 'json', sourceDir: 'trainer-buddy-pro/data/' },
}
```

### Email Assistant

```typescript
// skills/email-assistant/manifest.ts
export const manifest: SkillManifest = {
  id: 'email-assistant',
  displayName: 'Email Assistant',
  icon: '📧',
  lucideIcon: 'Mail',
  dbPrefix: 'ea',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'work',
  nav: {
    label: 'Email',
    defaultRoute: '/email',
    children: [
      { label: 'Inbox', route: '/email' },
      { label: 'Priority Queue', route: '/email/priority', lucideIcon: 'AlertCircle' },
      { label: 'Drafts', route: '/email/drafts', lucideIcon: 'PenSquare' },
      { label: 'VIP Senders', route: '/email/vip', lucideIcon: 'Star' },
      { label: 'Analytics', route: '/email/analytics', lucideIcon: 'BarChart3' },
    ],
  },
  homeWidgets: [
    { id: 'email-urgent', component: 'UrgentEmailWidget', span: 1, dataSource: 'ea_email_triage' },
  ],
  tables: [
    { name: 'ea_email_triage', description: 'Triaged email summaries' },
    { name: 'ea_email_drafts', description: 'AI-drafted replies' },
    { name: 'ea_vip_senders', description: 'VIP sender configuration' },
    { name: 'ea_email_digests', description: 'Daily email digest summaries' },
  ],
  settings: [
    { key: 'auto_triage', label: 'Auto-Triage', type: 'toggle', defaultValue: true },
    { key: 'vip_escalation', label: 'VIP Escalation', type: 'select', defaultValue: 'notify', options: [{ label: 'Notify', value: 'notify' }, { label: 'Urgent', value: 'urgent' }, { label: 'Auto-Reply', value: 'auto-reply' }] },
  ],
  sync: { strategy: 'direct' },
}
```

### HireMe Pro

```typescript
// skills/hireme/manifest.ts
export const manifest: SkillManifest = {
  id: 'hireme',
  displayName: 'HireMe Pro',
  icon: '💼',
  lucideIcon: 'Briefcase',
  dbPrefix: 'hm',
  accentColor: '#2563eb',
  version: '1.0.0',
  category: 'work',
  nav: {
    label: 'Job Hunt',
    defaultRoute: '/jobs',
    children: [
      { label: 'Dashboard', route: '/jobs' },
      { label: 'Applications', route: '/jobs/applications', lucideIcon: 'KanbanSquare' },
      { label: 'Resumes', route: '/jobs/resumes', lucideIcon: 'FileText' },
      { label: 'Interview Prep', route: '/jobs/prep', lucideIcon: 'MessageSquare' },
    ],
  },
  homeWidgets: [
    { id: 'active-applications', component: 'ActiveApplicationsWidget', span: 1, dataSource: 'hm_applications' },
  ],
  tables: [
    { name: 'hm_profiles', description: 'Job seeker profile' },
    { name: 'hm_resumes', description: 'Resume versions' },
    { name: 'hm_applications', description: 'Job applications tracker' },
    { name: 'hm_prep_sessions', description: 'Interview prep sessions' },
    { name: 'hm_activity_log', description: 'Job hunt activity log' },
  ],
  settings: [
    { key: 'target_role', label: 'Target Role', type: 'text', defaultValue: '' },
  ],
  sync: { strategy: 'direct' },
}
```

### Health Buddy Pro

```typescript
// skills/health-buddy/manifest.ts
export const manifest: SkillManifest = {
  id: 'health-buddy',
  displayName: 'Health Buddy Pro',
  icon: '🏥',
  lucideIcon: 'HeartPulse',
  dbPrefix: 'hb',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'health',
  nav: {
    label: 'Health',
    defaultRoute: '/health',
    children: [
      { label: 'Dashboard', route: '/health' },
      { label: 'Nutrition', route: '/health/nutrition', lucideIcon: 'Apple' },
      { label: 'Hydration', route: '/health/hydration', lucideIcon: 'Droplets' },
      { label: 'Activity', route: '/health/activity', lucideIcon: 'Activity' },
      { label: 'Supplements', route: '/health/supplements', lucideIcon: 'Pill' },
      { label: 'Trends', route: '/health/trends', lucideIcon: 'TrendingUp' },
    ],
  },
  homeWidgets: [
    { id: 'daily-nutrition', component: 'DailyNutritionWidget', span: 1, dataSource: 'hb_daily_summaries' },
    { id: 'hydration-progress', component: 'HydrationWidget', span: 1, dataSource: 'hb_hydration_entries' },
  ],
  tables: [
    { name: 'hb_profiles', description: 'Health targets and preferences' },
    { name: 'hb_nutrition_entries', description: 'Food/meal logging' },
    { name: 'hb_hydration_entries', description: 'Water intake tracking' },
    { name: 'hb_supplement_entries', description: 'Supplement tracking' },
    { name: 'hb_activity_entries', description: 'Physical activity logging' },
    { name: 'hb_custom_metrics', description: 'Custom health metrics' },
    { name: 'hb_daily_summaries', description: 'Aggregated daily totals' },
  ],
  settings: [
    { key: 'calorie_target', label: 'Daily Calorie Target', type: 'number', defaultValue: 2000 },
    { key: 'water_target_oz', label: 'Daily Water Target (oz)', type: 'number', defaultValue: 64 },
  ],
  sync: { strategy: 'direct' },
}
```

### NoteTaker Pro

```typescript
// skills/notetaker/manifest.ts
export const manifest: SkillManifest = {
  id: 'notetaker',
  displayName: 'NoteTaker Pro',
  icon: '📝',
  lucideIcon: 'StickyNote',
  dbPrefix: 'nt',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'productivity',
  nav: {
    label: 'Notes',
    defaultRoute: '/notes',
    children: [
      { label: 'All Notes', route: '/notes' },
      { label: 'Tags', route: '/notes/tags', lucideIcon: 'Tags' },
      { label: 'Templates', route: '/notes/templates', lucideIcon: 'FileTemplate' },
    ],
  },
  homeWidgets: [
    { id: 'recent-notes', component: 'RecentNotesWidget', span: 1, dataSource: 'nt_notes' },
  ],
  tables: [
    { name: 'nt_notes', description: 'Notes with full-text search' },
    { name: 'nt_tags', description: 'Tag taxonomy' },
    { name: 'nt_note_templates', description: 'Note templates' },
  ],
  settings: [
    { key: 'default_category', label: 'Default Category', type: 'text', defaultValue: 'general' },
  ],
  sync: { strategy: 'json', sourceDir: 'notetaker-pro/data/' },
}
```

### Relationship Buddy

```typescript
// skills/relationship-buddy/manifest.ts
export const manifest: SkillManifest = {
  id: 'relationship-buddy',
  displayName: 'Relationship Buddy',
  icon: '👥',
  lucideIcon: 'Users',
  dbPrefix: 'rb',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'lifestyle',
  nav: {
    label: 'Relationships',
    defaultRoute: '/relationships',
    children: [
      { label: 'Dashboard', route: '/relationships' },
      { label: 'Contacts', route: '/relationships/contacts', lucideIcon: 'Contact' },
      { label: 'Calendar', route: '/relationships/calendar', lucideIcon: 'Calendar' },
    ],
  },
  homeWidgets: [
    { id: 'upcoming-dates', component: 'UpcomingDatesWidget', span: 1, dataSource: 'rb_key_dates' },
    { id: 'follow-ups', component: 'PendingFollowUpsWidget', span: 1, dataSource: 'rb_follow_ups' },
  ],
  tables: [
    { name: 'rb_contacts', description: 'Contact profiles' },
    { name: 'rb_key_dates', description: 'Important dates (birthdays, anniversaries)' },
    { name: 'rb_interactions', description: 'Interaction history' },
    { name: 'rb_follow_ups', description: 'Pending follow-up actions' },
    { name: 'rb_life_events', description: 'Life events for contacts' },
    { name: 'rb_gifts', description: 'Gift tracking' },
    { name: 'rb_reminders', description: 'Scheduled reminders' },
    { name: 'rb_health_scores', description: 'Relationship health metrics' },
  ],
  settings: [
    { key: 'reminder_days', label: 'Default Reminder Days Before', type: 'number', defaultValue: 7 },
  ],
  sync: { strategy: 'direct' },
}
```

### Tutor Buddy Pro

```typescript
// skills/tutor-buddy/manifest.ts
export const manifest: SkillManifest = {
  id: 'tutor-buddy',
  displayName: 'Tutor Buddy Pro',
  icon: '📚',
  lucideIcon: 'GraduationCap',
  dbPrefix: 'tu',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'learning',
  nav: {
    label: 'Tutor',
    defaultRoute: '/tutor',
    children: [
      { label: 'Dashboard', route: '/tutor' },
      { label: 'Sessions', route: '/tutor/sessions', lucideIcon: 'Clock' },
      { label: 'Quizzes', route: '/tutor/quizzes', lucideIcon: 'CheckSquare' },
      { label: 'Mastery', route: '/tutor/mastery', lucideIcon: 'Target' },
      { label: 'Study Plans', route: '/tutor/plans', lucideIcon: 'BookOpen' },
      { label: 'Achievements', route: '/tutor/achievements', lucideIcon: 'Award' },
    ],
  },
  homeWidgets: [
    { id: 'study-streak', component: 'StudyStreakWidget', span: 1, dataSource: 'tu_sessions' },
  ],
  tables: [
    { name: 'tu_profiles', description: 'Learner profiles' },
    { name: 'tu_sessions', description: 'Tutoring sessions' },
    { name: 'tu_queries', description: 'Questions asked during sessions' },
    { name: 'tu_quiz_results', description: 'Quiz scores and analysis' },
    { name: 'tu_mastery_tracking', description: 'Topic mastery levels' },
    { name: 'tu_study_plans', description: 'Structured study plans' },
    { name: 'tu_achievements', description: 'Unlocked achievements' },
  ],
  settings: [
    { key: 'learning_style', label: 'Learning Style', type: 'select', defaultValue: 'visual', options: [{ label: 'Visual', value: 'visual' }, { label: 'Auditory', value: 'auditory' }, { label: 'Read/Write', value: 'read_write' }, { label: 'Kinesthetic', value: 'kinesthetic' }] },
  ],
  sync: { strategy: 'direct' },
}
```

### Budget Buddy Pro

```typescript
// skills/budget-buddy/manifest.ts
export const manifest: SkillManifest = {
  id: 'budget-buddy',
  displayName: 'Budget Buddy Pro',
  icon: '💵',
  lucideIcon: 'Wallet',
  dbPrefix: 'bb',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'finance',
  nav: {
    label: 'Budget',
    defaultRoute: '/budget',
    children: [
      { label: 'Overview', route: '/budget' },
      { label: 'Transactions', route: '/budget/transactions', lucideIcon: 'ArrowRightLeft' },
      { label: 'Budgets', route: '/budget/budgets', lucideIcon: 'PiggyBank' },
      { label: 'Trends', route: '/budget/trends', lucideIcon: 'TrendingUp' },
      { label: 'Savings', route: '/budget/savings', lucideIcon: 'Target' },
      { label: 'Net Worth', route: '/budget/networth', lucideIcon: 'BarChart3' },
      { label: 'Bills', route: '/budget/bills', lucideIcon: 'Receipt' },
    ],
  },
  homeWidgets: [
    { id: 'monthly-budget', component: 'MonthlyBudgetWidget', span: 1, dataSource: 'bb_transactions' },
  ],
  tables: [
    { name: 'bb_budgets', description: 'Budget configurations' },
    { name: 'bb_transactions', description: 'Income and expense transactions' },
    { name: 'bb_recurring', description: 'Recurring bills and income' },
    { name: 'bb_savings_goals', description: 'Savings goal tracking' },
    { name: 'bb_net_worth_snapshots', description: 'Net worth over time' },
  ],
  settings: [
    { key: 'budget_framework', label: 'Budget Framework', type: 'select', defaultValue: '50-30-20', options: [{ label: '50/30/20', value: '50-30-20' }, { label: 'Zero-Based', value: 'zero-based' }, { label: 'Envelope', value: 'envelope' }, { label: 'Custom', value: 'custom' }] },
    { key: 'currency', label: 'Currency', type: 'select', defaultValue: 'USD', options: [{ label: 'USD', value: 'USD' }, { label: 'EUR', value: 'EUR' }] },
  ],
  sync: { strategy: 'json', sourceDir: 'budget-buddy-pro/data/' },
}
```

### Plant Doctor

```typescript
// skills/plant-doctor/manifest.ts
export const manifest: SkillManifest = {
  id: 'plant-doctor',
  displayName: 'Plant Doctor',
  icon: '🌱',
  lucideIcon: 'Sprout',
  dbPrefix: 'pd',
  accentColor: '#22c55e',
  version: '1.0.0',
  category: 'lifestyle',
  nav: {
    label: 'Plants',
    defaultRoute: '/plants',
    children: [
      { label: 'Gallery', route: '/plants' },
      { label: 'Care Calendar', route: '/plants/calendar', lucideIcon: 'Calendar' },
      { label: 'Rooms', route: '/plants/rooms', lucideIcon: 'Home' },
    ],
  },
  homeWidgets: [
    { id: 'plants-needing-care', component: 'PlantsNeedingCareWidget', span: 1, dataSource: 'pd_care_schedules' },
  ],
  tables: [
    { name: 'pd_locations', description: 'Rooms/locations for plants' },
    { name: 'pd_plants', description: 'Plant inventory' },
    { name: 'pd_care_schedules', description: 'Care action schedules' },
    { name: 'pd_health_logs', description: 'Plant health check logs' },
  ],
  settings: [
    { key: 'reminder_time', label: 'Care Reminder Time', type: 'text', defaultValue: '08:00' },
  ],
  sync: { strategy: 'direct' },
}
```

### DocuScan

```typescript
// skills/docuscan/manifest.ts
export const manifest: SkillManifest = {
  id: 'docuscan',
  displayName: 'DocuScan',
  icon: '📄',
  lucideIcon: 'ScanLine',
  dbPrefix: 'ds',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'productivity',
  nav: {
    label: 'Documents',
    defaultRoute: '/documents',
    children: [
      { label: 'Library', route: '/documents' },
      { label: 'Search', route: '/documents/search', lucideIcon: 'Search' },
    ],
  },
  homeWidgets: [
    { id: 'recent-scans', component: 'RecentScansWidget', span: 1, dataSource: 'ds_scans' },
  ],
  tables: [
    { name: 'ds_scans', description: 'Scanned document records with OCR text' },
  ],
  settings: [
    { key: 'auto_classify', label: 'Auto-Classify Documents', type: 'toggle', defaultValue: true },
  ],
  sync: { strategy: 'direct' },
}
```

### Home Fix-It

```typescript
// skills/home-fix-it/manifest.ts
export const manifest: SkillManifest = {
  id: 'home-fix-it',
  displayName: 'Home Fix-It',
  icon: '🔧',
  lucideIcon: 'Wrench',
  dbPrefix: 'hf',
  accentColor: '#f97316',
  version: '1.0.0',
  category: 'lifestyle',
  nav: {
    label: 'Home',
    defaultRoute: '/home-repair',
    children: [
      { label: 'Dashboard', route: '/home-repair' },
      { label: 'Appliances', route: '/home-repair/appliances', lucideIcon: 'Refrigerator' },
      { label: 'Repairs', route: '/home-repair/repairs', lucideIcon: 'Hammer' },
      { label: 'Maintenance', route: '/home-repair/maintenance', lucideIcon: 'CalendarClock' },
      { label: 'Tools', route: '/home-repair/tools', lucideIcon: 'Wrench' },
    ],
  },
  homeWidgets: [
    { id: 'maintenance-due', component: 'MaintenanceDueWidget', span: 1, dataSource: 'hf_maintenance_tasks' },
  ],
  tables: [
    { name: 'hf_home_profiles', description: 'Home details and skill level' },
    { name: 'hf_tool_inventory', description: 'Tool ownership tracking' },
    { name: 'hf_appliances', description: 'Appliance registry with warranty info' },
    { name: 'hf_repair_logs', description: 'Repair history and costs' },
    { name: 'hf_maintenance_tasks', description: 'Scheduled maintenance tasks' },
  ],
  settings: [
    { key: 'skill_level', label: 'DIY Skill Level', type: 'select', defaultValue: 'intermediate', options: [{ label: 'Beginner', value: 'beginner' }, { label: 'Intermediate', value: 'intermediate' }, { label: 'Advanced', value: 'advanced' }] },
  ],
  sync: { strategy: 'direct' },
}
```

### InvoiceGen

```typescript
// skills/invoicegen/manifest.ts
export const manifest: SkillManifest = {
  id: 'invoicegen',
  displayName: 'InvoiceGen',
  icon: '🧾',
  lucideIcon: 'FileSpreadsheet',
  dbPrefix: 'ig',
  accentColor: '#14b8a6',
  version: '1.0.0',
  category: 'finance',
  nav: {
    label: 'Invoices',
    defaultRoute: '/invoices',
    children: [
      { label: 'Dashboard', route: '/invoices' },
      { label: 'Clients', route: '/invoices/clients', lucideIcon: 'Users' },
      { label: 'History', route: '/invoices/history', lucideIcon: 'History' },
    ],
  },
  homeWidgets: [
    { id: 'outstanding-invoices', component: 'OutstandingInvoicesWidget', span: 1, dataSource: 'ig_invoices' },
  ],
  tables: [
    { name: 'ig_profiles', description: 'Business profile for invoice branding' },
    { name: 'ig_clients', description: 'Client directory' },
    { name: 'ig_invoices', description: 'Invoice records' },
    { name: 'ig_line_items', description: 'Invoice line items' },
  ],
  settings: [
    { key: 'default_terms', label: 'Default Payment Terms (days)', type: 'number', defaultValue: 30 },
    { key: 'invoice_prefix', label: 'Invoice Number Prefix', type: 'text', defaultValue: 'INV' },
    { key: 'tax_rate', label: 'Default Tax Rate (%)', type: 'number', defaultValue: 0 },
  ],
  sync: { strategy: 'direct' },
}
```

---

## Appendix A: Sidebar Organization

Skills are grouped by category in the sidebar. Within each category, skills are listed alphabetically.

```
📊 Dashboard Home
🔔 Notifications
─────────────────
FINANCE
  💰 Expenses
  💵 Budget
  📈 Stocks
  🧾 Invoices
─────────────────
PRODUCTIVITY
  🧠 Memory
  📝 Notes
  📄 Documents
  🔒 Security
  ☀️ Briefing
─────────────────
WORK
  📱 Content
  📧 Email
  💼 Job Hunt
─────────────────
HEALTH & WELLNESS
  🏥 Health
  🏋️ Training
─────────────────
LEARNING
  📚 Knowledge
  📚 Tutor
─────────────────
LIFESTYLE
  🍽️ Meal Planner
  ✈️ Travel
  👥 Relationships
  🌱 Plants
  🔧 Home
─────────────────
⚙️ Settings
```

## Appendix B: Utility Functions

```typescript
// lib/utils/cn.ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// lib/utils/format.ts
import { format, formatDistanceToNow, isToday, isYesterday } from 'date-fns'

export function formatCents(cents: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
  }).format(cents / 100)
}

export function formatDate(date: string | Date, pattern = 'MMM d, yyyy'): string {
  const d = typeof date === 'string' ? new Date(date) : date
  if (isToday(d)) return 'Today'
  if (isYesterday(d)) return 'Yesterday'
  return format(d, pattern)
}

export function formatRelative(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date
  return formatDistanceToNow(d, { addSuffix: true })
}

export function formatNumber(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
  return n.toLocaleString()
}

export function formatPercent(value: number, decimals = 1): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(decimals)}%`
}
```

## Appendix C: Package Dependencies

```json
{
  "dependencies": {
    "next": "^14.2.0",
    "@supabase/ssr": "^0.5.0",
    "@supabase/supabase-js": "^2.45.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "recharts": "^2.12.0",
    "@dnd-kit/core": "^6.1.0",
    "@dnd-kit/sortable": "^8.0.0",
    "@dnd-kit/utilities": "^3.2.0",
    "lucide-react": "^0.400.0",
    "date-fns": "^3.6.0",
    "zod": "^3.23.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.4.0",
    "class-variance-authority": "^0.7.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "tailwindcss-animate": "^1.0.0",
    "@types/node": "^20.14.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0"
  }
}
```

## Appendix D: Conflict Resolutions from Audit

This section documents how each conflict identified in the audit was resolved:

| Audit Finding | Resolution |
|---------------|-----------|
| Budget Buddy uses Vite, not Next.js | **Standardized to Next.js 14+ App Router.** Budget Buddy rebuilt as Next.js pages. |
| Budget Buddy has no DB schema | **Full Supabase schema created** (5 tables: bb_budgets, bb_transactions, bb_recurring, bb_savings_goals, bb_net_worth_snapshots). |
| InvoiceGen uses SQLite only | **Migrated to Supabase** with ig_ prefixed tables. user_id added for multi-tenancy. |
| Plant Doctor/InvoiceGen use PascalCase tables | **Converted to snake_case plural** (e.g., `Plant` → `pd_plants`, `LineItems` → `ig_line_items`). |
| Mixed UUID functions (gen_random_uuid vs uuid_generate_v4) | **Standardized to `gen_random_uuid()`** — native PostgreSQL, no extension required. |
| Text-based IDs (Knowledge Vault, NoteTaker) | **Switched to UUID PKs.** Custom display IDs stored in separate `slug` or `display_id` columns. |
| User identity fragmentation (6+ patterns) | **Standardized:** every table gets `user_id UUID NOT NULL REFERENCES auth.users(id)`. Household-based skills chain access through parent table. |
| Plant Doctor/InvoiceGen missing user_id | **Added `user_id` to all tables.** RLS policies applied. |
| 13 dark mode vs 7 light mode skills | **Dark mode only** for the unified shell. Per-skill themes possible via `accentColor` in manifest. |
| Chart.js vs Recharts split | **Standardized on Recharts** for all chart components. TradingView Lightweight Charts as specialized add-on for Stock Watcher. |
| Daily Briefing prefix `db` could collide | **Changed to `dbr`** to avoid ambiguity with "database" abbreviation. |
| Mixed RLS policy depth | **Standardized to per-operation policies** (SELECT, INSERT, UPDATE, DELETE) for all tables. |
| Missing updated_at on some tables | **Every table** gets `created_at` and `updated_at` with auto-update trigger. |
| No migration strategy anywhere | **Defined migration file convention** with numbered files per skill (§5.6). |
| Inter vs Manrope font | **Manrope as primary** (matches NormieClaw production site), Inter as fallback. JetBrains Mono for monospace. |

---

*End of specification. This document contains everything needed to build the NormieClaw unified dashboard from scratch. An agent reading this spec should be able to scaffold the entire project, create all database tables, implement the shared component library, register all 21 skills, and deploy to Vercel without any additional guidance.*