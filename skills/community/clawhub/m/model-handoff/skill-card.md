## Description:

Maintain a HANDOFF.md file in the workspace so context survives seamlessly when switching between LLM models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bwiley1989](https://clawhub.ai/user/bwiley1989)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve active project context when switching between LLM models or resuming work in a new model session. It guides the agent to create and maintain a compact HANDOFF.md file and to point successor agents to it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent handoff files can expose sensitive workspace details, credential-file paths, or personal context if shared.

Mitigation: Review HANDOFF.md before sharing it and remove private profile, memory, and credential-file references.

Risk: AGENTS.md changes can affect how future agents behave in the workspace.

Mitigation: Require explicit user approval and review the diff before adding or changing AGENTS.md instructions.

Risk: Proactive handoff updates can preserve stale or unnecessary context.

Mitigation: Keep entries concise, refresh the last-updated timestamp, and remove completed or outdated project details on each update.

## Reference(s):

- [HANDOFF.md Starter Template](references/template.md)
- [ClawHub skill page](https://clawhub.ai/bwiley1989/skills/model-handoff)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown files and concise handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates HANDOFF.md and may update AGENTS.md instructions when explicitly approved.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
