# HTML report design

The bundled renderer is the source of truth. Do not ask the language model to recreate its HTML.

## Information architecture

Use an Apple-inspired, quiet operational surface with a 12-column Bento Grid:

- identity header with target, version, timestamp, and source counts;
- primary composite risk block;
- source coverage and network profile blocks;
- factual network block and material conflict block;
- authority-ordered risk rows on a shared 0-100 scale;
- a provider-by-dimension evidence matrix for location, network, score, proxy/VPN, Tor, and abuse;
- grouped provider tabs with returned fields and boolean signals.

Missing and unscored sources use text states and never receive zero-length bars presented as zero.
Keep all selected provider states accessible, including skipped, unavailable, and failed sources.

## Visual system

Follow system light/dark preference. Use neutral surfaces, blue/cyan accents, and green/yellow/red
only for semantic status. Do not use gradients, decorative blobs, bokeh, excessive shadows, or
one-hue palettes. Use at most 8px card radius, normal letter spacing, and platform system fonts.

Keep the page responsive without viewport-height layouts or page-level horizontal scrolling.
At narrow widths, stack Bento items, detail columns, and metric grids. Do not shrink essential
text below 11px or allow long provider values to overlap nearby content.

## Interaction and security

Tabs must support mouse, native focus, ArrowLeft/ArrowRight, Home, and End. Provide tablist,
tab, tabpanel, selected-state, and labelled-by semantics.

The report must be one offline HTML file with inline CSS and JavaScript and no CDN, fetch, XHR,
WebSocket, external font, or external asset. Embed report JSON as Base64 and render all upstream
strings through `textContent`; never inject provider text with `innerHTML`.
