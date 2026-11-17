## Description:

MeetGeek (meetgeek.ai). Use this skill for ANY MeetGeek request — searching and reading data. Whenever a task involves MeetGeek, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected MeetGeek account can list meetings and retrieve meeting details, summaries, insights, highlights, and transcript data through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may execute remote installers without clear user control, and OOMOL handles sensitive meeting data as an intermediary.

Mitigation: Install a reviewed, version-pinned oo CLI yourself and check its changes to other agent skills before connecting an account; account for OOMOL's intermediary role when handling sensitive meeting data.

## Reference(s):

- [MeetGeek](https://meetgeek.ai)
- [MeetGeek API documentation](https://docs.meetgeek.ai/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses with shell command examples and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Meeting lists and transcripts may be paginated; inspect the action schema before sending a payload.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
