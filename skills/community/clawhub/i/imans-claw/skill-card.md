## Description:

Imans Claw helps OpenClaw agents use the Imans CLI to query Imans workspace, catalog, product variant, sales order, order item, and classification data as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imans-ai](https://clawhub.ai/user/imans-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to connect agents to Imans business data through the Imans CLI. It supports targeted queries for workspace, product, variant, sales order, order item, and classification information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions include a remote installer command that executes mutable code directly in a shell.

Mitigation: Prefer the Homebrew or GitHub release installation path, and independently trust and verify any installer before use.

Risk: Imans queries can expose business-sensitive order or customer data during broad exports.

Mitigation: Use least-privilege Imans profiles, run the narrowest query that answers the request, and confirm before broad exports of order or customer data.

Risk: Authentication material can leak through chat or shell history if tokens are handled directly.

Mitigation: Use token environment variables or stdin for automation, and never request or print raw API tokens in chat.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imans-ai/skills/imans-claw)
- [Imans CLI Homepage](https://github.com/imans-ai/imans-cli)
- [Imans CLI Releases](https://github.com/imans-ai/imans-cli/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should use narrow filters, summarize parsed JSON, and avoid exposing raw tokens or broad customer/order exports without confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
