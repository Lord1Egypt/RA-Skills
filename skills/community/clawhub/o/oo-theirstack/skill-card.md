## Description:

Search and read TheirStack company, job, and technographic data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use the skill to search TheirStack company and job data, inspect technographics, and check the connected team's credit balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded CLI code, and broader changes to other agent skills are unexplained.

Mitigation: Review and install the CLI separately before allowing automated use; consult the command reference about OO_SKILLS_SYNC_DISABLED.

Risk: Queries pass through OOMOL, while remote installers and hosted credential handling have not been verified.

Mitigation: Connect only the intended TheirStack account and review the CLI separately before use.

## Reference(s):

- [TheirStack API documentation](https://theirstack.com/en/docs/api-reference)
- [TheirStack](https://theirstack.com)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON results with shell command examples and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the selected TheirStack action and query.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
