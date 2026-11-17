# Themes (vibes)

Themes are the styling lever. Same deck JSON + different theme = completely different look,
data intact. List installed themes at runtime with the `list_themes` MCP tool or
`npx @presentation-md/render --list-themes`.

**Alias cheat-sheet** (frontend-slides STYLE_PRESET names → package IDs):
`Neon Cyber` → `neon-noir` · `Terminal Green` → `crt-terminal` · `Swiss Modern` → `swiss-typographic`.
Full synonym lists live in `theme-selection-index.json` (`aliases` field). Use-case triples:
`theme-shortlists.json`.

| theme | vibe |
|-------|------|
| `claude` | Anthropic / Claude-inspired — warm cream paper, clay-coral accent, grotesk + editorial serif (bundled). |
| `default-tech` | Edgy tech startup — dark, violet + cyan, bold geometric sans (bundled). |
| `corporate` | Formal corporate — light, navy, restrained single accent, clean. |
| `playful` | Playful/creative — bright multi-color, rounded, big type. |
| `luxury-minimalist` | Ultra-luxury — near-black stage, cream serif, gold hairlines (Solstice). |
| `retro-arcade` | Retro 80s arcade — deep purple/black, magenta+cyan neon glow. |
| `editorial-serif` | Magazine editorial — warm cream paper, ink-black serif, crimson masthead. |
| `brutalist-mono` | Raw brutalist — concrete off-white, monospace, hazard-orange, zero radius. |
| `pastel-dreamy` | Soft pastel — lavender-blush, deep plum text, blush + periwinkle accents. |
| `aurora-glass` | Aurora glass — black void, Syne, violet + cyan (NovaSpark). |
| `ft-editorial` | FT broadsheet — cream newsprint, ink serif, blue + red signal. |
| `genz-bento` | Gen-Z bento — coral + lime stickers, hard offset shadows. |
| `crt-terminal` | CRT terminal / Terminal Green — cream type, phosphor green accents (RetroNet). |
| `swiss-typographic` | Swiss Modern / Swiss grid — white, Inter, signal red, zero radius (Grid Systems). |
| `candy-pop` | Candy pop — cream, hot pink + jellybean blue, Fredoka (Jellybean). |
| `aerospace-hud` | Aerospace HUD — navy, cyan, orange, Barlow Condensed (Axiom). |
| `brutalist-acid` | Dark acid brutalist — near-black, electric lime, Space Mono (MONOLITH). |
| `bauhaus` | Bauhaus — cream #f4f1ea, red #e63946 + blue #1f4ae0 (Primary). |
| `y2k-aero` | Y2K aero — icy sky + lime bubbles, Nunito (BubbleFlow). |
| `risograph-zine` | Risograph zine — kraft, red + blue overprint (Inkwell). |
| `neon-noir` | Neon Cyber / Neon noir — #050510 night, pink + cyan, Orbitron (Neon District). |
| `vaporwave` | Vaporwave — #1a0533 dusk, #ff6ad5 + #5ce1ff, Monoton (Mallsoft). |
| `botanical-luxe` | Botanical luxe — forest #1d3a2f, gold #bfa55a (Verdant). |
| `heritage-editorial` | Heritage editorial — parchment, terracotta, Playfair (Atelier). |
| `fintech-clean` | Fintech clean — white, violet + mint, Inter (Ledgerline). |
| `developer-dark` | Developer dark — GitHub night, green + blue (Forge). |
| `data-editorial` | Data editorial — white report, navy + red (Signalbox). |
| `scandinavian` | Scandinavian — linen, sage + clay, Fraunces (Hygge). |
| `art-deco` | Art Deco — emerald, gold leaf, Cinzel (Meridian Club). |
| `kinetic-wrapped` | Kinetic Wrapped — black + acid lime (Pulse). |
| `blueprint` | Blueprint — navy, cyan engineering grid (Apsis). |
| `glassmorphism` | Glassmorphism — icy mist, indigo + cyan (CloudPeak). |
| `broadsheet` | Newspaper broadsheet — newsprint, ink masthead (Daily Ledger). |
| `soft-editorial` | Soft Editorial — paper #F2EEDF, ink #2A241B, sage #B7C7A8 + blush #E1A4C2, Cormorant Garamond + Work Sans. |
| `editorial-forest` | Editorial Forest — cream #efe7d4, forest #2e4a2a + dusty rose #e89cb1, Source Serif 4 + JetBrains Mono. |
| `pin-and-paper` | Pin & Paper — legal pad #EFE56A, cobalt #1F3A8A, Space Grotesk + Caveat. |
| `vellum` | Vellum — periwinkle #2A3870, chartreuse #E8D85C, italic Cormorant Garamond + DM Sans. |
| `neo-grid-bold` | Neo-Grid Bold — putty #ECECE8, lemon #E6FF3D, Space Grotesk uppercase + JetBrains Mono. |
| `editorial-tri-tone` | Editorial Tri-Tone — pink #F2B6C6, butter #F2D86A, burgundy #7A1F35, Bricolage Grotesque + Instrument Serif. |
| `creative-mode` | Creative Mode — cream #EFE9D9, ink #0F0F0F, green #1F8A4C + pink #F06CA8, Archivo Black + Space Grotesk. |
| `broadside` | Broadside — ink #111111, fire orange #E85D26, cream #F0ECE5, Barlow 900 + IBM Plex Mono. |
| `bold-signal` | Bold Signal — #1a1a1a dark, orange card #FF5722, Archivo Black + Space Grotesk. |
| `notebook-tabs` | Notebook Tabs — page #f8f6f1 on outer #2d2d2d, Bodoni Moda + DM Sans, pastel tabs. |
| `creative-voltage` | Creative Voltage — electric blue #0066ff, dark #1a1a2e, neon #d4ff00, Syne + Space Mono. |
| `signal` | Signal — cream #F0ECE3 / navy #1C2644, gold #C8A870, Source Serif 4 + DM Sans. |
| `electric-studio` | Electric Studio — white + #4361ee blue split, Manrope 800, high-contrast studio panels. |
| `dark-botanical` | Dark Botanical — #0f0f0f void, warm #d4a574/#e8b4b8 accents, Cormorant + IBM Plex Sans. |
| `pastel-geometry` | Pastel Geometry — sky #c8d9e6, card #faf9f7, vertical pastel pills, Plus Jakarta Sans. |
| `split-pastel` | Split Pastel — peach #f5e6dc / lavender #e4dff0 split, Outfit, mint/yellow/pink badges. |
| `vintage-editorial` | Vintage Editorial — cream #f5f3ee, Fraunces display + Work Sans, witty bordered CTAs. |
| `paper-ink` | Paper & Ink — cream #faf9f7, charcoal #1a1a1a, crimson #c41e3a, Cormorant Garamond + Source Serif 4. |
| `biennale-yellow` | Biennale Yellow — parchment #E9E5DB, sun #F1EE2E, indigo #1B2566, Instrument Serif + Archivo. |
| `bold-poster` | Bold Poster — white canvas, ink #1C1410, tomato #D8000F, Shrikhand + Libre Baskerville. |
| `coral` | Coral — cream #F5F0E8 + coral #E85D5D on ink, Bebas Neue + Inter. |
| `emerald-editorial` | Emerald Editorial — emerald #3CD896, navy #0F1A5C, Bodoni Moda + Manrope. |
| `sakura-chroma` | Sakura Chroma — cream cassette paper, chroma stamps, Big Shoulders Display. |
| `pink-script` | Pink Script — near-black, hot pink #ED3D8C, DM Serif Display. |
| `block-frame` | BlockFrame — neobrutalist pastel blocks, Inter 900 + hard black borders. |
| `capsule` | Capsule — bone cream pills, Bodoni Moda + Space Grotesk candy palette. |
| `cobalt-grid` | Cobalt Grid — graph paper #F0EBDE, cobalt #1F2BE0, Newsreader. |
| `8-bit-orbit` | 8-Bit Orbit — navy void, neon cyan/pink/yellow, Tektur + Chakra Petch. |
| `mat` | Mat — sage #232E26, cream type, burnt orange #C07030, Bricolage + DM Sans. |
| `retro-zine` | Retro Zine — khaki #C8B99A, green #008F4D, Bebas Neue + Caveat. |
| `daisy-days` | Daisy Days — cream pastels, Fredoka One, charcoal-outlined stickers. |
| `blue-professional` | Blue Professional — cream #FDFAE7, cobalt #1E2BFA, Space Grotesk + Inter. |
| `monochrome` | Monochrome — ivory #FAFADF, ultra-light Jost, Lora italic quotes only. |
| `cartesian` | Cartesian — sandstone #EDE8E0, Playfair, 1px taupe draft lines. |
| `stencil-tablet` | Stencil & Tablet — bone #E2DCC9, Stardos Stencil, earth tablet blocks. |
| `long-table` | Long Table — cream #FAF1E2, rust #B53D2A, Bricolage + Fraunces italic. |
| `raw-grid` | Raw Grid — white canvas, 3px black borders, blush/sage fills, system sans 900. |
| `retro-windows` | Retro Windows — Win95 gray chrome, navy title bar, Press Start 2P accents. |
| `peoples-platform` | People's Platform — cream paper, cobalt/amber, Alfa Slab + red shadow. |
| `scatterbrain` | Scatterbrain — cream cork, sticky pastels, Shrikhand + Caveat. |
| `grove` | Grove — forest #192B1B, cream #D4CFBF, rust #C8524A, Playfair + Jost. |
| `studio` | Studio — near-black #1C1C1C, acid yellow #F5D200, Barlow 900 + IBM Plex Mono. |

Install more: `npm i @presentation-md/theme-<name>` (or the PyPI mirror
`presentation-md-theme-<name>`). Scaffold your own: `npx @presentation-md/create-theme`.

## Brand import

Generate a theme from an existing brand instead of hand-picking colors:

```
npx @presentation-md/create-theme --from-url https://acme.com
npx @presentation-md/create-theme my-theme-name --from-css ./brand.css
```

Extracts `:root` CSS variables and font declarations (falling back to a headless-browser
computed-style read when a site has no CSS custom properties — most real marketing sites don't).
Maps whatever's found onto the theme's 8 semantic roles and runs a WCAG contrast-safety pass, so
the result stays legible even when the raw brand colors wouldn't be. The CLI reports its
extraction source and any contrast adjustments it made. Also available as the `import_brand_theme`
MCP tool for agent-driven workflows.
