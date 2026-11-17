## Description:

Generates 12-16 character random passwords with letters, numbers, and symbols, with basic strength information and optional local history output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to generate individual passwords for personal accounts, check basic password strength, and optionally record generated values locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated passwords may be written to local plaintext files.

Mitigation: Disable history or remove local password logging; store credentials in a password manager or OS secret store instead of memory/passwords.md.

Risk: The skill includes broader API, file, command, and security-workflow language than its password-generation purpose requires.

Mitigation: Review and remove unrelated sections before deployment; limit allowed tools and commands to the password generation workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/password-generator-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated password records may be Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates 12-16 character passwords and may write generated passwords to memory/passwords.md if the workflow is followed.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
