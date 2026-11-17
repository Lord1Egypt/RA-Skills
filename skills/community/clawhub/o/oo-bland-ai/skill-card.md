## Description:

Bland AI (bland.ai). Use this skill for ANY Bland AI request — searching and reading data. Whenever a task involves Bland AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to read information from a connected Bland AI account, including account status, call details and transcripts, and available voices. Developers can use it to run these account and call lookups through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI can change other agents’ installed skills without this skill explaining those changes.

Mitigation: Review the CLI’s broader installation effects and prefer a verified release with explicit approval. If cross-agent skill changes are unwanted, configure OO_SKILLS_SYNC_DISABLED=1 before CLI use after checking version support.

Risk: Remote installer bytes and the exact installed release were not verified.

Mitigation: Review the CLI’s broader installation effects before proceeding and prefer a verified release.

## Reference(s):

- [Bland AI](https://www.bland.ai/)
- [Bland AI API documentation](https://docs.bland.ai/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON]

**Output Format:** [oo CLI commands and JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account, call, transcript, and voice data; available fields depend on the selected action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
