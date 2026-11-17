## Description:

Display file contents in hexadecimal and ASCII format. Use for binary file analysis, forensic examination, and low-level data inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and analysts use this skill to inspect local file bytes, stdin data, and string or hex conversions during binary analysis, forensic review, and low-level troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The utility reads files or stdin selected by the user and can load large inputs into memory.

Mitigation: Use it only on intended local files or streams, prefer the length option for large data, and avoid very large or untrusted streams until incremental processing is added.

Risk: Encode and decode conversion options are present but lightly under-described in the public description.

Mitigation: Review command arguments before use and update the skill description to document conversion behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/hexdump-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local files or stdin selected by the user; output length depends on input size and the length option.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
