# Discovery and low-effort interaction

Read this reference when starting complete IA work, selecting questions, deciding whether to stop, or planning an IA audit.

## Principle

The agent carries the IA method. The user supplies product knowledge in ordinary language. Never transfer professional quality-control work to a user who may not know IA.

Do not ask the user to choose Guided/Quick modes, approve jargon-heavy models, select a checkpoint, or restate “stop and wait.”

## Adaptive sufficiency loop

Run the sufficiency gate before every consequential architecture step, not only at intake. New objects, relationships, permissions, lifecycle rules, locale signals, evidence, and export requests can reveal a new blocking question.

Before each consequential step, classify open issues:

- **Blocking:** proceeding could select a materially different architecture, expose sensitive information, or create an expensive mistake. Ask and stop.
- **Important but assumable:** one default is defensible and reversible. State the assumption and continue.
- **Detail:** it will not affect the current IA decision. Defer it.

Do not use a numerical completeness score. Judge sufficiency against the decision being made.

An unknown blocks only the decision that depends on it. Continue useful independent analysis, but do not finalize, export, or imply certainty for the affected part.

## Host memory and prior preferences

Do not proactively retrieve or search persistent memory or prior-chat project records unless the user explicitly asks in the current conversation. Host-supplied memory may adapt only low-risk response length or technical depth when consistent with the current turn. It never determines response language, current project identity, product context, artifact choice, scope, evidence, or authorization.

- Do not create files or artifacts because another chat established an “always give me a file” preference.
- Without an explicit current request, do not create, update, persist, or claim to update Memory, Project Knowledge, Gem Knowledge, workspace context, or another durable project record.
- A statement such as “continue later,” “keep this,” or “we will return to it” does not by itself authorize persistence. If “save this” could mean a file, project note, or host memory and the destination changes the action, ask one short clarification.
- Do not reuse remembered roles, rules, research, approvals, or architecture decisions as confirmed facts. Verify the project identity and reconcile the prior context with the current brief first.
- When memory conflicts with the current request, follow the current request.
- Treat stale or same-name project memory as prior context until the user confirms it still applies. Do not merge different projects merely because their domain, title, or actors resemble one another.
- When a remembered preference would materially change effort, format, scope, or an external action, ask at the point of decision or use the non-mutating conversational default.
- For cross-session continuity, prefer a compact portable continuation note. If the user explicitly requests persistent storage, show or state the minimal intended payload, exclude secrets, sensitive personal data, raw transcripts, and unsupported assumptions presented as facts, then use only a capability evidenced in the current host.
- If durable memory is unavailable or success is uncertain, provide the continuation note and say it was not stored. Never invent a successful update. If the host changes memory automatically outside the agent's control, do not treat that event as reliable authorization or evidence.

## First turn

### No usable brief

Separate an empty invocation from an early but real product brief.

If the message only invokes the skill, repeats its starter, or describes the skill's purpose without actual product, audience, problem, evidence, or artifact context, ask in one short sentence for the product/problem or brief and stop. Do not provide a checklist, offer an artifact menu, explain memory or activation, or infer a project from prior context.

If the user has supplied any meaningful product idea or problem—even if incomplete—first determine whether they want orientation, help shaping the idea, a quick first structure, full IA work, an audit, or a derivative from existing IA. Infer this from their wording whenever possible; never make them choose an internal mode.

For an idea-stage or novice request, provide a small useful frame before asking anything: reflect the product idea, explain the first architecture consequence in ordinary language, and propose a reversible starting point. Then ask the single question with the highest expected effect on the next model decision. Typical starting information includes:

- What product or service is being designed?
- Who mainly uses it and what are they trying to accomplish?
- Is it new, a redesign, or an audit of an existing product?
- What brief, research, inventory, analytics, screenshots, policies, or current structure are available?

Do not demand all four answers at once. Ask a compact group only when the answers are tightly coupled. A visible provisional sketch is allowed when it helps the user recognize the problem and cannot reasonably be mistaken for a completed architecture; do not create a durable artifact yet.

### Partial or substantial brief

First inspect all provided material. Reflect the product and scope in a few lines. Ask only the smallest question or compact interdependent group that distinguishes plausible architectures. Do not use a numeric question quota.

As soon as the available context supports a responsible baseline, prefer one coherent useful pass over asking about each modeling layer in a separate turn. Cover the model slice needed for the user's current outcome with reversible defaults, then ask again only when a newly reached high-impact decision lacks a responsible default. This is an outcome-based sufficiency judgment, not a fixed question or decision count.

### Sufficient brief

Proceed, but reassess sufficiency when the model reaches another consequential decision. Do not ask a ritual confirmation merely because a workflow template contains a checkpoint.

## High-impact question lenses

Use only the lenses relevant to the product:

- outcome, audience, priority tasks, scope, and costly failures;
- core objects/content, relationships, states, and lifecycle;
- independent versus organization-scoped identities and ownership;
- visibility, permissions, consent, retention, and legal constraints;
- global versus contextual findability;
- audience vocabulary, organization logic, browse versus search needs;
- language, geography, jurisdiction, cultural convention, and local operating model when they change structure or terminology;
- scale, volatility, governance, and change authority;
- evidence that can confirm or challenge the proposed structure.

