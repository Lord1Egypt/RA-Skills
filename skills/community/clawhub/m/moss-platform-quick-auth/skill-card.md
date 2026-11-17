## Description:

B-only Quick Auth for Moss platform using only api-login and api-register, with no email code flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloeveryworlds](https://clawhub.ai/user/helloeveryworlds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to perform Moss platform quick authentication with the B-only api-login/api-register flow, including endpoint selection, status reporting, and credential handling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Moss authentication outputs such as access tokens, refresh tokens, API keys, and temporary passwords.

Mitigation: Verify the host before running authentication requests and redact credential values in chat unless raw values are explicitly required.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Credential values are redacted by default unless the user explicitly requests raw values.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
