## Description:

Provides developers with the OKX Onchain OS audit log path, file format, entry fields, and rotation behavior without reading or displaying log contents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to locate and understand OKX Onchain OS audit logs for offline troubleshooting. The skill is limited to explaining the path, JSON Lines structure, header, entry fields, and rotation behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit logs may contain command history, redacted arguments, errors, and timing data.

Mitigation: Share or inspect the audit log deliberately, avoid pasting troubleshooting logs into public channels, and do not read or display the log contents in the conversation.

## Reference(s):

- [OKX Web3](https://web3.okx.com)
- [ClawHub skill page](https://clawhub.ai/ok-james-01/skills/okx-audit-log)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown text with inline file paths and JSON field examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not read or display audit log contents.]

## Skill Version(s):

3.1.3 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
