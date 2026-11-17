## Description:

Ashby (ashbyhq.com). Use this skill for ANY Ashby request — searching and reading data. Whenever a task involves Ashby, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting and operations teams use this skill to retrieve Ashby candidate and job information, search candidates, and inspect the connected API key information through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code and introduce broader agent changes without clear user control.

Mitigation: Review and explicitly approve CLI installation. Configure OO_SKILLS_SYNC_DISABLED=1 before invoking oo if automatic skill writes are unwanted.

Risk: Candidate information may be accessible through the OOMOL connection.

Mitigation: Limit the Ashby connection to the read permissions needed for the task.

## Reference(s):

- [oo CLI documentation and source](https://github.com/oomol-lab/oo-cli)
- [Ashby](https://www.ashbyhq.com)
- [Ashby API documentation](https://developers.ashbyhq.com/)
- [OOMOL CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific JSON input; results returned as JSON.]

## Skill Version(s):

1.0.4 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
