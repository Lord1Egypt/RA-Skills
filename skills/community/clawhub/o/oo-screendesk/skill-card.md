## Description:

Use an OOMOL-connected Screendesk account to read recordings and transcripts, find workspace users, and update recording details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users can use this skill to retrieve Screendesk recordings and transcripts, search workspace users, and update recording titles, summaries, or descriptions. Updates should be reviewed and confirmed before they are run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic remote CLI installation step has unverified contents and exact release behavior.

Mitigation: Review the installer and release yourself before installing or updating the CLI.

Risk: Automatic skill synchronization may change agent skills without clear disclosure.

Mitigation: Review the synchronization behavior and set OO_SKILLS_SYNC_DISABLED if automatic synchronization is not acceptable.

Risk: The skill uses the connected Screendesk account, and recording updates change stored data.

Mitigation: Grant only the required account permissions and confirm the exact recording update before running it.

## Reference(s):

- [Screendesk](https://screendesk.io)
- [Screendesk API documentation](https://docs.screendesk.io/api/screendesk-api/overview)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-screendesk)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON action responses summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can retrieve recordings, transcripts, and user listings; supports updates to recording titles, summaries, and descriptions.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
