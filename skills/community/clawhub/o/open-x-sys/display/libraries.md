# Bundled page libraries

> **When to read**: a tier 0 page needs a library; you must decide whether to inline one or load it; or the person asks what the page depends on.

Tier 0 pages are single self-contained HTML files. OpenXSys bundles a small set of pinned visualization and motion libraries so that pages are consistent, checkable and able to work offline. The authoritative list, with versions, files and checksums, is `deps/openxsys.lock.json`. This page says what each library is for.

**Review status.** The versions and checksums below were recorded on 2026-11-16 from the jsDelivr package metadata. They are **candidates awaiting review**; a library counts as bundled only when its entry in the lock file is marked `approved`. Until then, treat each as a pinned candidate: use exactly the stated version, and never a floating "latest".

## Use a library only when the page needs it

Many of the best pages need none: type, layout, SVG and a little plain JavaScript are enough for most reveals. A library earns its place when it does something that would otherwise take hundreds of careful lines: a force layout, a projection, a timeline scrubber tied to scroll, real typeset mathematics. Loading five libraries to draw one bar chart makes the page slower and makes it look like every other page.

## The set

| Library | Version | Use it for | Form | Size (min) | License |
|---|---|---|---|---|---|
| **D3** | 7.9.2 | Data-driven SVG and canvas: scales, shapes, layouts, projections, transitions. The default for anything drawn from data | Classic script | 281 kB | ISC |
| **GSAP** (+ ScrollTrigger) | 3.15.1 | Sequenced motion and scroll-linked animation where CSS transitions are not enough | Classic script | 73 kB + 45 kB | GSAP standard license (free to use; not an OSI open-source license) |
| **Scrollama** | 3.2.0 | Scrollytelling: step enter and exit events | Classic script | 5 kB | MIT |
| **KaTeX** | 0.19.1 | Typeset mathematics | Classic script + CSS + fonts | 273 kB + 25 kB | MIT |
| **Mermaid** | 12.3.0 | Quick structural diagrams from text. Large; prefer hand-made SVG when the diagram is the centerpiece | Classic script | 5.5 MB | MIT |
| **Three.js** | 0.187.0 | 3D scenes, when the third dimension carries the insight | ES module | 659 kB + 1.5 MB core | MIT |
| **MapLibre GL JS** | 6.18.0 | Interactive maps. Needs a tile source, which is a network dependency and may have its own terms | ES module + worker + CSS | 1.1 MB + 520 kB | BSD-3-Clause |

ECharts is the alternative to D3 named in the design. D3 was chosen for the bundle because OpenXSys pages are native to their subject and D3 imposes no chart look. If the person already works with ECharts or another library, use theirs.

Licenses are stated as understood at recording time and are confirmed during review (see `deps/DEPENDENCIES.md`).

## Inline, or load

A page is one file. There are two honest ways to include a library.

**Inline (preferred for a deliverable that must work offline or be sent as a file).** If offline copies were installed (`display/lib/`, placed there by the installer after checksum verification), copy the library's source into a `<script>` element in the page. The page then needs nothing else. Classic-script libraries (D3, GSAP, Scrollama, KaTeX, Mermaid) inline cleanly. Inline KaTeX's CSS as well; its fonts are separate files, so either embed the few fonts used or accept the browser's fallback fonts offline and say so.

**Load from the pinned URL with an integrity check.** Use the exact version and the checksum from the lock file:

```html
<script src="https://cdn.jsdelivr.net/npm/d3@7.9.2/dist/d3.min.js"
        integrity="sha256-kSERCY6plQOm9JZzYdK73J2/WM+cZ4yOJ+WwLRoH8ME="
        crossorigin="anonymous"></script>
```

The browser refuses the file if it does not match. A page built this way needs a network connection for that library; say so when you deliver it.

**ES-module libraries** (Three.js, MapLibre) cannot be imported from a local file by a page opened by double-click, because browsers block module imports from `file://`. For these, load from the pinned URL, or inline the module source in a `<script type="module">` and import through a blob URL. If neither is acceptable for this deliverable, choose a form that does not need the library: most 3D insights can be shown with a well-made 2D projection, and many map insights with a static, sourced base map drawn as SVG.

## Rules for any library on a page

- **Exact pinned version**, from the lock file. Never `@latest`, never an unpinned URL.
- **Integrity attribute** on every remote script and stylesheet.
- **No other remote code.** No analytics, no trackers, no fonts or scripts from hosts that are not in the lock file, unless the person asks. Web fonts are an exception only when the design needs them; then name the host and provide a system-font fallback so the page still reads well offline.
- **A fallback that still tells the story.** If a library fails to load, the page should show the reveal in text and a static figure, not a blank area.
- **Tell the person what the page depends on** in one line when it depends on anything outside the file.

## A library that is not in the set

If the subject really needs something else, it is an install outside the bundled set: ask first, name the library, its version, its license and why it is needed (see `system/consent.md`). If the person already has it in their project, using theirs is not a new install.
