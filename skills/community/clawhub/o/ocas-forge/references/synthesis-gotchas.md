# Synthesis Gotchas

## Don't Just Sample — Consume Exhaustively

When asked to audit, synthesize, or build from a large reference library, don't read a handful of files and extrapolate. Read deeply across all categories. The user explicitly called this out: "don't just sample consume everything." For large libraries (e.g., 270+ design files), read representative files from EVERY category, not just 2-3. The value of a synthesis is proportional to the coverage of the source material.

**Rule**: For any synthesis task involving 50+ source files, read at minimum one file from each major category or subcategory. If there are 11 categories, read from all 11. Skipping categories produces gaps that undermine the entire synthesis.

## Dynamic Color Systems Over Hardcoded Palettes

When building a design system, prefer a model where colors derive from a small set of cue colors (e.g., 3 cues: background, accent hue, danger hue) via systematic HSL lightness/saturation shifts. Hardcoded hex palettes are brittle — changing a theme requires updating dozens of values. A dynamic model means changing one hue propagates everywhere: surfaces, text hierarchy, interactive states, dark mode, badges, focus rings.

**Pattern**: Define cue colors as HSL. Document derivation rules (e.g., "accent-hover = HSL(h, s, l - 4%)"). Provide a pre-computed `values:` section with hex values for agents to use directly, but make the derivation logic the source of truth. When the user asks to retheme, change only the cue values and recompute.

**Baseline's specific model**: 3 cue colors (background white, accent blue H:221 S:71% L:53%, danger red H:0 S:68% L:47%). Semantic colors (success/warning) are fixed hues that don't shift with accent. Dark mode inverts the luminance scale (surfaces go dark, text goes light, accent gets +4% lightness). Chart palette derived via hue rotation from accent (+30° increments). All documented in `references/design/BASELINE.md`.

**Baseline's motion system** (§5 of BASELINE.md): 5 duration tokens (0.08s–1.0s), 4 easing tokens, 5 spring presets (snappy/gentle/bouncy/instant/release), distance and scale tokens. All motion must use these tokens — no hardcoded durations or inline stiffness/damping. Use `motion/react` only, never `framer-motion`. Always respect `prefers-reduced-motion`. Full spec at `references/design/BASELINE.md` §5 and the standalone `design-references` skill.

**Baseline's glass system** (§6 of BASELINE.md): 3 glass variants (regular/clear/identity), CSS patterns for web adaptation, glass+motion pairings, accessibility rules. Glass is for navigation/controls only — never on content. Never mix variants in one interface. Full spec at `references/design/BASELINE.md` §6 and the standalone `design-references` skill.

## Frontend Design References

When building any skill that produces or evaluates frontend UI, load these references:

1. **BASELINE.md** (`references/design/BASELINE.md`) — the canonical design system. §5 for motion tokens/springs, §6 for glass/translucency, §9 for complete CSS custom properties.
2. **design-references** skill (`skill_view(name='design-references')`) — consolidated motion+glass reference with raw source files from motion-foundations, motion-vue, and liquid-glass-design agent skills.
3. **Taste-skill anti-slop rules** (`~/.hermes/references/design/taste-skill/anti-slop-rules.md`) and **pre-flight checklist** (`~/.hermes/references/design/taste-skill/anti-slop-preflight.md`) — canonical AI-frontend anti-pattern references.

## External Skill Dependencies

| Skill | When to load |
|-------|-------------|
| `design-references` | When building any skill that produces animated UI, glass/translucency effects, or frontend component patterns. Consolidates motion-foundations, motion-vue, and liquid-glass-design. |
| `hyperframes` | When building video compositions, animated title cards, or HTML-to-video pipelines. Uses GSAP for animation — motion tokens from BASELINE apply. |

## Stack References Need Full Coverage

When building a stack reference (e.g., frontend libraries), don't leave major categories empty. If the design system will be used for dashboards, include data visualization libraries. If it will be used for forms, include form libraries. A stack reference that omits visualization because "it wasn't asked about explicitly" is incomplete — the user expects comprehensive coverage of all frontend domains they might need.