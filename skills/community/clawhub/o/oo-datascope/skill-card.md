## Description:

Use an OOMOL-connected account to read, create, and update DataScope data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using DataScope through an OOMOL-connected account can ask an agent to retrieve answers, locations, and metadata list elements, or to create and update supported records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback recommends executing a downloaded installer whose contents were unavailable for inspection.

Mitigation: Prefer installing and verifying the CLI yourself, and require approval before a downloaded installer runs.

Risk: The OOMOL connection mediates access to DataScope, and create or update actions can change account data.

Mitigation: Review the action and exact payload before confirming any write; retain the skill's explicit confirmation requirement for changes.

## Reference(s):

- [DataScope API documentation](https://dscope.github.io/docs/)
- [DataScope homepage](https://www.mydatascope.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Text]

**Output Format:** [JSON action results and oo CLI commands, with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that create or update records require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.5 (source: frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
