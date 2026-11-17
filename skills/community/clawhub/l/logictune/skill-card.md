## Description:

Applies AI LogicTune's strategic working principles to a requested task, or adds them to an agent's operating instructions when the user explicitly requests persistent setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redrookai](https://clawhub.ai/user/redrookai)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use LogicTune to guide planning, research, coding, and extended tasks. On explicit request, they can merge its principles into their active workspace instructions for future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Merging guidance into AGENTS.md can change the agent's behavior in future sessions.

Mitigation: Use task-only guidance for temporary use; request persistent activation explicitly and review the AGENTS.md changes before keeping them.

## Reference(s):

- [ClawHub release](https://clawhub.ai/redrookai/skills/logictune)
- [Project homepage (publisher-provided metadata)](https://github.com/RedRookAI/openclaw-skills/tree/main/skills/logictune)
- [Behavioral checks](references/checks.md)
- [OpenClaw workspace instructions](https://docs.openclaw.ai/concepts/agent-workspace)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent setup may update the active workspace's AGENTS.md only when explicitly requested.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