For sensitive or regulated domains, prioritize access, consent, retention, ownership, jurisdiction, and auditability before selecting architecture.

## Ask in product language

Questions must describe consequences the user can recognize.

Avoid:

> Is the role-context permission model correct?

Prefer:

> Can a doctor belong to more than one clinic, and should their access change depending on which clinic they are working in?

Avoid:

> Does the navigation model match your mental model?

Prefer:

> Should patients search across every clinic, or begin inside one clinic and see only its doctors?

Do not include hints that teach the user how to police the skill. The skill must perform its own scope, evidence, and completeness checks.

## Handling weak answers

“Everyone” or “all content types” is an incomplete prioritization, not evidence of equal needs or approval for every feature. Ask about the first useful audience outcome or first release when it affects structure. Distinguish accepting a recommendation from authorizing unrelated capabilities. Preserve the decision history so later diagrams and exports do not promote assumptions into confirmed scope.

If the user replies “yes,” “continue,” “I don't know,” or gives no new product detail:

1. do not repeat the same approval request;
2. offer a small set of plausible patterns when the user needs help recognizing the choice;
3. infer or recommend a defensible default from the brief and domain evidence;
4. state the default and its user-visible consequence briefly;
5. keep its Proposed or Inferred status in internal state, and describe it naturally to the user;
6. continue unless the consequence is unsafe, legally sensitive, or difficult to reverse.

Continue through a coherent slice before asking another question. Do not turn one resolved uncertainty into an immediate sequence of increasingly specialist questions.

When two choices are both consequential and no defensible default exists, explain the difference in plain language and ask one decision question.

Do not turn ordinary product mentoring into an implicit growth exercise. Registration, login, synchronization, payment, monetization, promotion, engagement loops, and conversion or retention metrics are separate decisions. Introduce them only when the brief, evidence, or the affected architecture requires them. A user accepting a convenient starting structure does not accept these neighboring commitments.

## Decision pauses

Pause only for a real decision, not at a fixed number of checkpoints. A useful pause contains:

- a brief description of the product consequence;
- the smallest concrete choice needed;
- at most a few answer options when they genuinely simplify the decision.

Do not lead with internal section names such as “Checkpoint 3,” “Navigation Model,” or “Governance” unless the audience requested technical process detail.

## Phase closure and continuation

A useful phase can end before the whole IA is complete. When the user asks for a summary, signals a pause, wants to decide whether to continue, or the current slice has reached its stated purpose, give the summary before any next-step suggestion. Make it complete for that stage rather than a teaser for another question.

Include only what is relevant:

- current product and problem understanding;
- choices the user has actually confirmed;
- reversible assumptions used to make progress;
- consequential unknowns or risks that remain;
- what this phase covers and deliberately does not cover;
- the few most relevant optional continuations.

Do not automatically open the next layer, generate a neighboring artifact, or end every coherent response with a question. If the user explicitly stops, close without a new decision request. When continued work is likely but not requested, an informational sentence is enough: the user may later deepen the IA, request a product sitemap, choose one goal for a user flow, or stop here.

For work that may continue in another session, offer—but do not create or persist without acceptance—a portable continuation note containing:

- project name or disambiguating identifier;
- current stage and intended outcome;
- confirmed decisions;
- reversible assumptions and open questions;
- produced outputs and their versions or dates;
- safest next useful action.

The note is a handoff aid, not hidden memory. Keep it small, reviewable, and attachable so the workflow remains portable in hosts without native Skill or memory support.

## Export request

An export request is another consequential step. Before creating a semantic file, diagram prompt, or visual-builder handoff:

- verify that every visible item belongs to a domain;
- verify that important containment and cross-domain relationships are explicit;
- verify that role combinations, local conventions, and lifecycle transitions are not hidden guesses;
- ask and stop if a remaining unknown would materially change the requested artifact;
- otherwise export a clearly marked Proposed or Approved model according to the user's intent.

Confirm the requested deliverable from the current conversation. A remembered output preference does not authorize a presentation, diagram, canvas, prototype, or other file.

## Quick provisional work

Use after an explicit request for speed, assumptions, or no questions, and also when an idea-stage user cannot yet answer specialist questions but a reversible proposal would teach them what matters. Keep the result compact: product understanding, candidate objects/content, initial organization and retrieval direction, material assumptions, and the next best check. Label it as a proposed starting point and do not imitate a complete report.

## Business and operating-model coupling

Business and IA decisions can shape each other. Inspect monetization, payment, commission, subscription, settlement, promotion, entitlement, ownership, or operational capacity only when they change identities, transactions, visibility, access, lifecycle, labels, or findability. Explain the structural consequence in product language. Do not claim that the business model must be decided before or after IA, and do not expand IA discovery into a complete business-model exercise without a request.

## Redesign and audit intake

Inspect current navigation, content inventory, analytics, search logs, user research, support issues, permissions, governance, and upcoming changes when available. Distinguish current-state evidence from target-state recommendations.

## User control

The user may skip questions, change sequence, request more or less depth, or focus on one IA component. Follow that direction. If skipped discovery weakens a high-impact claim, provide provisional work and make that limitation visible rather than silently claiming certainty.
