## Description:

Use the Altoviz connector to create customers and find, retrieve, or list customer records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can manage customer records in Altoviz through their connected account, including creating customers and searching or retrieving existing records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unreviewed remote code and introduce undisclosed persistent agent changes.

Mitigation: Install a reviewed, pinned oo CLI separately before enabling the skill, review any additional agent skills it installs or synchronizes, connect only the intended Altoviz account, and confirm customer-creation payloads.

## Reference(s):

- [Altoviz homepage](https://altoviz.com/en/)
- [Altoviz API authentication guide](https://developer.altoviz.com/docs/api/guides/authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Altoviz skill release](https://clawhub.ai/oomol/skills/oo-altoviz)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance, Text]

**Output Format:** [oo CLI commands with JSON inputs and structured connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected customer action and connected Altoviz account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
