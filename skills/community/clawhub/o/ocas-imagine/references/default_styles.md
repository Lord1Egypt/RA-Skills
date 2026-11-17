# Default Styles Library

Index of predefined Style Prompts. Each style is a self-contained aesthetic system with its own color palette, rendering rules, compositional logic, and emotional register — maintained in its own file.

When Flow 1 step 1 directs "retrieve a style definition from `references/default_styles.md`," read the target style's individual file from the list below. Do not try to pull multiple styles from this index file.

| Style | File | TL;DR |
|---|---|---|
| SOMA | [`soma.md`](./soma.md) | Thermal imaging of a memory you're not sure you had — blurred luminous gradient painting, peach/lavender/coral/cyan/mint, no edges. |
| NOIR | [`noir.md`](./noir.md) | Twilight insomnia in a city that never fully darkens — flat vector silhouettes, coral + olive-gray + near-black, oversized low sun. |
| HIRO | [`hiro.md`](./hiro.md) | Modern woodblock print — flat naturalistic colors with misregistration and paper grain, extreme negative space, deadpan observational. |
| COMIC | [`comic.md`](./comic.md) | Two inks on cheap paper, looking straight down — hand-drawn ink linework on warm peach-orange ground, one accent color, bird's-eye view. |
| CANDY | [`candy.md`](./candy.md) | A painting you can't quite focus on, interrupted by color that doesn't explain itself — soft plein-air landscape behind sharp opaque color fields. |
| VAPORWARE | [`vaporware.md`](./vaporware.md) | Akira meets Marty McFly in Brazil (1985) — photoreal speculative consumer electronics, cream + safety orange, soft studio light. |
| NEON-SEAMS | `styles.jsonl` (user-created) | the agent's asset style — violet/iridescent form self-luminous against near-black void, outer edge dissolving into glitch particles + neon seams. Routes via gentube (skill gentube-image-gen). |

## Adding a new default style

Default styles live under `references/` as `{name}.md` (lowercase). Follow the section shape used by the existing files (TL;DR + five-to-eight labeled sections drawn from: Era, Color Palette, Rendering Style, Lighting, Form/Figure Treatment, Composition & Framing, Surface & Texture, Mood & Narrative Tone). Add a row to the index table above. User-created styles belong in `~/openclaw/data/ocas-imagine/styles.jsonl`, not here.
