# Product and UX sitemap

Read this reference when the user requests a product/UX sitemap, destination hierarchy, screen map for structural planning, or a review of how pages and destinations relate. Do not use it for an XML/SEO sitemap unless the user is asking only for the product structure that should inform a separate SEO implementation.

## Purpose and boundary

A product sitemap communicates destination scope, hierarchy, labels, access, and important navigation relationships. It is a view of product structure, not the complete IA and not evidence that users can find or understand the destinations.

When “sitemap” is ambiguous, use context:

- product, UX, app, pages, navigation, hierarchy, or design usually means a product sitemap;
- XML, URL, crawl, index, robots.txt, Search Console, or search-engine coverage means an SEO sitemap;
- ask one short clarification only when the distinction changes the requested work and context does not resolve it.

## Source contract

If an accepted IA exists, derive the sitemap through its IA Reference Lock. Otherwise create a versioned minimum semantic substrate containing only the audience, canonical content/objects, labels, access constraints, and structural assumptions needed for this sitemap. Do not require a full IA engagement.

Record:

- source type and version: IA Reference Lock or minimum semantic substrate;
- sitemap purpose, audience, platform/channel, and scope;
- readiness and evidence status;
- unresolved decisions that could change destinations or hierarchy;
- invariants and allowed adaptation boundaries.

## Destination model

Use stable IDs. For each relevant destination, define only what the decision needs:

- label and purpose;
- parent and any legitimate alternate access or cross-link;
- canonical IA item/content references;
- audience and access scope;
- entry contexts and orientation/recovery behavior;
- route or URL proposal only when implementation needs it;
- evidence status and consequential assumptions.

A destination is a place the user can meaningfully arrive at, orient within, and leave. Keep these neighboring concepts separate even when they appear together in a UI:

- **information domain:** a semantic area in the IA, not automatically a page;
- **destination:** a reachable place such as a hub, collection, detail, workspace, utility, or external boundary;
- **view or filter:** a presentation of a destination such as “Today,” “Saved,” or a filtered list—not a child page unless it has independent purpose, addressability, and orientation;
- **state:** a condition of an object or destination such as empty, pending, unavailable, or completed;
- **capability:** something a person can do, such as search, compare, book, or edit;
- **action/control:** the trigger for a capability, not a destination.

Do not promote a view, state, feature, or button into the destination hierarchy merely because it is visible. If classification is uncertain, state what the node represents before placing it.

Distinguish:

- hierarchy: primary structural parent;
- cross-link: navigational association without reparenting;
- contextual entry: search, notification, deep link, campaign, saved item, or another entry point;
- utility/system destination: support, authentication, settings, error, access denied, or recovery;
- external destination: a boundary, not an internal child.

An authentication or access gate is not the structural parent of the product merely because some users pass through it first. Show it as an entry or utility boundary. A role-scoped workspace can still be a destination even when it is nested under an account or another hub; “not top-level” does not mean “not a destination.”

Separate destinations whose purpose and lifecycle differ. For example, a cart is transient pre-purchase work while order history and order detail are post-purchase records; settings do not belong under saved items merely because both are personal. When a transaction crosses an external payment boundary, show relevant return destinations or states—success, failure, cancellation, pending/unknown, and recovery—proportional to the product risk.

Do not force every object into its own page. Do not copy an organizational chart unless it matches users' information needs. Do not mix content types, product objects, UI controls, and pages at one abstraction level without making the distinction explicit.

## Review

Check structural integrity:

- every destination has a unique stable ID and meaningful purpose;
- every node classified as a destination is genuinely reachable and is not merely a view, state, capability, or control;
- parents and cross-links reference existing destinations;
- the hierarchy has an intentional root or declared multiple entry structures;
- no unintended cycles, orphans, duplicates, or unreachable destinations remain;
- private, role-scoped, or state-dependent destinations are not exposed to the wrong audience;
- labels remain consistent with the canonical vocabulary;
- alternative entry and recovery paths exist where the product requires them;
- role-scoped creation, management, support, trust/safety, and post-transaction destinations are represented when they are in scope, rather than disappearing behind a public profile;
- changes from the source are classified as allowed adaptation, proposal, semantic drift, or implementation defect.

Report structural correctness separately from findability. Use tree testing, first-click testing, search analysis, task evidence, or another claim-matched method before saying users can find something. Fixed click counts, hierarchy depth, or category counts are heuristics or project constraints, not universal rules.

## Output

Use the smallest representation that answers the request: indented tree, destination table, Mermaid, editable diagram, or structured JSON. A request for a detailed sitemap requires a destination-complete view for the agreed scope, not a domain list, capability inventory, conceptual relationship map, or one task flow. A companion flow may clarify navigation but must not replace the requested sitemap. In ordinary conversation, lead with the destination structure and explain only distinctions that affect the decision; keep schema field names and evidence codes for a requested structured handoff. A diagram must preserve a textual equivalent and the same destination IDs. Create a durable file only when the current conversation requests or accepts it.
