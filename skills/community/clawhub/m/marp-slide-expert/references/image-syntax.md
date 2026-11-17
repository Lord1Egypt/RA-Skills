# Image Syntax in Marp

Marp's image handling is one of the most common sources of layout bugs. Reference: [marpit.marp.app/image-syntax](https://marpit.marp.app/image-syntax).

## TL;DR

**Every image in marp must use the `![bg ...]` syntax.** There is no inline image sizing. If you want it visible, it is a background — that's the only option.

## Single background image

```markdown
![bg](image.jpg)               <!-- Full slide background -->
![bg left](image.jpg)          <!-- Left half, image takes its natural ratio -->
![bg right](image.jpg)         <!-- Right half -->
![bg left contain](image.jpg)  <!-- Left half, contained (preserves aspect, fits) -->
![bg right:60%](image.jpg)     <!-- Right 60% of slide -->
![bg opacity:.5](image.jpg)    <!-- Background with 50% opacity overlay -->
```

Combine freely:
```markdown
![bg left contain opacity:.9](<image with spaces.png>)
```

## Multiple background images

Each `![bg]` declaration stacks. The last one is on top. Images arrange by default:

```markdown
![bg](a.png) ![bg](b.png) ![bg](c.png)
```
→ horizontal row, equal widths.

Use the `vertical` keyword on the first image to flip to a column stack:

```markdown
![bg vertical](a.png) ![bg](b.png) ![bg](c.png)
```
→ vertical column.

## Mixed text + multiple images (split layout)

When you want content on one side and images on the other:

```markdown
![bg right vertical](a.png)
![bg](b.png)

# Title

Content text goes here. Marp shrinks the content area
to fit the space not covered by `bg right`.
```

Reading order:
1. First `![bg right vertical](a.png)` — first image takes the right column, will stack vertically with subsequent right-column images.
2. Second `![bg](b.png)` — fills the remaining left area as a background.
3. Content overlays on top, in the space not covered by the first image.

This is the canonical pattern for "show a screenshot on the right with explanatory text on the left."

## Choose horizontal vs vertical by image orientation

For a deck of mixed-orientation screenshots, decide per slide:

| Orientation | Ratio (w/h) | Arrangement |
|---|---|---|
| Landscape | > 1.2 | Default horizontal row works fine |
| Portrait | < 0.85 | Add `vertical` keyword |
| Square | 0.85 – 1.2 | Either; horizontal row usually reads better |

For a typical screenshot-heavy deck (most slides are 1920×1080 → landscape), the default `![bg]` row is correct almost everywhere. Use `vertical` only for portrait phone screenshots or tall diagrams.

## Path escaping

Paths with spaces, non-ASCII characters, or special chars MUST be wrapped in `<...>`:

```markdown
![bg](<path with spaces.png>)
![bg](<non-ascii path/image.jpg>)
![bg](<path(with)parens.png>)
```

Without the brackets, marp truncates the URL at the first space and silently fails to find the file (showing as text in PDF).

## Anti-patterns to avoid

- ❌ `![w:60% center](image.jpg)` — **not supported by marp**, shows as text.
- ❌ `![width:200px](image.jpg)` — also not supported in marp.
- ❌ `<img src="..." width="600">` — HTML img tags are ignored by marp.
- ❌ `![bg left w:60%](image.jpg)` — `bg left/right` and `w:` are not combinable; use `bg left:60%` instead if needed.

If a layout truly needs an inline image (e.g., a small icon next to text), the workaround is to use a background image with extreme transparency and place the text on top. But for most cases, restructure as text + background image.
