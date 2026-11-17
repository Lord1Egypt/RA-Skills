## Description:

This skill lets an agent send messages to Orimon through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with Orimon connected through OOMOL can inspect the send-message action schema and send a message to an Orimon chatbot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions run remote installers whose contents were not inspected.

Mitigation: Review installer contents and prefer a separately reviewed, pinned CLI installation.

Risk: Startup skill synchronization may install or refresh other agent skills.

Mitigation: Decide whether synchronization is appropriate; use OO_SKILLS_SYNC_DISABLED to disable it when desired.

Risk: Messages and connected-account access pass through OOMOL.

Mitigation: Use only data appropriate for the OOMOL service.

## Reference(s):

- [Orimon](https://orimon.ai)
- [Orimon API documentation](https://orimon.gitbook.io/docs/developer-api/getting-started-with-apis#how-to-generate-your-developer-api-key)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: frontmatter, server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
