## Description:

Search and read Luma calendar, event, guest, and profile data through the connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to search and read calendar, event, guest, and profile information from a connected Luma account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Luma workflow is appropriate, but its setup can execute unverified remote code and introduce additional agent skills without clearly explaining those changes.

Mitigation: Review and approve CLI setup separately, preferably using a vetted release. Check which additional agent skills it installs; the CLI command reference documents OO_SKILLS_SYNC_DISABLED for disabling startup skill synchronization. Connect only the intended Luma account and consider the guest/profile data accessible through OOMOL. The remote installers could not be inspected, so their full system changes remain unverified.

## Reference(s):

- [Luma API documentation](https://docs.luma.com/reference/getting-started-with-your-api)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Luma](https://lu.ma)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-luma)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Luma calendar, event, guest, and profile data scoped to the connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
