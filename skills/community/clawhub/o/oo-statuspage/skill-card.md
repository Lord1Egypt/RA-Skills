## Description:

Use the OOMOL-connected Statuspage account to read, create, update, and delete Statuspage data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams can inspect Statuspage pages, incidents, components, and events, or make approved changes to incidents and components through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote software.

Mitigation: Review the CLI installation and use a verified release before allowing setup.

Risk: The required CLI can install additional agent skills through automatic synchronization.

Mitigation: Consider disabling automatic skill synchronization using the vendor's documented control.

Risk: The connected account can create, update, or delete Statuspage data.

Mitigation: Connect only the intended account and permissions, and keep the skill's confirmation requirements for changes and deletion.

## Reference(s):

- [Statuspage](https://www.atlassian.com/software/statuspage)
- [Statuspage API documentation](https://developer.statuspage.io/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Statuspage data in JSON with concise text summaries; oo CLI commands for execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and delete actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
