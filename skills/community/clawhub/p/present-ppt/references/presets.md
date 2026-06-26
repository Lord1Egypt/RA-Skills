# Presets

## v9-architecture

Source file used during prototyping:
- `outputs/gartner-practical-evaluation-slide-v1/slide-01-practical-evaluation-system-v9.html`

Semantic regions:
1. topbar
2. title
3. core summary box
4. left driver panel
5. center layered architecture stack
6. right judgement chain

Important styling choices captured in code:
- wide layout (13.33 x 7.5)
- analyst-style muted palette
- rounded cards and light borders
- native text boxes instead of rasterized text
- arrow bridge between major columns

## ai-runtime-page

Source file used during prototyping:
- `outputs/gartner-ai-runtime-slide-v1/slide-04a-ai-runtime-v1.html`

Semantic regions:
1. header
2. lead box
3. state input chips
4. runtime title
5. main process modules
6. support cards
7. judgement output chips
8. base layer
9. takeaway

Important styling choices captured in code:
- analyst-style wide layout
- 5 equal-width process modules with chevron flow
- chip bands above and below runtime
- native text boxes instead of rasterized text

## data-strategy-deck

Used for multi-slide data strategy / cyberpunk-themed presentation decks.

Source file used during prototyping:
- `/Users/mk/workspace/ai/mk-present/test/data-strategy-deck.html`

Semantic regions (per slide type):
1. **title** — section label, huge title (DATA / STRATEGY), subtitle, status line
2. **stats** — section label, heading, body, 3 stat blocks with numbers
3. **agenda** — section label, numbered feature list with title + body
4. **definition** — section label, heading, body, 2-column comparison (NOT / IS)
5. **architecture** — section label, heading, house diagram (roof + 4 floors + foundation)
6. **pillars** — section label, heading, 2×2 pillar cards with accent top lines
7. **maturity** — section label, heading, 5-level maturity list
8. **assessment** — section label, heading, body, 3-column assessment
9. **roadmap** — section label, heading, 3 roadmap phases with time labels
10. **closing** — accent bar, title, subtitle, cursor line

Important styling choices captured in code:
- dark theme (background `#0A0A12`, muted text `#4A4E6A`)
- accent colors: blue `#3D5AFE`, purple `#7C4DFF`, cyan `#00E5FF`, pink `#FF1493`
- native text boxes using Verdana (headings) and Courier New (body/mono) as system-friendly substitutes for Orbitron / Space Mono
- per-slide page counter
- rounded rect cards with accent-colored top border lines

## Future preset ideas

- three-column analyst page
- single-column infographic page
- timeline / roadmap page

## Template for new presets

When adding a brand-new preset, start from:
- `scripts/preset_template.js`
- `scripts/layout_template.js`
- `references/preset-template.md`
