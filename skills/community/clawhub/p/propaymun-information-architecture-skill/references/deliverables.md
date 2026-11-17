# IA deliverables and semantic model

Read this reference after the IA direction is stable enough to communicate or when the user requests a reusable artifact.

## Layered delivery

Do not use every section by default. Select the smallest useful combination.

### Decision layer

- purpose, scope, audience, and evidence status;
- recommendation and why it fits;
- consequential unknowns and decisions;
- next action.

### Working architecture layer

- users, content, and context;
- important objects/content and relationships;
- organization and taxonomy;
- labels and controlled vocabulary;
- navigation, search, entry, orientation, and recovery;
- roles, permissions, ownership, lifecycle, and governance;
- meaningful alternatives and trade-offs.

### Assurance layer

- evidence ledger and limitations;
- validation plan and decision rules;
- decision log and review triggers;
- machine-readable semantic model when it will be reused.

For a focused request, include only its essential prerequisites. Do not pad it into a complete report.

## Canonical structure before presentation

Every deliverable must represent one canonical semantic IA model. Do not independently invent a text hierarchy, diagram, HTML artifact, and role table that disagree with one another.

The canonical model should capture, where relevant:

- users, roles, contexts, and priority information needs;
- information domains, concepts, objects, and content types;
- parent-child hierarchy and ordering;
- typed cross-relationships that hierarchy cannot express;
- organization schemes, taxonomy, labels, metadata, and classification rules;
- navigation, search, entry, orientation, and recovery;
- visibility, permissions, ownership, lifecycle, and governance;
- evidence, consequential assumptions, unknowns, decisions, and validation.

Renderers select views of this model. They do not become the model.

## IA Reference Lock

Before translating the IA into a downstream artifact, record the smallest stable contract needed to prevent semantic drift:

```yaml
ia_reference_lock:
  source: canonical semantic IA
  model_version: "2.0"
  readiness: provisional | reviewable | approved
  approved_structure: [domains, items, hierarchy, typed relationships]
  approved_language: [labels, preferred terms, synonyms]
  findability_constraints: [navigation, search, entry, orientation, recovery]
  access_privacy_constraints: [visibility, permissions, consent, retention]
  unresolved: [assumptions, unknowns, conflicts]
  invariants: [meaning that must survive translation]
  adaptation_boundaries: [decisions delegated to the downstream capability]
```

Use a compact human-readable form in chat and a structured form in reusable handoffs. This lock is a translation contract, not a claim that every field is approved. Readiness controls how assertively the derivative may be presented:

- **not-ready:** continue IA work; no consequential derivative;
- **provisional:** create an explicitly exploratory derivative with visible assumptions;
- **reviewable:** create a decision-ready derivative and identify remaining review points;
- **approved:** preserve approved constraints and treat changes as proposals.

Review differences as one of: allowed adaptation, new proposal, semantic drift, or implementation defect.

For a standalone product sitemap or user flow with no accepted IA, use the same discipline through a **minimum semantic substrate** rather than pretending a complete IA exists:

```yaml
semantic_substrate:
  id: substrate-001
  version: "1.0"
  artifact: product-sitemap | user-flow
  purpose: "decision this artifact must support"
  relevant_audiences_or_actors: []
  canonical_items_or_content: []
  labels_and_states: []
  access_and_business_rules: []
  evidence_status: Proposed
  unresolved: []
  invariants: []
```

The substrate is deliberately smaller than full IA, but it is versioned and traceable so later IA work can reconcile it.

## Suite handoff manifest

For transfer to a dedicated Sitemap, User Flow, design, engineering, or future ProPaymun Product Suite component, include only stable shared context:

```yaml
suite_handoff:
  contract_version: "1"
  source_skill: propaymun-information-architecture
  source_model_version: "2.0"
  intended_consumer: sitemap | user-flow | product-design | engineering | other
  requested_outcome: "..."
  ia_reference_lock: "embedded or linked"
  open_decisions: []
  evidence_limits: []
  requested_return: [proposals, drift-report, artifact]
```

For a product sitemap or user-flow consumer, include the owning artifact type, its decision purpose, source lock or substrate ID, readiness, stable IDs, unresolved decisions, and permitted downstream adaptations. Do not require UI, prototype, code, or multiple diagrams unless the user asks for them.

Do not transfer full conversation history when the lock and evidence limits are sufficient. The receiving component may propose adaptations but must return structural changes for IA review.

## Audience adaptation

