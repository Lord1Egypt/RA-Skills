## Description:

Connects OpenClaw agents to Reasonix desktop projects and sessions so they can list local projects, inspect session files, resume a selected project session, or start a new one against the shared ~/.reasonix store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who use Reasonix Desktop with OpenClaw use this skill to discover local Reasonix projects and continue or create project sessions from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Listing or resuming Reasonix desktop sessions can expose local project paths, topic metadata, and selected session history to the agent.

Mitigation: Use the skill only in trusted workspaces and confirm before operating on sessions that may contain sensitive context.

Risk: The packaged list-projects.sh helper has a command-execution risk when run with a malicious HOME environment.

Mitigation: Do not run that helper in untrusted wrapper or automation environments until the HOME-derived Python injection issue is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-reasonix-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Reasonix project paths, topic metadata, and selected session history.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
