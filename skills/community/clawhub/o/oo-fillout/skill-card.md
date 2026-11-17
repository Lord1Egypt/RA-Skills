## Description:

Use this skill to read, create, update, and delete Fillout data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to manage Fillout forms and submissions through an authenticated OOMOL-connected account, with confirmation before creating or deleting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructions run a remote CLI installer whose safety has not been established by this review.

Mitigation: Review and verify the CLI installer separately before allowing setup to run, including any bundled skills it installs.

Risk: Creating or deleting submissions changes Fillout data.

Mitigation: Confirm the exact payload and effect before writes, and confirm the target before destructive actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Fillout REST API documentation](https://www.fillout.com/help/fillout-rest-api)
- [Fillout](https://www.fillout.com/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON payloads, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
