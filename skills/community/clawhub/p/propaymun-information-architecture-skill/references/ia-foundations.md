# IA foundations and decision rules

Read this reference when defining, evaluating, or explaining the architecture rather than producing a narrowly specified artifact.

## Model

Use this expanded model for complex digital products:

`Objects + Relationships + Organization + Labels + Metadata + Navigation + Search + Permissions + Governance`

Evaluate it in the intersection of:

`Users × Content × Context`

### Boundaries

- **Information architecture** is the overall findability and meaning system.
- **Taxonomy** is a controlled classification and vocabulary.
- **Content model** defines content types, fields, relationships, rules, and lifecycle.
- **Product sitemap** visualizes a hierarchy of pages or destinations derived from architecture decisions; it is not the IA itself and uses the focused companion workflow in this skill.
- **Navigation** is the interface that exposes paths through the architecture.
- **Search** supports direct retrieval and discovery.
- **User flow** models actions, states, decisions, and alternate paths for completing a goal; it is not the IA itself and uses the focused companion workflow in this skill.
- **Content strategy** governs why, by whom, and through what lifecycle content is created and maintained.

Do not use these terms interchangeably.

## Organization systems

Possible schemes include topic, task, audience, object, lifecycle state, chronology, geography, alphabet, or a hybrid. Select a scheme based on priority tasks, audience language, object relationships, scale, volatility, and governance—not personal preference.

Task-oriented or hybrid structures can outperform subject-only structures for some knowledge-acquisition tasks, but this is contextual evidence rather than a universal law.

## Object-first IA

Before screens or menus, identify domain objects and their:

- attributes and metadata;
- relationships and cardinality;
- actions and allowed transitions;
- lifecycle states;
- ownership and permissions;
- creation, entry, retrieval, archiving, and deletion paths.

Use object-first modeling especially for SaaS, enterprise, marketplaces, AI products, and systems with dynamic content or multiple roles.

## Information scent and labels

A label is a prediction cue. A good label helps the intended audience distinguish this destination from competing choices and anticipate what happens after selection.

Evaluate labels for:

- audience vocabulary and localization;
- specificity without jargon;
- distinction from siblings;
- consistency across channels;
- examples for abstract categories;
- behavior at realistic breadth and depth.

Hierarchy depth cannot be judged independently of label quality. Reject fixed depth, click-count, or option-count rules.

## Navigation and search

Support both exploration and known-item retrieval. Search does not replace navigation. Consider:

- global, local, contextual, utility, and associative navigation;
- filters, facets, sorting, saved views, and recents;
- synonyms, query suggestions, no-result recovery, and reformulation;
- direct/deep entry and orientation away from the home page;
- backtracking and recovery after wrong choices.

## Permissions and personalization

Treat permissions as architecture because they change visibility and available actions. Keep permission logic distinct from personalization. In adaptive IA:

- preserve a canonical structure;
- keep critical destinations available;
- make adaptation legible and reversible;
- offer show-all or stable alternatives;
- avoid destabilizing shared collaboration contexts.

## Governance

Record owners, change authority, review cadence, naming rules, lifecycle, versioning, and deprecation. Monitor orphaned, duplicate, obsolete, ownerless, and inaccessible content.

## Principles as heuristics

Use the principles of objects, choices, disclosure, exemplars, front doors, multiple classification, focused navigation, and growth as review prompts. Do not turn them into rigid requirements.
