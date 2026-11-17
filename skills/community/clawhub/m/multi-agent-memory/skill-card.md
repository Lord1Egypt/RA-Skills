## Description:

Multi Agent Memory defines a shared-memory and project-collaboration workflow for multiple agents, with isolated project state, shared knowledge bases, cross-project search, versioned records, milestones, weekly reports, and handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucey0017-cloud](https://clawhub.ai/user/brucey0017-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent teams use this skill to initialize and maintain OpenClaw project memory for multi-agent work, including status tracking, shared knowledge capture, weekly reporting, milestone tracking, and handoff documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts create, read, search, and archive shared project-memory files under a broad OpenClaw path.

Mitigation: Run the skill under a non-root account with a dedicated workspace and restrict permissions on the OpenClaw memory directory.

Risk: Project or phase names supplied to scripts may allow writes outside intended folders or unsafe command behavior before input validation is added.

Mitigation: Use only trusted project and phase names, avoid shell metacharacters and path separators, and review generated paths before execution.

Risk: Shared knowledge bases, reports, and handoff documents can retain sensitive project data.

Mitigation: Do not store secrets, credentials, regulated data, or confidential material in shared memory, weekly reports, archives, or handoff files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucey0017-cloud/skills/multi-agent-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash shell commands and generated project-memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates project status, todos, milestone, weekly summary, handoff, knowledge-base, and archive files under an OpenClaw workspace.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
