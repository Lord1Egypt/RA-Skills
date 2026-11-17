# Optional IA diagramming

Read this reference only when the user requests or accepts an IA, product-sitemap, or user-flow diagram. Read the owning semantic reference first.

## Start from semantics

Define nodes, relationship types, direction, groups, states, evidence status, and view scope before choosing coordinates or colors.

`Truth model → IA question → Visual encoding → Deliverable`

The visual must be generated from the same canonical model used by text and structured outputs. Do not redesign the architecture while laying out the diagram.

## ProPaymun structural grammar

The recognizable quality of the output comes from consistent meaning, not a fixed color palette or card style.

- **Primary hierarchy:** information domains contain or classify concepts, objects, or content types.
- **Typed connections:** labeled edges show meaningful cross-domain relationships that a tree cannot express.
- **Consistent abstraction:** do not mix domains, pages, UI controls, database fields, and task steps in one level.
- **Overview before detail:** show the whole information universe at a legible level, then create focused domain views when necessary.
- **Details on demand:** attributes, states, rules, permissions, evidence, and decisions belong in contextual detail or focused views unless they are essential to interpreting the map.
- **Findability cues:** communicate relevant browse, search, entry, orientation, and recovery systems without drawing a page-level sitemap.

A connected hierarchical IA map is not automatically a sitemap. It becomes a sitemap when its nodes and containment primarily represent pages or destinations. It becomes a user flow when its edges primarily represent goal-directed actions, system responses, states, decisions, failures, or recovery. Visual similarity does not make these artifact types interchangeable.

## One decision question per view

Useful IA views include:

- domain or object relationships;
- taxonomy and classification;
- navigation systems and cross-links;
- search, metadata, and facets;
- roles, visibility, and permissions;
- current-versus-proposed architecture.

Do not include neighboring mapping deliverables unless the user requests a coordinated set. Keep each view focused on one decision and share stable source IDs across related views.

For complex IA, coordinate several views from the same model:

1. overview structure map;
2. focused domain or relationship maps;
3. taxonomy and label view;
4. retrieval and findability view;
5. access, lifecycle, or governance view when material.

Do not force all layers into one graph.

## Capability-aware routing

Use the format requested by the user when the environment supports it. Otherwise explain the available alternatives.

- A textual tree, relationship list, or matrix is the portable baseline.
- Mermaid is useful as editable syntax when it renders reliably; it is not the default response.
- Standalone HTML or SVG can provide a polished shareable view when creation and rendering tools are available.
- Draw.io is an optional companion for precise editable geometry and formal handoff.
- Excalidraw is an optional companion for workshops and conceptual explanation.

Do not assume a companion is installed. Do not install one without explicit authorization. Preserve a textual equivalent even when a visual is created.

## Language and RTL

Keep the surrounding explanation in the user's language. For Persian or another RTL language:

- use a readable RTL textual structure as the safe baseline;
- keep human-facing labels in the user's language when the renderer handles them well;
- allow English technical labels or IDs when RTL rendering would reduce clarity or reliability;
- explain the language choice once rather than apologizing throughout the artifact.

## Visual encoding

- Give the view a title, IA question, scope, status, and legend when needed.
- Keep abstraction levels consistent.
- Label relationship direction and meaning; avoid vague edges.
- Use containment only for real ownership, scope, or grouping.
- Never rely on color alone.
- Keep labels concise and specific.
- Use whitespace and scale to establish hierarchy.
- Encode evidence status only when it changes interpretation. Explain it in plain language and redundantly when it matters, such as border style plus a text label. Do not turn internal evidence metadata into unexplained badge noise.

For a sitemap, distinguish hierarchy, cross-link, contextual entry, external boundary, and access-limited destination. For a user flow, distinguish action, system response, decision, state, failure, recovery, success, and actor handoff when present. Do not rely on color alone for these meanings.

## Render and inspect

Before rendering, reconcile the view with the model and accompanying text: domain counts and names agree; each edge has the intended endpoints, direction, and meaning; required versus optional links remain distinguishable where material; facets connect to all relevant item types. A diagram request authorizes a representation, not new architecture. Label an overview as partial when it omits detail and identify the omitted scope. Avoid quantitative claims such as “four domains” unless checked against the displayed view.

When rendering tools are available:

1. generate editable source;
2. render the requested output;
3. inspect the actual result;
4. fix clipping, overlap, crossings, ambiguity, imbalance, and unreadable text;
5. preserve the source beside the final export.

For a decision node, inspect every outgoing branch at the rendered size: each connector must visibly leave the decision, carry an unambiguous condition label, and reach the intended node without label or edge collisions. If the renderer cannot make that reliable, simplify the layout or deliver the exact textual flow instead of presenting a misleading visual.

If rendering is unavailable, say that the source was reviewed or syntax-checked but not visually verified. Never claim visual QA without inspecting the render.

## Accessibility

Provide a concise textual equivalent covering the important nodes, relationships, exceptions, and evidence state. Use accessible titles and descriptions where supported. Readability at the target size matters more than zoomability.
