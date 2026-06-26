# Framework Figure Taxonomy

Use this taxonomy before writing prompts or generating images. Routing is multi-label first, then primary subtype selection.

## Core Subtypes

| Subtype | Reader Question | Best Paper Slot | Required Decisions |
|---|---|---|---|
| Method framework | What is the proposed method, and why are its parts organized this way? | intro / method | modules, novelty highlight, data/control flow, output |
| Architecture | Which components interact, and what is trained or inferred? | method / system | boundaries, interfaces, parameters, losses, inference path |
| Pipeline / process | What happens step by step? | method / system | temporal order, stages, state updates, feedback loops |
| Agent workflow | What does the agent observe, decide, call, verify, and update? | method / agent system | planner, model/tool calls, memory, verifier, loop |
| System/data flow | Where do data, users, tools, and model components move? | system / method | lanes, data stores, services, latency or control boundaries |
| Mechanism intuition | Why does the central idea work? | intro / method / analysis | cause-effect chain, variable roles, constraints |
| Case walkthrough | How does one example move through the framework? | intro / qualitative / appendix | example states, before/after, stage labels |
| Evidence-linked framework | How does the framework connect to evidence or ablations? | results / rebuttal | evidence cards, comparison boundary, claim mapping |
| Failure-aware framework | Where can the system fail, and what boundary should reviewers understand? | analysis / limitation / rebuttal | failure modes, triggers, affected modules, mitigation |

## Routing Axes

- Reader question: identity, sequence, interaction, mechanism, example behavior, evidence support.
- Logical gap: problem-to-method, method-to-mechanism, mechanism-to-result, result-to-claim.
- Layout skeleton: left-to-right pipeline, layered stack, hub-and-spoke architecture, swimlanes, modular grid, loop, before/after split.
- Density: intro overview, method technical, appendix dense, rebuttal conservative.
- Paper slot: intro, method, system, analysis, appendix, rebuttal, slides.
- Multi-label status: record all applicable labels, then select a primary subtype.

## Default Primary-Subtype Rule

- For method sections, default to `method_framework` plus `architecture` or `pipeline_process`.
- For agentic systems, default to `agent_workflow` plus `system_data_flow`.
- For intro figures, default to `method_framework` plus `mechanism_intuition`.
- For qualitative examples, default to `case_walkthrough` plus `pipeline_process`.
- For rebuttals, default to `evidence-linked framework` or `failure-aware framework`.

Do not lock the primary subtype from prose alone when visual comparison would help. Recommend a 6-image candidate board.
