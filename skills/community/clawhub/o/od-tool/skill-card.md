## Description:

Dump file contents in octal, decimal, hexadecimal, and ASCII formats. Use for binary data inspection and low-level file analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local file bytes while debugging binary data, file encodings, or low-level content issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may print the contents of sensitive local files into the agent session.

Mitigation: Use it only on files whose contents are intended to be inspected and shared in the session.

Risk: The documentation advertises hexadecimal, decimal, ASCII, and address-base options that scanner evidence says are not implemented.

Mitigation: Rely on the skill only for octal byte dumps unless the publisher updates the implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/od-tool)
- [ClawHub publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file byte dumps; scanner evidence notes the implementation emits octal output and does not support all advertised format flags.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
