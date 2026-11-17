## Description:

Autonomous agent that continuously creates, tests, and lists new SKILL.md files on OpenCollab, FreeLanceDAO, CryptoGigs, and x402 marketplaces; it iterates on underperforming skills and auto-deprecates skills with zero traction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and marketplace operators use this skill to generate, test, publish, track, and retire marketplace skill listings based on market demand and earnings signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated marketplace publishing can create or deprecate public listings without adequate human approval.

Mitigation: Require manual approval before every publish or deprecation action.

Risk: Generated skills may include unsafe instructions or secrets before publication.

Mitigation: Stage generated skills outside shared agent directories and scan generated content for secrets and unsafe instructions.

Risk: The artifact describes automation scripts, marketplace credentials, and scheduled behavior that are not included for verification.

Mitigation: Verify the required scripts, credentials, target directories, and scheduler configuration before enabling automation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ssidharhubble/skills/openclaw-listing-bot)
- [zo.pub publishing target](https://zo.pub/ssyopros/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown SKILL.md files with shell command guidance and listing metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces marketplace skill drafts, smoke-test steps, publish commands, and earnings or deprecation logs.]

## Skill Version(s):

1.0.18 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
