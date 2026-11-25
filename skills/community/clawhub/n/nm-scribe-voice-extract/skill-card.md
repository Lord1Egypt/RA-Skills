## Description:

Extracts a user's writing voice from text samples via SICO comparative analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Writers use this skill to compare anonymized writing samples with model-generated baselines and create a followable voice profile and default register for consistent drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writing samples may contain sensitive information and can be copied into persistent profile storage without a retention warning; existing samples may also be overwritten.

Mitigation: Treat samples as sensitive, remove identifying details before intake, choose a profile destination deliberately, and back up or review existing sample files before copying new ones.

Risk: The security review was partial because two local path references could not be resolved, leaving evidence about those references incomplete.

Mitigation: Review the unresolved path references and their targets before relying on the skill in a sensitive workflow.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-scribe-voice-extract)
- [Scribe plugin page](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown voice profile and register, with a JSON sample manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses comparative writing samples; documented intake thresholds are at least three samples and 500 words total.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
