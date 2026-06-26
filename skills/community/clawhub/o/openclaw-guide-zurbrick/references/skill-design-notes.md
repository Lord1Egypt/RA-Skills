# Skill Design Notes for OpenClaw

## Prefer a skill when
- the capability is mostly procedural knowledge
- the agent needs a repeatable workflow
- supporting examples, references, or scripts would help
- a user may invoke it directly or the model may load it contextually

## Prefer retrieval / progressive disclosure when
- the information is large, specific, or rarely needed
- loading it into the main prompt every session would be wasteful
- the agent can fetch the right detail on demand

## Prefer a sub-agent when
- the task is specialized enough to deserve a different prompt/model/context
- reviewing the output is easier than carrying the whole specialty in the main agent
- the work is long-running or cognitively separable

## Prefer a new first-class tool only when
- existing tools + skills + retrieval + subagents have already failed repeatedly
- the task is frequent and expensive to get wrong
- a deterministic primitive materially reduces failure rate or complexity

## Smell tests
If a proposal mainly sounds elegant, pause.
If the pain is not recurring, pause.
If the maintenance cost is unclear, pause.
