---
name: kiwi-design-system
description: Apply and improve PIP, the WhiteKiwi design system. Use when a task explicitly chooses PIP, works on WhiteKiwi/kiwi-design-system, or changes a product using @whitekiwi/ui or @whitekiwi/tokens. Covers integration, design contracts, shared improvement proposals, upstream contributions, and consumer verification; not a general-purpose brand creation skill.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - node
---

# Kiwi Design System

Use PIP's existing visual language and components in the requested product. When
product work reveals a useful shared improvement, carry it through the existing
user authorization: prepare the shared change in PIP, verify it in the consumer,
and complete the authorized release and adoption. For genuinely new scope,
explain the smallest change and the unresolved decision.
Do not require another consumer or a minimum usage count.

## Read the right source

The [design-system repository](https://github.com/WhiteKiwi/kiwi-design-system)
owns the implementation and design contracts. This skill owns the agent workflow.

- [Public catalog](https://design.whitekiwi.link/): visual specimens, system layers, and design standards.
- [Design contract](https://github.com/WhiteKiwi/kiwi-design-system/blob/main/DESIGN.md) and [guidelines](https://github.com/WhiteKiwi/kiwi-design-system/blob/main/docs/guidelines.md): visual roles, interaction states, and rationale.
- [UI package](https://github.com/WhiteKiwi/kiwi-design-system/tree/main/packages/ui) and [tokens package](https://github.com/WhiteKiwi/kiwi-design-system/tree/main/packages/tokens): exports, dependencies, themes, and API limits.

Inspect the consumer's dependencies, lockfile, source, and repository instructions.
Check installed package versions against the inspected source revision: `main`
and the website may contain changes not yet published. Use a local checkout or
available source-reading tools; an unavailable source is a limitation, not proof
that a component or capability is absent.

## Choose the work

- **Integrate or change a PIP product:** read [references/integration.md](references/integration.md). Prefer existing APIs and composition before adding parallel local UI.
- **A useful shared gap emerges:** inspect the local UI added or overridden in this task, compare the public API, and select the smallest reusable behavior. Continue through the contribution reference when shared improvements are already authorized.
- **Implement an agreed improvement:** read [references/contribution.md](references/contribution.md). Make the shared change in the design-system repository first, including documentation and verification, then verify its use in the consumer.
- **Explain or review the system:** read the relevant source and report what exists, its contracts, and demonstrated gaps. Do not turn a review into implementation or apply PIP to an unrelated brand.

Reuse an explicit request or standing instruction to return shared improvements
to PIP. Do not turn every missing component into a new approval cycle. Resolve
only a new product direction, incompatible API, or external action outside that
authorization. Prepare the concrete reversible work before that decision.
If the user chooses an app-only solution, respect that scope. If upstream access
is unavailable, preserve the reproduction and proposed change for handoff.

Keep product data, business logic, and product-only composition in the app.
Share only the agreed reusable parts. Start with the current need rather than
speculative options. Track temporary workarounds with their reason, related
issue/PR, and removal condition.

## Keep public material reader-focused

The public site explains what PIP contains, its design criteria, and how its
layers fit together. The repository README explains what the project is and
where its parts live. Keep agent approval, execution, and rollout procedures in
this skill and its references. Keep visual rules and API details in their source
repository instead of copying a second catalog into the skill.

## Close the consumer loop

Review new local controls, copied styles, internal-selector overrides, and missing
states before declaring the product work done. Record the applicable outcome in
the existing PR or design contract, not a new report for every task:

- Existing PIP API covers the need: reuse it.
- Shared improvement: link the PIP change and verify the consumer adoption.
- Product-only behavior: keep it local and explain the ownership boundary.
- Unresolved gap: link the existing issue or authorized draft PR, with the next
  action and workaround removal condition. If external tracking is not authorized,
  give a concrete handoff with the remaining decision; do not label it completed.

A proposal buried in the product document is not an implemented contribution.
Inspect other known consumers when useful, but one demonstrated use case is enough.
Non-React products can share native HTML patterns and component CSS without
loading the React entry. Read the repository's native-pattern contract; keep
behavior and accessibility obligations with the markup. Do not force a framework
migration merely to consume PIP.

## Verify and finish

Use the design repository's current checks and inspect changed screens in the
relevant themes, states, and viewport sizes. Static checks do not prove keyboard
behavior or a consumer application's complete accessibility. Node.js and the
repository's pinned package manager are needed for builds; do not claim runtime
verification when those tools or the app are unavailable.

Report the source revision, checks actually run, related PRs, and what remains.
Distinguish design-system merge, npm publication, and consumer adoption. A
contribution request does not itself authorize publishing packages or deploying
the app. Follow already authorized release scope without asking again.
