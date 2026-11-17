## Description:

Jiminny (jiminny.com). Use this skill for ANY Jiminny request — searching and reading data. Whenever a task involves Jiminny, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to search and read activities, transcripts, summaries, scorecards, coaching feedback, and organization data in Jiminny through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup executes remote code without clearly obtaining approval for local changes.

Mitigation: Install and approve the CLI separately before enabling the skill, and review its bundled-skill synchronization settings.

Risk: The remote installers and hosted connector are outside the submitted artifact, so their exact behavior is unverified.

Mitigation: Review the setup and connector before relying on them, and use a suitably scoped Jiminny connection.

## Reference(s):

- [Jiminny](https://jiminny.com)
- [Jiminny Customer API Documentation](https://jiminny.github.io/customer-api-docs/)
- [Jiminny ClawHub skill page](https://clawhub.ai/oomol/skills/oo-jiminny)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON results and Markdown usage guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented Jiminny data; available results depend on the selected action and its input schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
