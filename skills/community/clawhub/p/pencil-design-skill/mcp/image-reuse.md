# Asset Reuse

> **Applies to**: Mode B (MCP Tools)
> **See also**: [component-reuse.md](../references/component-reuse.md) · [screenshot-qa.md](screenshot-qa.md)

---

## Core Principle: Search Before Generate

> **Inspired by Stitch** — Stitch emphasizes **efficiency and reuse**: avoid reinventing the wheel, maintain brand consistency through existing assets, and accelerate the path from idea to implementation. Regenerating a logo every time is a direct violation of this principle.

AI image generation is non-deterministic. Every generation produces a different result. If one screen already has a logo and you generate a new one for another screen, you end up with two different brand identities — design loses consistency.

The same applies to:
- Product images reused across screens
- Illustrations or decorative graphics
- Brand elements (logos, wordmarks, icons)
- Profile photos or avatars appearing in different contexts

---

## Workflow: Discover and Reuse Assets

### Step 1 — Search for Existing Assets

**Before generating any image**, search the document first:

```
pencil_batch_get({
  filePath: "path/to/file.pen",
  patterns: [
    { name: "logo" },
    { name: "brand" },
    { name: "icon" },
    { name: "image" }
  ],
  searchDepth: 5
})
```

Or search by node type:

```
pencil_batch_get({
  filePath: "path/to/file.pen",
  patterns: [{ type: "frame", name: "logo|brand|hero" }],
  searchDepth: 5
})
```

### Step 2 — Copy the Existing Asset

When found, use the Copy operation — not regeneration:

```javascript
// Copy logo from another artboard into the current screen
logoCopy=C("existingLogoNodeId", "targetParentId", { width: 120, height: 40 })
```

`C()` preserves the original image fill, styling, and structure.

If the logo lives inside a reusable Header component, insert the whole component:

```javascript
header=I("screenId", { type: "ref", ref: "HeaderComponent", width: "fill_container" })
```

### Step 3 — Adjust Size

```javascript
U("copiedLogoId", { width: 100, height: 32 })
```

**Always maintain aspect ratio** — never stretch or distort.

---

## When to Generate New Images

Only use `G()` to generate in these cases:

| Condition | Description |
|-----------|-------------|
| No similar asset in the document | Confirmed via search |
| Image is unique to this screen | Specific hero photo, unique illustration |
| Building the first screen | No assets exist yet |

```javascript
// Only when no existing asset matches
heroImg=I("heroSection", { type: "frame", name: "Hero Image", width: "fill_container", height: 400 })
G(heroImg, "stock", "modern office workspace")
```

---

## Strict Rules for Logos

Logos have the strictest reuse requirements:

1. **ALWAYS search first** — if any other screen has been designed, a logo almost certainly already exists
2. **ALWAYS copy** — never regenerate an existing logo; generated logos will never match
3. **Maintain proportions** — scale proportionally, never stretch
4. **Check inside components** — the logo may be inside a reusable Header/Navbar component

---

## Decision Tree

```
Need an image or logo?
│
├── Is it a logo or brand element?
│   ├── Already exists in the document? → COPY IT
│   └── First screen, nothing exists yet? → Generate or ask user for asset
│
├── Is it a product photo or hero image?
│   ├── Same image used on another screen? → COPY IT
│   └── Unique to this screen? → Generate with G() or use stock
│
└── Is it an icon?
    ├── Already in design system components? → Use ref instance
    └── Need a new icon? → Use icon_font type or generate
```

---

## Pre-Generation Checklist

- [ ] Searched for existing logos and images with `pencil_batch_get`?
- [ ] Used name patterns like `logo`, `brand`, `image`, `hero` in the search?
- [ ] Checked if reusable components (Navbar, Header) contain a logo?
- [ ] Copying existing assets rather than regenerating?
- [ ] For logos specifically: **absolutely confirmed** no logo exists in the document?

---

## See Also

- [component-reuse.md](component-reuse.md) — Check reusable components that may contain logos/icons
- [screenshot-qa.md](screenshot-qa.md) — Verify copied assets are placed correctly