- **Product or leadership:** lead with decisions, risks, scope, and consequences.
- **Cross-functional team:** add object relationships, vocabulary, ownership, and retrieval behavior.
- **Design or research:** emphasize audience language, organization hypotheses, findability, and validation.
- **Engineering or data:** add stable identifiers, relationships, cardinality, states, permissions, and lifecycle rules.
- **Content or operations:** emphasize ownership, vocabulary, metadata, publishing or service lifecycle, retrieval, and governance.

When no audience is specified and it does not affect the decision, use a cross-functional professional baseline.

Translate the same canonical model for each audience. Do not create separate architecture truths for leadership, design, engineering, or operations.

## Format selection

In a conversation-capable environment, use chat text by default. Produce a file or heavy artifact only when the current conversation requests it or the user accepts a concrete format after the semantic source is ready enough. Persistent memory or a preference from another chat is not deliverable authorization, and no current request means no Memory, Project Knowledge, Gem Knowledge, or workspace-context mutation. Prompt-to-app builders are downstream renderers: prepare their handoff only after the canonical IA or minimum semantic substrate is stable enough for the intended decision.

Offer only formats supported by the current environment and distinguish:

- editable source;
- rendered output;
- copy-ready content when file creation is unavailable.

Do not generate every format. Produce the one the user selects.

## Interactive connected IA blueprint

When the user requests an interactive visual artifact, it should help a mixed team understand and challenge the IA without requiring IA expertise.

### Primary view

Start with a connected hierarchy of information domains, concepts, objects, and content types. Make containment, classification, and important cross-domain relationships legible. The viewer should understand the product's information universe and major connections before opening any specialist detail.

This is not a sitemap: its nodes are semantic information structures rather than pages or destinations. It is not a user flow: edges express structural or semantic relationships rather than a sequence of actions.

### Progressive detail

Reveal relevant detail through selection, expansion, filtering, or focused subviews:

- purpose, attributes, states, and lifecycle;
- taxonomy, labels, metadata, and classification rules;
- navigation, search, entry, orientation, and recovery;
- role visibility, permissions, ownership, and governance;
- decisions, consequential assumptions, unknowns, evidence, risks, and validation.

Do not make a collection of tabs, tables, or cards the primary IA. Use them only to explain the structure. Avoid rendering internal evidence labels as unexplained badges on every node.

The blueprint is a review view of the architecture, distinct from a product interface, sitemap, user flow, API, or database schema. If the user requests one of those derivatives, create it from the IA Reference Lock through the relevant capability rather than turning the blueprint itself into that deliverable.

## Semantic IA JSON

Use this portable shape only when structured reuse, validation, rendering, or handoff justifies it:

```json
{
  "meta": {
    "title": "Example IA",
    "model_version": "2.0",
    "status": "proposed",
    "language": "en",
    "direction": "ltr",
    "scope": "Product area",
    "problem_shape": "hybrid",
    "locale_context": {
      "country": null,
      "operating_model": null,
      "evidence_status": "Unknown"
    },
    "handoff": {
      "purpose": "review",
      "readiness": "provisional"
    }
  },
  "contexts": [],
  "audiences": [],
  "tasks": [],
  "information_needs": [],
  "domains": [],
  "items": [],
  "relationships": [],
  "roles": [],
  "organization_schemes": [],
  "taxonomy": {},
  "labels": [],
  "metadata_model": [],
  "navigation_systems": [],
  "search": {},
  "permissions": [],
  "lifecycles": [],
  "governance": {},
  "evidence_ledger": [],
  "assumptions": [],
  "unknowns": [],
  "conflicts": [],
  "decisions": [],
  "validation": []
}
```

Keep IDs stable across revisions. Relationships must reference existing IDs. Use the response language for human labels. Technical IDs may be English when interoperability benefits. Use `direction: rtl` for an RTL rendered artifact unless the selected renderer is clearer with English technical labels and a different flow direction.

Use `parent_id` only for real hierarchy, containment, or classification. Represent associative, dependency, reference, ownership, lifecycle, and visibility relationships explicitly in `relationships` with a type, direction, and human-readable meaning.

## Architecture alternative card

```markdown
### Option name
- Organizing principle:
- Best-supported needs:
- Trade-offs and failure risks:
- Retrieval dependency:
- Governance cost:
- Supporting evidence:
- Validation needed:
```

## Decision log entry

```markdown
- Decision:
- Status: Confirmed | Proposed
- Rationale and evidence:
- Alternatives considered:
- Consequences:
- Owner:
- Review trigger:
```
