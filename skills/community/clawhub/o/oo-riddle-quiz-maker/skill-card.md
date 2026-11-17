## Description:

Use the oo CLI to read and manage Riddle Quiz Maker projects, riddles, and tags through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to inspect Riddle projects, retrieve embed information, and manage riddles and tags through their connected Riddle account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute an unverified installer, and bundled-skill synchronization may affect more agent hosts than intended.

Mitigation: Review and install the CLI separately, check its synchronization settings, and limit changes to intended hosts.

Risk: Publishing riddles or performing destructive actions can change or remove live content.

Mitigation: Retain the documented approval steps and confirm the exact target and effect before these actions.

## Reference(s):

- [Riddle Quiz Maker](https://www.riddle.com)
- [Riddle API documentation](https://www.riddle.com/help/api)
- [oo CLI repository (tool reference)](https://github.com/oomol-lab/oo-cli)
- [Riddle Quiz Maker ClawHub release](https://clawhub.ai/oomol/skills/oo-riddle-quiz-maker)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [JSON connector responses and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by selected Riddle action; state-changing actions follow the skill's approval steps.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
