## Description:

openFDA (open.fda.gov). Use this skill for ANY openFDA request — searching and reading data. Whenever a task involves openFDA, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search openFDA drug records and count common field values through an OOMOL-connected account. Results are informational and are not medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup instructions direct the agent to run an online installer that was not verified.

Mitigation: Review and approve CLI installation separately before allowing setup; review the installer and its source first.

Risk: Queries pass through OOMOL, and account credentials and billing may be involved.

Mitigation: Review the connected account and billing implications before use, and follow the stated connection and authentication guidance.

Risk: Drug record search results could be mistaken for medical advice.

Mitigation: Treat results as informational and do not use them as medical advice.

## Reference(s):

- [openFDA](https://open.fda.gov/)
- [openFDA API documentation](https://open.fda.gov/apis/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON action payloads and connector responses, with shell commands and setup guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are informational and must not be used as medical advice.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
