---
name: gld_ue_template
description: Unified Design and Interaction Standard Template for EPC Management System, complete React + Ant Design (JavaScript) project template and interactive specification documentation.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins:
        - node
        - npm
      install:
        - npm install
    homepage: https://github.com/your-org/gld_ue_template
---
# gld_ue_template

Unified Design and Interaction Standard Template for EPC Management System.
This SKILL provides a complete React + Ant Design (JavaScript) project template and interactive specification documentation.

## 1. Design System Specifications

### 1.1 Color System

**Primary Colors (主色)**
- Primary Blue: `#3c83f8` (Brand color, active states, primary buttons)
- Blue Hover: `#5995f9`
- Blue Active/Click: `#2b6bd9`
- Blue Soft: `#ecf3ff` (Backgrounds for active items)

**Functional Colors (功能色)**
- Success Green: `#46bc46` (Success states, positive metrics)
- Warning Orange: `#f7c03e` (Warning states, medium risk)
- Danger Red: `#ef5f59` (Error states, high risk, negative metrics)
- Purple: `#a855f7` (Categorization, special items)

**Neutral Colors (中性色)**
- Page Background: `#E9F2FB`
- Surface (Cards/Panels): `#ffffff`
- Surface Soft: `#fafafa`
- Line/Border: `#dfdfdf`
- Line Soft: `#e5e5e5`
- Text Main: `#262626`
- Text Sub: `#595959`
- Text Faint: `#8c8c8c`

### 1.2 Typography System

**Font Family**
`"PingFang SC", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`

**Font Sizes & Weights**
- Base Size: `14px` (Regular 400)
- Page Title: `24px` (Bold 700)
- Section Title: `16px` (Medium 450/500)
- Metric Value: `34px` (Medium 450/500)
- Small Text/Meta: `12px` (Regular 400)

**Line Heights**
- Tight: `1.2`
- Normal: `1.5`
- Relaxed: `1.8`

### 1.3 Spacing & Layout System

**Spacing Scale**
- xs: `4px`
- sm: `8px`
- md: `16px`
- lg: `24px`
- xl: `32px`
- 2xl: `48px`

**Border Radius**
- sm: `2px`
- md: `4px`
- lg: `8px`
- Cards/Panels: `12px` or `14px`
- Pills/Badges: `16px` or `50%`

**Shadows**
- sm: `0 1px 2px rgba(0, 0, 0, 0.05)`
- md: `0 4px 6px rgba(0, 0, 0, 0.1)`
- lg: `0 10px 15px rgba(0, 0, 0, 0.15)`
- hover: `0 8px 25px rgba(0, 0, 0, 0.2)`

## 2. Navigation System Standards

### 2.1 Global Navigation (Top Header)
- Represents first-level menus.
- Default first item is "首页" (Home).
- Header height: `54px`, rounded corners (`30px`), gradient background (`linear-gradient(90deg, #ffffff 0%, #eef5ff 76%, #dcecff 100%)`).

### 2.2 Secondary Navigation (Left Sidebar)
- "首页" (Home) has **NO** secondary left sidebar menu. The content area takes full width.
- All other first-level menus have 2/3 level nested left sidebar menus.
- Parent items in the sidebar are **only navigation groups** (click to expand/collapse).
- Only final level navigation items correspond to actual page routes.
- Active state styling: Background `#fff3e6`, Text `#f0932b`, Font Weight `450`.

### 2.3 Breadcrumb Navigation
- **Component**: Located in `src/components/Breadcrumb.jsx`.
- **Functionality**: Automatically generates breadcrumbs by parsing the current route path.
- **Mapping**: Uses a `breadcrumbMap` object to map URL segments to their display names.
- **Styling**:
  - Container (`.crumb-row`): Flex layout with a `6px` gap and `10px` bottom padding.
  - Items (`.breadcrumb`): Uses `text-faint` color. Hovering changes the color to the brand primary blue.
  - Current Page: Marked with the `current` class, uses `text-main` color, `600` font weight, and is not a link.
  - Separators: Displays a `/` character between items.
- **Integration**: Included by default in `SidebarLayout`.

## 3. Component Specifications

### 3.1 Buttons
- **Primary Button**: Background `#3c83f8`, Text `#fff`, Border Radius `4px`, Height `32px`.
- **Ghost Button**: Background `#fff`, Text `#595959`, Border `#dfdfdf`, Height `32px`. Hover: Border `#5995f9`, Text `#5995f9`.

### 3.2 Tags & Badges
- **Blue Tag**: Color `#3c83f8`, Background `#ecf3ff`.
- **Orange Tag**: Color `#f7c03e`, Background `#fff9f2`.
- **Green Tag**: Color `#46bc46`, Background `#f7fff2`.
- **Red Tag**: Color `#ef5f59`, Background `#fff2f4`.
- **Gray Tag**: Color `#8c8c8c`, Background `#f2f2f2`.

### 3.3 Metric Cards
- White background, `12px` border radius, `1px` solid `#e5e5e5` border.
- Header with label and icon tile (`32x32px`, `10px` radius).
- Large value text (`34px`, `#0f348c` or status color).
- Footer with muted description text.

### 3.4 Tables
- Header: Background `#f6faff`, Text `#595959`, Font Weight `600`, Border Bottom `#e5e5e5`.
- Body: Text `#595959`, Border Bottom `#e5e5e5`. Hover Background `#ecf3ff`.
- Category Rows: Background `#f3f7ff`, Font Weight `450`, Left border indicating category color.

### 3.5 Modals
- Overlay: `rgba(0,0,0,0.45)`.
- Content: Background `#fff`, Border Radius `12px`, Max Width `800px`.
- Header: Title `16px` Medium, Close button.
- Animation: `modalIn 0.2s ease-out` (scale 0.95 to 1, opacity 0 to 1).

## 4. How to Use This Template

When a user requests to create or modify a frontend project using this standard:

1. **Initialize Project**: Copy the contents of the `template` directory to the target project folder.
2. **Install Dependencies**: Run `npm install` (React 18, Ant Design 5.x, React Router v6, Chart.js).
3. **Follow Navigation Rules**: Ensure "首页" has no sidebar, and other sections use the nested sidebar structure.
4. **Use Provided Components**: Utilize the pre-built layout and UI components to maintain 100% design consistency.
5. **No TypeScript**: Write all code in JavaScript (`.js` / `.jsx`).

## 5. Template Structure

The `template` directory contains a complete React application:
- `src/App.jsx`: Routing configuration.
- `src/layouts/`: GlobalLayout, SidebarLayout.
- `src/pages/`: Home, ListManagement (Demo pages).
- `src/components/`: Reusable UI components (MetricCard, Tag, etc.).
- `src/styles/`: Global CSS variables and overrides.
