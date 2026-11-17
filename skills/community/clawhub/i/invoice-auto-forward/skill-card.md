## Description:

Scans supported email accounts for invoice messages, extracts PDF, OFD, or XML invoices, and forwards them according to configurable rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

Employees and operations teams can configure invoice emails to be scanned, filtered, and forwarded to finance or other recipients. Developers can also use the setup, check, scan, run, and parse commands to configure and operate the workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email-controlled links can reach internal services.

Mitigation: Disable link fetching when it is unnecessary; otherwise restrict link_domains to trusted invoice providers and keep link timeouts and size limits enabled.

Risk: Oversized or malicious archive-based invoice files can consume excessive resources.

Mitigation: Keep download size limits enabled and accept only expected invoice formats; review unusual OFD files before processing.

Risk: Email authorization codes may be exposed during setup or operation.

Mitigation: Store codes in the permission-restricted secrets file and do not print them in chat or logs.

## Reference(s):

- [ClawHub release](https://clawhub.ai/songhonglei/skills/invoice-auto-forward)
- [Configuration example](references/config.example.json)
- [Troubleshooting and security guidance](references/troubleshooting.md)
- [Skill instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure or initiate email scanning and forwarding when the user requests it.]

## Skill Version(s):

1.0.10 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
