## Description:

Provides LogSnag actions through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to publish LogSnag events and insights or update user profile properties through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run a remote installer without a separate approval step.

Mitigation: Review and install the oo CLI separately before enabling the skill, including any automatic agent-skill synchronization.

Risk: Actions use an OOMOL connection and some can change LogSnag data.

Mitigation: Understand that OOMOL handles requests and connected credentials, and confirm the exact data change before running write actions.

## Reference(s):

- [LogSnag API quick start](https://docs.logsnag.com/quick-start)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, API Calls, Guidance]

**Output Format:** [Shell commands with JSON payloads and structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may create or update LogSnag data; the skill requires confirmation before write actions.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
