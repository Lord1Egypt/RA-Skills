## Workflows

### Workflow A: inspect before editing

Before any edit:

- inspect the project
- inspect the target screen
- verify whether the screen is actually generated content

Practical heuristic:

- if `htmlCode` exists, the screen is more likely to be safely editable
- if the target is only an uploaded image or reference asset, do not assume `edit_screens` will behave well

### Workflow B: generate first, then refine

For new directions:

1. create or choose the right project
2. if a reusable design system exists, pass it explicitly to generation or apply it to target screens before major sibling-screen work
3. generate a first screen with the minimum safe parameter set
4. review output quality
5. move to small edits rather than repeating large generation prompts

Default safe starting point: `projectId` + a short, structured prompt. Then add `deviceType` or `modelId` only when there is a reason.

### Workflow B1: preview-first approval loop

Use this for any workflow that may end in code retrieval:

1. generate or edit one candidate screen
2. retrieve and review the visual output first (`fetch_screen_image` when available, otherwise equivalent visual artifact)
3. gather explicit user approval or precise revision instructions
4. repeat until one direction is clearly accepted
5. only then retrieve code (`fetch_screen_code` when available) or move to export

If an edit returns a different screen id, treat the returned screen as the new candidate and inspect that screen before further edits. Do not keep editing the older source screen by accident.

### Workflow B1.5: extract the handoff pack

Use this immediately after approval, before implementation work starts:

1. retrieve the accepted screen with `get_screen`
2. capture or save the screenshot artifact referenced by `screenshot.downloadUrl`
3. capture or save the exported HTML referenced by `htmlCode.downloadUrl` when present
4. keep the project `DESIGN.md` / design-system definition with the same pack
5. record the screen id, width, height, and device type next to those artifacts

This pack is the minimum reliable handoff bundle for coding agents.
If `htmlCode` is absent, continue with screenshot + design system + screen metadata and treat implementation as visual translation rather than export translation.

### Workflow B2: greenfield app bootstrap from Stitch exports

Use this when the product is new enough that there is no meaningful coded UI to preserve yet.

1. generate the canonical screen family in Stitch first
2. get explicit acceptance on the direction before broad implementation
3. if code or HTML export is available in the active environment, download it
4. read the export completely before rewriting anything
5. translate the exported structure into the target stack instead of eyeballing screenshots
6. keep the layout system, spacing logic, token choices, and section structure where they are sound
7. replace hardcoded content and brittle markup gradually, not all at once
8. add the real app concerns after translation: data flow, typing, state, accessibility, dark mode, tests

Use this path especially when:

- the app is being built from scratch
- Stitch generated a strong screen family quickly
- the main value is the concrete composition, hierarchy, and token choices
- recreating the same layout manually would be slower and less faithful

Do not treat the export as production-ready final code. Treat it as a high-fidelity implementation seed.

### Workflow B3: Flutter or native-app translation path

Use this when the destination is Flutter, React Native, SwiftUI, Jetpack Compose, or another non-DOM UI stack.

Follow this implementation loop:

1. inspect the target app shell, navigation, theme, component structure, and repo rules before writing code
2. create or retrieve the route-specific Fidelity Pack: accepted screenshot, screen metadata, design system, and exported code artifact when available
3. extract tokens from the design system/export into the target theme first: colors, typography roles, spacing, radii, borders, shadows
4. implement reusable native primitives before the screen: surface/card, large number, selector pill, entity row, favorite/action affordance, ad/empty placeholder
5. implement one approved screen at a time inside the existing app architecture
6. run the target repo's normal verification command
7. capture a real device/viewport screenshot and compare it to the Stitch reference
8. write a drift list: `missing`, `mismatched`, `intentional`; fix high-impact drift with scoped patches only

Native translation rules:

- keep the app shell, navigation structure, and platform conventions in the target app
- treat Stitch HTML/CSS as a structural reference, not as code to port literally
- translate one approved screen at a time into native layout primitives
- map `DESIGN.md` roles into app theme tokens before building large widgets
- preserve hierarchy, spacing rhythm, card geometry, and numeric emphasis first
- rebuild states that matter for the product, not only the happy-path screenshot
- compare the native result against the accepted screenshot and log `missing`, `mismatched`, `intentional`

For Flutter specifically, the normal target is quality parity, not DOM parity. Recreating the accepted visual system and interaction hierarchy matters more than copying the exported HTML structure line by line.

Flutter implementation note:
- Do not nest a second `Scaffold` inside an existing app shell unless that is the app's established pattern. A nested scaffold can make bottom navigation, safe areas, or overlays drift from the Stitch reference.
- Compare against a real simulator/device screenshot after the first pass. Stitch's mobile canvas may have more vertical space than the actual device once system status bars and app navigation are present.

### Workflow C: full-app redesign

For an existing product redesign:

1. create a dedicated Stitch project
2. define the main screen families
3. generate one canonical screen per family
4. refine those canonical screens with preservation-first prompts
5. only then add alternate states and edge cases
6. move to code after the family set is coherent

This is slower than opportunistic one-off generation, but it reduces design drift.

### Workflow D: reference-driven redesign

When redesigning a real app:

- gather reliable reference captures first
- work one screen family at a time
- name the relevant reference images explicitly in the prompt
- treat those references as the source of truth for current structure

Good pattern:

```text
Use the uploaded real app references in this project.
The relevant images are named today_top.png, today_day_actions.png, and today_meals_mid.png.
Those images show what exists now.
Keep the real structure and improve only hierarchy, spacing, and polish.
Do not invent new sections.
```

### Workflow E: visual review before further iteration

Use this when the session already has multiple candidate screens or when the next edit would otherwise be ambiguous.

1. use `list_screens` to find the likely targets
2. use `get_screen` to inspect candidate screens
3. when a screenshot or visual artifact is available, review it before the next major edit
4. ask the user to choose using a human description of the screen, not only an opaque ID
5. continue only after the canonical target is clear

### Workflow F: decide whether to stay in Stitch or move to code

Stay in Stitch when:

- the information architecture is still drifting
- the visual hierarchy is still weak
- multiple screen directions are still being explored
- the user is reacting to screenshots rather than implementation details

Move to code when:

- one canonical screen direction is accepted
- the required elements are stable
- the remaining work is implementation fidelity rather than design exploration
- the screen can be implemented coherently in the target stack

Quick decision table:

- stay in Stitch: unresolved hierarchy, unclear task flow, unstable screen family, unresolved design-system direction
- move to code: accepted screen family, clear transfer contract, target architecture known, drift handling plan defined

For greenfield work, prefer this move-to-code order:

1. generate mobile and desktop canonical screens separately when both matter
2. accept the visual direction
3. export or download the generated code artifact when available
4. translate that artifact into the real stack
5. only then start screen-by-screen product hardening

---
