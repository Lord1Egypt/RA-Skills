## Description:

Searches files on a NAS via rclone and Tailscale and helps deliver confirmed files through supported messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tecfancy](https://clawhub.ai/user/tecfancy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and operators use this skill to search trusted NAS shares for requested files, confirm the correct match, and deliver permitted files through supported messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad NAS file access could expose or mishandle private files.

Mitigation: Use only trusted NAS shares and messaging channels, limit searches to the user's requested scope, and require explicit confirmation of each file before transfer.

Risk: Temporary HTTP links can expose sensitive files if used outside a trusted private network or left running.

Mitigation: Avoid the HTTP fallback for sensitive files, bind it only to the Tailscale address, use short-lived links, and stop the server after delivery or timeout.

Risk: Downloaded files may remain in local temporary storage after success or failure.

Mitigation: Use per-request private temporary directories where possible and verify cleanup after every operation.

Risk: Unvalidated path or rclone arguments could retrieve unintended files.

Mitigation: Validate rclone arguments, show the resolved file name, size, and path to the user, and proceed only after confirmation.

## Reference(s):

- [rclone operation reference](references/rclone-ops.md)
- [Channel native file sending reference](references/channel-file-send.md)
- [HTTP temporary download link procedure](references/http-temp-link.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, file-selection prompts, MEDIA lines, and temporary link instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before transfer and cleanup of temporary files after each operation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
