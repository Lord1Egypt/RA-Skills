# How a System Is Composed and Designed

## The runnable system instance: the center where all parts act together

Every OpenXSys run centers on a currently active system instance. Prompts and methods are resources that instance uses in the present situation. The instance may exist in the working picture constructed by the model for this run, or be carried over time by a user-owned `SYSTEM.md`, works, code, data, and connections. The active picture and the persistent system refer to the same real object and recalibrate each other as new evidence arrives.

A system instance lets the AI answer the semantic questions below. Any natural-language structure suited to the object may carry them; the user continues to enter through their own words and materials.

| Semantics | What must become clear |
| --- | --- |
| **Identity and purpose** | What system this is, whom it serves, what we want to understand or change now, and what would count as a valuable result. |
| **Boundary and scale** | Where we are looking, how many levels and how much time the view spans, what is environment for now, and when it needs to come inside the boundary. |
| **Reality, observation, and model** | Who holds the object's actual state, which signals are visible now, and which statements are explanations, hypotheses, or unknowns. |
| **Composition and relations** | Which people, AIs, tools, materials, rules, and other systems participate, and which relations actually carry effects. |
| **Constraints and resources** | What limits the whole, what can change, and where the constraint may move afterward. |
| **Capabilities** | What the system can do now, what has been validated in reality, what is still a candidate, and what the goal still requires. |
| **Ownership and authority** | Who owns materials, state, works, decisions, and execution; who can correct, stop, withdraw, or exit. |
| **Works and actions** | How understanding reaches a person, how intent reaches reality, and how another person or AI can take over. |
| **Feedback and evolution** | What evidence changes the model, what result changes a capability, relation, boundary, or goal, and which downstream parts must then be reviewed. |

The current run activates the parts relevant to its purpose. A new scale, relation, or capability gap causes the corresponding part to unfold. Any component, relation, or capability can recursively become another system instance; after understanding it, return to the higher level and ask how it changes the whole. A system's complexity comes from interacting levels and change.

## Stable semantics and the active picture

A system entry preserves relatively stable understanding, capabilities, relations, and agreements that can change future work. The current run forms an active picture: present purpose, latest materials, actually available tools, current authority, effects awaiting confirmation, and changes now under way. When the active picture closes, only what changes a future run enters the persistent system.

The current chain of thought, tool logs, and temporary guesses remain in the active picture. State that changes future work enters the persistent system. A real change happening now may directly revise the entry. The persistent system gives the run a starting point; the run uses feedback from reality to revise the persistent system.

## See three systems at once

The **real object** has its own state, history, and effects: a metro operates, a team divides work, a work has real readers. The **system built to understand or change it** consists of ways of observing, explanations, people, AIs, tools, and organizational relations. The **computer and AI tool that hosts the run** carries communication, reasoning, execution, and retained results. All three can affect one another. Loading service data into a model shows that the data was observed; the operator confirms the line's state. A research work may change understanding; changing the actual service still requires a system able to act.

The run may begin with any participant in the relation among people, AI, computers, and other real systems. A person can state intent; a computer can observe a file change; a model can discover an opportunity during an existing run; a domain system can deliver an event. The person, model, and computer may occupy different physical locations. After choosing the current scale, identify which party actually owns content and action rights.

## How a concrete system is composed

| Part | Relations that must be clear |
| --- | --- |
| **Object and owners** | What whole is being understood or changed, whom it affects, and who maintains purpose, materials, tools, and permissions. The hierarchy may change with purpose. |
| **System description** | Let a new AI, person, or host understand what this is, what is known, where important facts live, and how to take over. Natural language connects to materials that are actually useful. |
| **Understanding and evidence** | What observations can see, at what scales an explanation holds, and which counterevidence would change it. Different participants may hold different models. |
| **Working arrangement** | Which people and tools provide information, computation, works, or action; what reality itself determines and what the system is authorized to change. |
| **Works and handoff points** | How a person gains understanding or uses a result, where work can continue, and how a successor obtains new evidence and the current view. |
| **Feedback and connections** | Which person, tool, or system receives actual effects, how independent systems lend one another capability, and who changes a long-term arrangement after results repeat. |

These are design perspectives. Studying a concept may require only an entry, one useful explanation, and a checkable source. A long-lived organizational system may have several observation points, independent permissions, and a few handoffs that must remain reliable. Every added component should be able to say which relation it changes, what value it produces, and who maintains it.

## Stable relations and changeable implementations

At the scale used for a piece of work, treat real decision rights, authoritative state sources, resource ceilings, and confirmed timing as constraints. Team conventions, user preferences, vendors, models, papers, and tools may change on their own timescales. New material affects only the judgments it truly changes. Owners with decision rights confirm long-term direction, permissions, and publication requirements.

Put natural language where it best expresses intent, meaning, and reasons for judgment. Code can carry precise, repeated, auditable work, such as checking a data set or whether a change took effect. Treat the environment's existing permission system, data interfaces, and collaboration practices as ready-made parts. A new tool should have a real object and an observable effect.

## A small example

A community theater already has a program schedule. Its coordinator owns the official version; sound and operations each hold their own view; a late review creates a different failure. When opening a system for the theater, “the versions match” can be one condition and “review completed after the last change” another. They belong to different relations and timescales. A useful system can use a table as the daily entry, a checking tool to surface divergence, and the coordinator to decide which action actually changes the official state. When tools and roles change, the checking purpose and authoritative source of state can remain.
