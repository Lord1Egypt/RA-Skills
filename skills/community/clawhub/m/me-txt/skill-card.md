## Description:

Create, fetch, and validate me.txt personal identity files for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rollsmorr1](https://clawhub.ai/user/rollsmorr1)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create, retrieve, and validate me.txt files that describe personal identity information for AI agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned npx commands that may download and execute mutable third-party code.

Mitigation: Prefer manual me.txt creation and direct HTTPS fetches, or run an exact reviewed CLI version in a restricted environment without unnecessary credentials.

Risk: A me.txt file can publish personal identity, contact, preference, and work information.

Mitigation: Ask the user to approve each included section before publishing and omit sensitive or unnecessary personal details.

## Reference(s):

- [me.txt homepage](https://metxt.org)
- [me.txt specification](https://metxt.org/spec)
- [ClawHub skill listing](https://clawhub.ai/rollsmorr1/skills/me-txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell commands and me.txt file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated me.txt content should be concise and include only sections with user-provided content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
