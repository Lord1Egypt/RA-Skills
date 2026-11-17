---
name: industry-evolution-3d
description: Turn any domain's "industry / technology / people evolution history" into an interactive 3D spatiotemporal graph web page — a world map as the base, a vertical time axis (year → height), nodes positioned by real lat/lon + year, hover-to-bring-to-front with detail cards. Use when the user wants "a timeline map / evolution graph / industry-layout visualization of domain X", or mentions an interactive web page combining "geo coordinates + time + nodes + hover cards". Feed it a JSON dataset and it generates a self-contained HTML.
agent_created: true
---

# 3D Industry-Evolution Spatiotemporal Graph Generator

Turn "the key milestones of a domain (AI, automotive, semiconductors, pharma, internet…)" into a rotatable, zoomable, hover-for-details 3D web page:
**world map as the base + a vertical time axis (year → height) + nodes placed by real lat/lon + person avatars / brand logos / event tetrahedra + hover-to-front with detail cards**.
The full logic was battle-tested in an "AI Industry History" project (hover cards hugging the node, oldest node raised off the ground, hover-to-front without being occluded). This skill parameterizes and generalizes that work.

## When to use
- The user wants "an evolution graph / timeline map / industry-layout visualization of domain X".
- The user provides a list with year / location (lat/lon or city) / type and wants an interactive web page.
- Unlike `wb-finance-skill` or `neodata-financial-search`: this skill focuses on **geo + time dual-axis visualization**, not data fetching.

## Workflow
1. **Collect data**: have the user provide a milestone list (or you research/complete it). Each item needs at least: `year`, `type`, `title`, `loc`, `lat`, `lon`, `desc`.
   - `type` is one of three: `person` (people/entrepreneurs, shows avatar), `product` (product/tech, shows logo or brand-colored abbreviation plate), `event` (event/conference, shows tetrahedron).
2. **(Optional) Images**: for people, `portraits: { pid: "image URL or local path" }`; for brands, `logos: { key: "image URL or path" }` and map `title` to `{ logo: key, color:"#hex", abbr:"abbr" }` in `brandMap`.
   - Optional: people degrade to an "initials disc", products degrade to a "brand color + abbreviation plate".
3. **(Optional) Map**: `map` takes a path or URL to an equirectangular/Mercator world-map PNG (inlined at generation). Leave empty for a solid-color base (still works, just no geographic basemap).
4. **Generate**:
   ```bash
   # generate.py auto-locates template.html in its own directory via __file__, no need to cd
   # Replace SKILL_DIR with the actual install path: user-level ~/.workbuddy/skills/industry-evolution-3d, or project-level <workspace>/.workbuddy/skills/industry-evolution-3d
   SKILL_DIR=~/.workbuddy/skills/industry-evolution-3d
   python3 "$SKILL_DIR/generate.py" "$SKILL_DIR/examples/ai_history_sample.json" /tmp/demo.html
   ```
   Dependencies: `pip install Pillow requests` (any python3: `python3 -m pip install Pillow requests`).
5. **Preview / Deploy**: double-click `index.html` locally to view; to share, use `workbuddy_cloudstudio_deploy` (directory contains index.html, port 3000).

## input.json schema
```jsonc
{
  "meta": {                      // required (year range must be present)
    "title": "Title",
    "subtitle": "Subtitle / notes",
    "yearMin": 1943, "yearMax": 2026,
    "axisBase": 10,              // time-axis start height above ground (prevents oldest node from hugging the floor, see lessons)
    "axisH": 120,                // total axis height (corresponds to yearMax)
    "mapWidth": 200, "mapDepth": 100
  },
  "map": "assets/world_map.png", // optional; path or URL; empty = solid-color base
  "yearTicks": [1940,1950,...,2026], // optional; defaults to decade ticks
  "milestones": [                // required, array
    { "year":1943, "type":"event", "title":"...", "loc":"Chicago, USA", "lat":41.88, "lon":-87.63, "desc":"..." },
    { "year":2012, "type":"person", "pid":"hinton", "initial":"GH", "title":"Geoffrey Hinton", "loc":"...", "lat":.., "lon":.., "desc":"..." },
    { "year":2022, "type":"product", "title":"ChatGPT (OpenAI)", "loc":"...", "lat":.., "lon":.., "desc":"..." }
  ],
  "portraits": { "hinton": "https://.../photo.jpg" },  // optional pid->image
  "logos": { "openai": "https://.../logo.svg" },        // optional key->image
  "brandMap": { "ChatGPT (OpenAI)": { "logo":"openai", "color":"#10a37f", "abbr":"GPT" } },
  "wiki":  { "Title": "https://en.wikipedia.org/wiki/..." }, // optional exact wiki link; defaults to wiki search
  "baike": { "Title": "https://baike.baidu.com/item/..." }   // optional; defaults to Baidu search
}
```

## Key design (verified, do not casually change)
- **Coordinate mapping**: `x=(lon/180)*(MAP_W/2)`, `z=-(lat/180)*MAP_D`, `y=AXIS_BASE + (year-YEAR_MIN)/(YEAR_MAX-YEAR_MIN)*(AXIS_H-AXIS_BASE)`.
- **Hover-to-front**: `setNodeActive` sets the hovered node's `renderOrder=1000` + `depthTest=false`, so it stays clickable and visible even when occluded by collapsed nodes.
- **Hover card**: `placeCard` uses `nodeScreenCenter(node)` to anchor the card `+14px` down-right of the **current node**, and only does viewport clamping — this is the user-approved baseline; do NOT add complex "avoid other nodes / keep fully visible" logic that pushes the card away (we hit that pitfall, see lessons).
- **Height above ground**: the oldest year must have `AXIS_BASE>0`, otherwise the tetrahedron/sprite sinks into the ground plane (a point the user explicitly wanted fixed).
- **Image inlining**: at generation, avatars/logos/map are base64-inlined, so the page opens offline; SVG is inlined as base64 directly, bitmaps are cropped to a circle (avatar) / shrunk (logo/map) via PIL.

## Boundaries / notes
- The geographic basemap defaults to a world map; for "non-geographic" domains (e.g. a pure timeline), leave `map` empty or swap in a custom basemap (flowchart/topology needs a different template).
- Too many nodes (>60) get crowded; consider splitting by sub-period or tuning `MAP_W/MAP_D`.
- Deploying to CloudStudio with the same sandbox id keeps the URL stable (see memU/deploy notes).

See `references/lessons.md` for the pitfalls we hit and the final solutions while getting this graph right.
