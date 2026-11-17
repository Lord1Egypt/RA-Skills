## Description:

Connects an agent to Ticketmaster through an OOMOL-connected account for event, venue, attraction, classification, and season ticketing actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with an OOMOL-connected Ticketmaster account can search for and retrieve event, venue, attraction, and classification information. They can also run season ticketing commands after reviewing the action schema and confirming any state changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded CLI software that has not been verified, and the CLI may also synchronize additional agent skills.

Mitigation: Install a fixed CLI release and consider setting OO_SKILLS_SYNC_DISABLED=1 to disable additional skill synchronization.

Risk: Season ticketing actions can change Ticketmaster state, and the hosted connector implementation has not been verified.

Mitigation: Review the action schema and confirm each exact payload and effect before running a change; ensure you are comfortable with OOMOL handling requests and connected credentials.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-ticketmaster)
- [Ticketmaster](https://www.ticketmaster.com)
- [Ticketmaster Discovery API documentation](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [JSON connector payloads and returned data, with text summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Season ticketing actions can change state and require confirmation before execution.]

## Skill Version(s):

1.0.6 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
