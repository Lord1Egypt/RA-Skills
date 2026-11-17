# Modeling and option generation

Read this reference when creating object models, taxonomies, labeling systems, navigation/search structures, or architecture alternatives.

## Semantic model sequence

Model in this order when relevant:

1. users, roles, contexts, and priority tasks;
2. domain objects and content types;
3. attributes, metadata, and relationships;
4. actions, states, lifecycle, and permissions;
5. organization schemes and taxonomy;
6. labels and vocabulary;
7. navigation, search, entry, and recovery;
8. governance and validation.

This is a reasoning order, not a mandatory conversation order.

## Model the information universe

First recognize the dominant IA problem:

- **content/taxonomy:** content types, topics, audience vocabulary, metadata, classification, browse, and search carry most of the architecture;
- **object/operation:** persistent objects, records, relationships, states, ownership, permissions, and lifecycle carry most of the architecture;
- **hybrid:** both are consequential and must meet in one model.

This is an internal modeling choice, not a mode the user must select. Do not force roles, permissions, lifecycle, or object-style detail into a content-led problem unless it improves a real decision.

Before choosing a visual or document structure, distinguish:

- **information domain:** a stable subject or responsibility area;
- **concept or object:** a recognizable thing people reason about or act on;
- **content type or record:** a governed information structure with attributes and lifecycle;
- **classification:** a way of grouping or faceting items;
- **destination or page:** a later interface exposure that belongs in a sitemap, not the canonical IA hierarchy;
- **task step:** an action or state transition that belongs in a user flow.

Use one canonical item registry. Every item must reference exactly one information domain; do not maintain separate `objects` and `nodes` lists that can drift. Build a parent-child hierarchy only where containment, scope, or classification is real. Add typed relationships for association, dependency, reference, membership, ownership, lifecycle, visibility, or derivation. Name the relationship in product language so a non-specialist can understand its consequence.

Exactly one `domain_id` means one canonical home in the model. It does not prevent facets, tags, related-content links, contextual exposure, search results, or alternate findability paths.

Model a relationship record such as membership, assignment, payment, or application as its own item when it has attributes, lifecycle, permissions, history, or findability. Do not collapse distinct objects only to make a diagram smaller.

Keep a person or account distinct from the roles they can assume and from role-scoped profiles, organizations, stores, or workspaces they can own or administer. A low-friction experience may expose these through one account without making them one semantic object. Merge them only when their identity, ownership, lifecycle, visibility, and permissions are genuinely equivalent.

For open contribution, marketplace, community, or multi-party systems, identify the minimum trust and safety structure that changes visibility or lifecycle: reporting, moderation or review ownership, restricted or suspended states, prohibited content or goods, disputes or appeals, and recovery. This does not commit every control to the first release; it prevents the architecture from treating consequential operating states as nonexistent.

For an existing product, derive the candidate model from the content inventory, current structure, search/navigation evidence, policies, and observed failures. For a new product, derive it from audiences, priority tasks, planned capabilities, domain rules, and information that must be created, found, understood, governed, or retained.

## Canonical item card

For each important object capture:

```yaml
id: item-project
domain_id: domain-work
name: Project
kind: object
purpose: Unit of coordinated work
parent_id: null
attributes: [name, owner, status, due_date]
relationships:
  - target: Workspace
    type: belongs_to
actions: [create, view, edit, archive]
states: [draft, active, completed, archived]
roles: [owner, editor, viewer]
entry_points: [global_search, workspace_projects, recent_items]
lifecycle_owner: Product Operations
evidence_status: Proposed
```

## Relationship and lifecycle integrity

Test each proposed relationship with one normal example and one valid exception. Specify whether it is optional or required and whether multiple targets are meaningful; do not infer “every item must link” from a useful related-content pattern. For example, a subject-specific review may reference an entity while industry news may reference none or several. Introduce a maintained reference catalog only when a retrieval need justifies its ownership and update cost.

- Use `parent_id` only for a real primary hierarchy.
- Use typed relationships for additional meaning, including `belongs_to`, `references`, `membership`, `assignment`, `settles`, `owned_by`, and `visible_to`.
- Give each relationship explicit endpoints, direction, label, meaning, and evidence state.
- When an item can belong to alternative scopes, model the options explicitly instead of forcing one parent.
- Structure lifecycle states and transitions. For each transition record the source, destination, permitted role, condition, and evidence state when relevant.
- Keep roles distinct until their permissions and authority are confirmed equivalent.

## Taxonomy design

Keep independent dimensions separate. Format (video/audio/text), editorial purpose (news/review/analysis), topic, audience, and subject attributes may coexist as facets; do not flatten them into mutually exclusive siblings. Define which item types each facet applies to. Use canonical subject references alongside topic classification where needed without forcing all content to reference a catalog item.

Define:

- purpose and audiences;
- meta-characteristic or governing classification intent;
- dimensions and category membership rules;
- polyhierarchy or faceting policy;
- synonym, preferred term, and localization policy;
- inclusion/exclusion examples;
- objective and subjective stopping conditions;
- owner and extension/deprecation rules.

Useful subjective qualities: concise, robust, comprehensive within scope, extendible, and explanatory. Do not force mutual exclusivity when the product genuinely needs facets, tags, or multiple classification.

## Generate meaningful alternatives

Alternatives must differ structurally, not just in labels or colors. Typical lenses:

- task-first;
- object/resource-first;
- audience/role-first;
- lifecycle/state-first;
- topic/domain-first;
- hybrid with stable primary structure plus facets or contextual paths.

For each option state:

- organizing principle;
- tasks it supports well;
- likely failure modes;
- dependence on search or personalization;
- scalability and governance cost;
- evidence supporting it;
- validation needed.

Recommend one only after comparing it with priority tasks and constraints.

## Navigation model

Specify each navigation system's purpose, audience, content scope, ordering rule, visibility rule, and relationship to search. Avoid one overloaded global menu for unrelated tasks.

## Search model

Specify searchable objects/content, metadata and facets, synonyms, ranking signals, permission filtering, result types, empty-state behavior, and recovery. Never expose restricted content through labels, counts, snippets, or suggestions.

## Priority information-need trace

For each priority need, verify this chain without turning it into a screen-by-screen flow:

`audience/context → information sought → entry point → organizing cue or label → canonical item/content → access rule → recovery`

Use the trace to catch orphaned content, misleading labels, missing entry points, inaccessible search results, and dead ends. Keep only traces that test consequential parts of the architecture.

## AI product considerations

For products containing agents or generated content, also model:

- user, system, tool, source, conversation, run, artifact, memory, and permission objects;
- provenance and citation at the claim or artifact level;
- draft/review/approved states;
- human confirmation for consequential actions;
- visibility and retention boundaries;
- stable canonical locations despite adaptive recommendations;
- recovery, undo, retry, and escalation.

## Revising an existing architecture

Treat a correction or new requirement as a change to the canonical model, not as a fresh parallel document.

1. classify the input as a new fact, decision, scope change, label change, evidence update, or implementation constraint;
2. identify the directly affected IDs and then inspect dependent hierarchy, relationships, information-need traces, navigation, search, access, lifecycle, governance, validation, and renderer views;
3. preserve stable IDs unless the underlying meaning changed; record merges, splits, renames, and deprecations explicitly;
4. update the canonical model once and regenerate derived views instead of hand-editing each output;
5. show the user a compact delta, its product consequences, any newly blocking unknown, and the next validation need;
6. rerun structural validation and handoff-readiness checks before export.

Do not repeat the full architecture when only a small part changed unless the user requests a consolidated artifact.
