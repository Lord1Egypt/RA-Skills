# Capability-aware execution and output routing

Read this reference when adapting the same IA work to different agents, chat surfaces, build environments, or installed tools.

## Route by capability, not brand

Use this evidence order:

1. capability visibly exposed in the current surface or tool list;
2. capability explicitly declared by the host for this session;
3. capability explicitly confirmed by the user;
4. otherwise **unknown**.

Unknown is not evidence of absence. Use portable text or a self-contained handoff and state what was not produced. Never claim to have rendered, inspected, installed, or executed something without corresponding evidence.

Product names are hints, not guarantees. Before choosing behavior or format, inspect the actual capabilities available in the current session:

- Can the agent ask a question, end the turn, and continue from the answer?
- Can it inspect attachments, URLs, repositories, or authorized connected sources?
- Can it search the public web without exposing private context?
- Can it create files or execute code?
- Can it render Mermaid reliably in the user's language and direction?
- Can it create a native document, artifact, app, canvas, or diagram?
- Can the result be visually inspected rather than merely generated?
- Is a diagram companion installed and authorized?

Never claim a capability from the model name alone. If an important capability is absent, use the strongest truthful fallback.

## Shared behavioral invariant

Every surface uses the same decision logic and semantic IA model. Environment adaptation changes pacing, reference delivery, and rendering—not architecture quality, evidence standards, or the meaning of the IA.

File-only and instruction-plus-knowledge surfaces must still follow the high-priority operating core: plain user language, outcome-based sufficiency, one coherent pass when possible, no silent neighboring product commitments, and no durable mutation without a current request. A larger context window or extended reasoning mode does not justify a longer interview or bilingual duplication.

Host memory, profiles, and prior-chat preferences do not change the current deliverable gate. Automatically supplied memory may adapt only low-risk response length or technical depth when consistent with the current turn. It cannot choose response language, current project, product context, artifact, scope, or evidence, and cannot authorize a file, canvas mutation, presentation, prototype, upload, persistence, or external action that the current conversation did not request or accept.

Without an explicit current request, do not create, update, persist, or claim to update Memory, Project Knowledge, Gem Knowledge, workspace context, or another durable project record.

If the host visibly performs or announces a durable memory action that the skill did not request and cannot prevent, do not treat that record as current product evidence or imply that the action was part of the ProPaymun workflow. State the host limitation only when it affects the user's task.

## Output ladder

### Level 0 — portable text

Use in any environment. Include:

- the architecture recommendation in plain language;
- an indented hierarchy of information domains and important objects/content;
- a concise list of typed cross-relationships that the tree cannot express;
- findability, access, and consequential uncertainty only where relevant.

This is a complete fallback, not an apology or a placeholder.

### Level 1 — structured text

Use Markdown tables or Mermaid only when they improve comprehension. Preserve a textual equivalent. For unreliable RTL rendering, keep the explanation and hierarchy in the user's language and use concise English technical IDs only where they improve renderer reliability.

### Level 2 — native artifact

Use a document, interactive HTML, artifact, canvas, or generated app when the environment supports it and the user requested a durable artifact. The artifact must render the canonical semantic model rather than invent a new structure.

### Level 3 — professional diagram

Use a native diagram tool or an optional companion when precise geometry, editable connectors, workshop facilitation, or formal handoff justifies it. Draw.io suits precise editable handoff; Excalidraw suits conceptual explanation and workshops. Do not require either companion for a complete IA and do not install one without authorization.

## Downstream composition

When the current conversation explicitly requests a UI, image, prototype, sitemap, user-flow, presentation, document, builder prompt, or technical mapping, do not reject the request merely because it is not an IA representation. For an existing IA, stabilize it to the needed readiness and create an IA Reference Lock. For a standalone product sitemap or user flow, create only the versioned minimum semantic substrate required by that artifact. Then:

- produce the derivative with a capability visibly available and authorized in the current surface; or
- provide a self-contained handoff to the relevant downstream capability.

Preserve the locked domains, items, relationships, labels, findability, access/privacy constraints, evidence state, and unresolved assumptions. Mark any downstream addition as an adaptation or new proposal. Do not present a derivative as new IA evidence.

### Product sitemap or user flow without prior IA

Do not require a complete IA engagement. For a product sitemap, establish the relevant audience, destinations, canonical content/objects, hierarchy, labels, access, and entry/recovery context. For a user flow, establish the actor, goal, trigger, relevant objects, states, permissions, decisions, failure/recovery, and success. Record the substrate version and assumptions so a later IA can reconcile rather than silently replace it.

When “sitemap” may mean an XML/SEO URL inventory, infer the intended artifact from product/UX language versus crawl/index/URL language. Ask one disambiguation question only when the distinction remains material and unresolved.

## Surface profiles

### Conversation-first chat

Default to Level 0. Ask before creating a heavy file or visual. If the user requests a richer output, select the highest available truthful level.

### Chat with artifact or canvas capability

Keep intake conversational. After sufficiency, use Level 2 when an interactive or durable view materially improves review. Do not skip clarification merely because a canvas is available.

### CLI or agent with files and code execution

May produce and validate structured IA JSON, HTML, SVG, or other editable sources. Run and inspect deterministic helpers when available. Distinguish syntax validation from visual inspection.

### Prompt-to-app or build-first surface

Treat it as a downstream renderer, not the default IA reasoning environment. First stabilize the IA in a conversation-capable environment. Then provide a self-contained prompt that carries the locked IA and clearly names whether the target is an IA review blueprint or a product experience derived from it. If the builder is the only available surface, use portable text and questions first; do not mutate the canvas while material unknowns remain.

### Diagram-capable surface

Use Level 3 only when the requested IA question benefits from a diagram. Keep the diagram scoped and preserve text for accessibility and portability.

## Research routing

Use web or connected sources when they can materially change terminology, domain rules, compliance, content inventory, or current-state understanding. Do not turn missing search capability into fabricated evidence. A build surface may be able to create visuals but lack reliable browsing; these capabilities must be judged separately.

## Installation and configuration are different

- A native Skill runtime discovers `SKILL.md` and its resources.
- A web Project, Gem, or custom Agent usually needs a persistent instruction plus an uploaded knowledge file.
- A one-off chat can use the Workspace Kit knowledge file as an attachment plus the short workspace instruction.

Do not call file upload or prompt pasting a native Skill installation. The behavior contract stays the same, but persistence, automatic triggering, tools, and context limits may differ by surface.

The repository may document verified examples, but the portable contract must not name unverified services as supported. A file-capable environment can use the Workspace Kit when the user designates it as operating guidance; that is session-scoped use, not proof of installation, persistence, automatic activation, or full capability parity.
