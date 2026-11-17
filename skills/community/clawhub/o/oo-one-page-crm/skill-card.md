## Description:

Use OnePageCRM to read, create, and update contacts and deals through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams can use the skill to look up OnePageCRM contacts and deals, or create new contacts and deals. It requires an installed, signed-in oo CLI connected to the intended OnePageCRM account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute changing remote code and may make unexplained changes to other agent skills.

Mitigation: Review and explicitly approve a fixed CLI version before setup, and check automatic skill installation and synchronization settings.

Risk: The skill accesses a connected CRM account, and create actions change CRM data.

Mitigation: Connect only the intended account and keep the required user confirmation of the exact write payload and effect.

## Reference(s):

- [OnePageCRM homepage](https://www.onepagecrm.com/)
- [OnePageCRM API documentation](https://developer.onepagecrm.com/api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-one-page-crm)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON payloads and connector responses, with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CRM records returned by read actions; create actions require user confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
