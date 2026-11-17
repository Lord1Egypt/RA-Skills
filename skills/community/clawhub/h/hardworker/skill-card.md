## Description:

Forces persistent problem solving using a Striver mindset and structured breakthrough methodology. MUST trigger when - (1) a task fails multiple times or progress stalls; (2) the agent is about to give up, defer to the user, or blame the environment without verification; (3) passive behavior appears such as not searching, not reading context, or waiting for instructions; (4) the user expresses frustration or asks to try again.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to keep an AI coding or troubleshooting agent engaged when tasks fail repeatedly, progress stalls, or the agent is tempted to defer too early.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad autonomous troubleshooting with files, local permissions, and APIs.

Mitigation: Use it cautiously in workspaces with sensitive files, live credentials, production APIs, paid services, or tasks where the agent should pause before expanding scope.

Risk: Persistent problem-solving pressure can reduce user control over when the agent stops or asks for confirmation.

Mitigation: Require explicit user checkpoints before high-impact actions, production changes, credential use, or paid service calls.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown instructions and trigger text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload; the skill changes agent behavior through prompt guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
