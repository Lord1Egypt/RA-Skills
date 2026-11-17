## Description:

Use the oo CLI to read Lever postings, opportunities, and notes, and create notes on opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and agents use this skill to retrieve Lever postings, opportunities, and notes, and to add notes to opportunities through a connected Lever account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and introduce broader agent changes without clear approval.

Mitigation: Review the CLI installation separately, approve a specific verified release, and use OO_SKILLS_SYNC_DISABLED to suppress startup synchronization if desired.

Risk: Creating an opportunity note changes Lever data.

Mitigation: Connect only the intended Lever account and confirm the note-writing payload before execution.

## Reference(s):

- [Lever](https://www.lever.co)
- [Lever API documentation](https://hire.lever.co/developer/documentation)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON action responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields depend on the selected Lever action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
