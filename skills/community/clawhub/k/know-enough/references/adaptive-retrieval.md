# Adaptive Retrieval

`know-enough` decides what knowledge to acquire and which functional strategy can supply it. The harness or available orchestration discovers and selects existing skills, tools, or services to execute that strategy. Do not assume a named skill, service, corpus, or capability is installed or accessible. These capability labels describe intent, not executable APIs.

## Minimal acquisition cycle

1. **Need.** Identify the missing information that could change the answer or next decision. Reuse the current knowledge state: if context and evidence already suffice for the task and risk, stop without searching.
2. **Sources and capabilities.** Select relevant sources using the existing registry's roles and selection rules when available. Check authority, scope, freshness, actual access rights, and the functional capabilities the harness can really use. A registry entry does not grant access. Do not invent capabilities or corpus names to fit a preferred plan.
3. **Minimal plan.** Choose the shortest, least costly available path that can meet the evidence requirement. State the expected result of each step. Start with direct reading or exact lookup when sufficient; combine capabilities only to resolve a material need.
4. **Delegated execution.** Let the harness map the plan to available means and use them. Carry source identifiers, document versions/dates, passage or row locations, excerpts, and references through each step so claims can cite the evidence actually consulted. Prefer original passages or records over generated retrieval summaries for material claims. Reuse the existing knowledge state and provenance mechanisms; do not create another registry or evidence system.
5. **Verification.** Apply the main skill's relevance, authority, freshness, scope, coverage, and contradiction checks. Inspect original passages and search scores in context; there is no universal score threshold. Semantic proximity, a classification result, or a successful join is not proof that a factual claim is true. For linked evidence, verify identifiers and the meaning of the relationship rather than trusting execution success.
6. **Stop or deepen.** Stop at knowledge that is necessary and sufficient for the task and its risk, not exhaustive corpus coverage. Otherwise take one targeted step whose result could change the decision. If accessible means cannot supply the missing evidence, report the limit and whether progress can safely continue; do not repeat ineffective searches indefinitely.

Reuse the main skill's output contract, including `Sufficiency: ENOUGH / NOT ENOUGH`. Explain the stopping judgment and cite consulted sources rather than merely listing a proposed search plan.

## Functional capabilities

| Capability | Prefer when | Check |
|---|---|---|
| `direct_read` | A source is identified, a file is targeted, or a small note set is sufficient | Read the relevant part; do not scan large corpora blindly. |
| `structured_query` | Exact values, combined numeric/categorical filters, aggregations, or already structured relationships determine the answer | Inspect schema, business definitions, units, and stable identifiers; retain query logic and supporting records. |
| `lexical_search` | References, codes, acronyms, or exact business terms identify evidence | Account for spelling, punctuation, and abbreviation variants; inspect the matching passage. |
| `semantic_search` / `hybrid_search` | The need is conceptual or vocabulary varies; use hybrid when both exact terms and meaning matter | Confirm relevance in original passages and interpret scores in context, without a universal threshold or an inference of authority from similarity. |
| `relationship_lookup` | Established relationships connect entities, sources, or data | Use reliable identifiers and attested relationships; do not infer links from similar names alone. |
| `document_preparation` | A relevant, accessible source exists but its current form cannot be used | Delegate preparation to an available capability within existing authorization. Do not automatically ingest or transmit content without authorization; if authorization is missing, explain the needed action and scope. |
| `classification` | An ambiguous semantic choice would substantially change the acquisition plan | Optional. Prefer rules or the active model's reasoning for simple cases; a specialized classifier is never a prerequisite. |

All capabilities are optional. If one is absent or access is denied, use a legitimate available alternative or state the limitation. Do not install technology or trigger tool creation by default. A knowledge gap is not by itself a capability-creation justification.

When specialized classification is useful and available, send only the useful, authorized context. If it is absent, disabled, fails, or is ambiguous, the active model remains responsible for a reasoned fallback. Classification confidence does not establish evidence sufficiency.

## Handoff to existing retrieval and classification capabilities

Follow the selected capability's installed instructions and actual request/response contract. Reuse its configuration and transport; do not create a duplicate skill or client. Discover supported search modes from the deployment, and request hybrid search or reranking only when actually exposed. A generated answer with citations is not necessarily an original passage: preserve the citations as returned, identify the answer as a synthesis, and obtain the original evidence when the claim and risk require it. Do not invent missing identifiers, page numbers, dates, or server features. An explicit no-answer response describes that search's coverage, not proof that the fact does not exist.

For an optional classification handoff:

1. Confirm that an available, approved deployment can answer the needed judgment. Installed model weights or a registered tool alone do not prove that the serving endpoint is compatible or authorized for the context. Keep deployment settings and secrets in the environment that owns the capability.
2. State the bounded judgment and supply only the minimal authorized context. Use separate named questions for conditions that can both hold, such as structured filters and conceptual retrieval needs; do not force them into a mutually exclusive choice. Use a named choice for exclusive alternatives and an ordered rubric for a score.
3. Preserve question identifiers, returned values/distributions, rubric meaning, and available model/provider information. Check missing answers, incompatible types, and execution errors through the selected capability's existing validation. Do not replace missing values with zero, round a fractional rubric score into a category, or treat a confidence statistic as factual correctness.
4. Use the judgment to inform a targeted acquisition plan, then check source evidence normally. Do not introduce universal decision thresholds. If the result is ambiguous, malformed, unavailable, or outside the approved deployment, return to the active model's reasoning without automatically switching to another service or repeatedly retrying.

## Conceptual plan

Use a few lines of ordinary language when helpful:

> Knowledge objective → desired capability/capabilities → accessible sources → expected evidence → stopping criterion

For each step, explain the result needed for the next step. This is not a required schema, configuration, or interpreted language.

Examples:

- **Exact reference:** find the current requirement for code R-17 → targeted reading or lexical search → accessible approved manual → the matching passage with version and location → stop once applicability and current authority are established.
- **Structured question:** identify active facilities with capacity at least 20 tonnes → structured query → accessible facility records and dictionary → filters, units, facility IDs, and matching rows → stop when the exact criteria are answered with adequate coverage. Semantic search adds nothing if the query suffices.
- **Exploratory question:** understand why teams bypass a review step → lexical, semantic, or hybrid search according to what is available → accessible procedures and incident narratives → relevant original passages with source roles and dates → stop once material explanations are supported and remaining uncertainty is explicit. Text may come first; structured follow-up is needed only if it changes the answer.
- **Composite question:** find eligible facilities that have handled a similar test → structured filtering, documentary search, then relationship lookup as needed → authorized facility records and test reports → qualifying rows plus passages linked by verified facility IDs → stop once both eligibility and relevant experience are supported. Reverse or shorten this order if the question or initial evidence warrants it; there is no mandatory structured-then-semantic sequence.

## Result distinctions

| Observed state | Response |
|---|---|
| No result | State what was searched and its coverage. Try a targeted variant or another accessible source if useful; no match alone does not prove nonexistence. |
| Source inaccessible / capability unavailable | State the access or execution limit without pretending the source was searched. Use an authorized alternative if adequate; otherwise report missing evidence. |
| Contradictory evidence | Preserve and cite both claims; check scope, dates, and authority. Deepen proportionately or report unresolved conflict, using available reconciliation support when needed. Do not silently choose the higher similarity score. |
| Insufficient evidence | State which claim or scope is unsupported even if some results were returned. Obtain one specific missing piece if possible; otherwise return `NOT ENOUGH` with the practical limit. |

Do not confuse these states or repeat a search unless there is a concrete reason to expect decision-changing evidence.
