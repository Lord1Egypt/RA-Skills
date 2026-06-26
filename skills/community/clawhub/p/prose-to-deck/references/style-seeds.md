# Style Seeds

A style seed is a minimal constraint set — not a template.
It defines the boundaries of a visual direction, not the direction itself.

When a `style=<name>` parameter is passed at invocation, load the matching seed before Phase 3.
The seed narrows the search space; Phase 3 still requires full design judgment within that space.
Specific colors, fonts, motifs, and layout decisions remain the AI's responsibility — derived from
the content, not copied from the seed.

---

## Available Seeds

### `dark-precise`

**Background:** dark
**Tone:** precise, technical, forward-looking
**Avoid:** warm accent colors, decorative serif display fonts, soft/rounded atmosphere effects
**Good for:** technical articles, engineering retrospectives, data-heavy content

### `dark-warm`

**Background:** dark
**Tone:** intimate, weighty, personal
**Avoid:** cold blue/teal accents, clinical mono-heavy layouts
**Good for:** personal essays, career reflections, experience-sharing

### `light-editorial`

**Background:** light
**Tone:** authoritative, readable, open
**Avoid:** heavy atmosphere effects, dark overlays, neon accents
**Good for:** thought leadership, opinion pieces, long-form analysis

### `light-energetic`

**Background:** light
**Tone:** energetic, optimistic, action-oriented
**Avoid:** muted palettes, heavy serif typography, slow/minimal layouts
**Good for:** product launches, how-to guides, motivational content

---

## How to Use

1. At invocation, if `style=<name>` is present, read this file at the start of Phase 3.
2. Identify the matching seed. If no match, treat as if no seed was provided.
3. Use the seed's background and tone as hard constraints — do not override them.
4. Use the avoid list as a filter — eliminate directions that violate it before making your choice.
5. Everything else (palette values, typefaces, motifs, atmosphere) is still decided by content analysis.

The seed is a starting gate, not a finish line.

---

## Adding New Seeds

Seeds should be added when a recurring visual need isn't covered by existing options.
A seed is ready to add when you can describe it in 4 lines: background, tone, avoid, good-for.
If it takes more than that, it's a template — don't add it.
