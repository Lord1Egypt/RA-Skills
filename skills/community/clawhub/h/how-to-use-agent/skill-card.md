## Description:

Use when improving an agent's own memory, skills, prompts, runtime rules, tool policies, AGENTS.md/agent.md files, or when adapting ideas from other agent projects into the current agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangrichao2020](https://clawhub.ai/user/huangrichao2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to plan and review agent self-improvement work across memory, prompts, skills, runtime rules, and related documentation. It emphasizes consent, architecture notes, progressive rollout, rollback planning, verification, and handoff manuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent self-improvement can introduce incorrect or misleading guidance into prompts, memory, skills, policies, or runtime documentation.

Mitigation: Review each proposed change before deployment and require the approval prompt to identify affected files, rationale, risks, and rollback.

Risk: Broad memory or prompt rewrites can remove important operating constraints or make rollback difficult.

Mitigation: Do not approve broad rewrites unless the impact is understood; prefer small phases, preserved data, progressive rollout, verification, and clear rollback paths.

Risk: Patterns adapted from external agent projects may be incompatible with the current agent environment.

Mitigation: Use source-level research to produce an adaptation memo, then land the smallest safe local experiment instead of copying external code directly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangrichao2020/skills/how-to-use-agent)
- [Publisher profile](https://clawhub.ai/user/huangrichao2020)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional code, shell command blocks, architecture notes, rollout plans, consent prompts, verification notes, and work manuals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before modifying agent-owned instruction, memory, skill, prompt, policy, or runtime surfaces.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
