## Description:

Interact with the Jules CLI to manage asynchronous coding sessions for complex, isolated coding tasks that benefit from a remote VM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajstafford](https://clawhub.ai/user/ajstafford)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to assign, monitor, and integrate Jules CLI asynchronous coding sessions for larger or more exploratory repository work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task text passed through documented shell commands can accidentally execute local shell syntax when the text is untrusted or unsanitized.

Mitigation: Validate and quote inputs, avoid shell processing for task text when possible, or pass the task through a file or stdin mechanism supported by the CLI.

Risk: Applying completed remote work can modify the local codebase.

Mitigation: Require explicit user approval before applying remote changes and inspect the proposed changes before integration.

## Reference(s):

- [Jules CLI Usage Reference](references/usage.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the jules and python3 binaries, and may require HOME for Jules credentials.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
