## Description:

Use Agify to estimate ages from full or first names, optionally scoped by country.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request Agify age estimates for a full or first name, optionally by country. It also supports batch predictions for up to 100 names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security assessment is suspicious: it flags a high-risk remote install command and behavior that does not match the skill's stated Agify purpose.

Mitigation: Consider not installing until the remote installer and login steps are explained and independently verified; the scan was partial and does not establish that all behavior is safe.

Risk: Name-prediction requests may transmit names and optional country information to external services.

Mitigation: Consider the external data transmission before sending names or country information.

## Reference(s):

- [Agify API documentation](https://agify.io/documentation/api/reference)
- [Agify](https://agify.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell commands; connector results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-name and batch predictions of up to 100 names; each name consumes quota.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
