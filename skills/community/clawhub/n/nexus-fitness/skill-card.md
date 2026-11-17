## Description:

Log and track workouts, meals, weight, and fitness friends with OAuth-secured cloud storage and conversational Nexus CLI queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiluazen](https://clawhub.ai/user/kiluazen)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help users install and operate the Nexus CLI for explicit workout, meal, weight, history, update, authentication, and fitness-friend workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can upload sensitive fitness, meal, weight, and friend-linked data to a Nexus cloud account.

Mitigation: Review the privacy policy and log only data the user is comfortable storing in the Nexus cloud account.

Risk: The skill asks the agent to install and run the external nexus-fitness CLI package.

Mitigation: Verify that nexus-fitness is the intended package before installing or executing commands.

## Reference(s):

- [Nexus website](https://kushalsm.com/nexus)
- [Nexus GitHub](https://github.com/kiluazen/nexus)
- [Nexus privacy policy](https://kushalsm.com/nexus/privacy-policy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Nexus CLI commands, structured fitness entry examples, and concise operational guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
