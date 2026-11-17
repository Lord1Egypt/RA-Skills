## Description:

Helps developers and privacy-conscious users plan and validate local LLM workflows on consumer CPU or GPU hardware without cloud-only dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, privacy-conscious users, hobbyists, and small teams use this skill to choose and implement practical local LLM setup workflows, checklists, scripts, or decision support for ordinary home machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Demand-evidence claims may not directly support every local LLM setup scenario.

Mitigation: Treat demand evidence as context and validate recommendations against the user's hardware, operating system, model size, and tooling constraints.

Risk: Broad implicit triggers could route adjacent AI, privacy, or workflow questions to this skill unnecessarily.

Mitigation: Confirm the user's intent and local LLM relevance before applying the setup workflow.

Risk: Generated commands or configuration may be unsuitable for a user's hardware or environment.

Mitigation: Prefer CPU-safe or small-model workflows, state assumptions, and include verification commands before changes are treated as complete.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/local-llm-setup-advisor-133318)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown responses with checklists, commands, configuration snippets, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verification notes, local-hardware assumptions, and follow-up risks.]

## Skill Version(s):

0.1.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
