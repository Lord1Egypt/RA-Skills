## Description:

Generate secure random passwords and check password strength with configurable length, character types, entropy estimates, and local-only operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alone86136](https://clawhub.ai/user/alone86136)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to ask an agent for local password generation commands or password-strength checking guidance without relying on network services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checking a real password through a command-line argument can expose it locally through shell history or process listings.

Mitigation: Use the checker only with throwaway examples until it is changed to read from a hidden prompt or standard input, and do not pass real passwords on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alone86136/skills/local-password)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated passwords, entropy estimates, and crack-time estimates produced by local Python scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
