## Description:

Coordinates task-specific sub-agents such as Learner and Critic agents so a main agent can delegate research, evaluation, communication, and result synthesis for complex tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchunwanwusheng](https://clawhub.ai/user/yangchunwanwusheng)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to coordinate one-shot sub-agents for search, quality review, multi-agent collaboration, and final response synthesis. It is most relevant when a main agent needs to split work across Learner, Critic, and shared-memory workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task-specific sub-agents may receive sensitive prompts, files, or shared-memory context if the main agent delegates too broadly.

Mitigation: Review sub-agent prompts before use and avoid sending secrets or sensitive private data to Learner, Critic, or shared ontology memory unless that sharing is intended.

Risk: Multi-agent outputs can mix search, critique, and synthesis results in ways that may obscure which agent produced a claim.

Mitigation: Have the main agent summarize each sub-agent result before synthesis and preserve source attribution for important decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangchunwanwusheng/skills/multi-agent-coordinator)
- [ClawHub publisher profile](https://clawhub.ai/user/yangchunwanwusheng)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline code examples and command-oriented coordination patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces coordination plans, sub-agent task prompts, evaluation guidance, and synthesized final responses; no executable code is bundled.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and artifact version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
