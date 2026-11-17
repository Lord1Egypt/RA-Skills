## Description:

Myapp Creator helps an agent create or update standalone single-file HTML apps and documents for Xiaodu users, then register them with fe-service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhang6714268](https://clawhub.ai/user/zhang6714268)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents serving Xiaodu Swan users use this skill to turn short app or document requests into self-contained HTML. The skill supports creating, updating, reading, and installation-checking app records through its configured service tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and transmits a long-lived API token together with user and app data.

Mitigation: Install only in trusted local environments, protect the local token configuration, prefer short-lived or scoped tokens where available, and avoid placing secrets or private content in app prompts.

Risk: A configurable MYAPP_API_BASE can direct generated app content and identifiers to an unintended service.

Mitigation: Use HTTPS and a fixed, approved backend host; confirm the fe-service operator before installing or running the skill.

Risk: Unpinned npx/npm install paths can resolve to a CLI version that has not been separately reviewed.

Mitigation: Prefer a vetted ClawHub CLI version or separately review the resolved CLI package before using unpinned install commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhang6714268/skills/myapp-creator)
- [Publisher profile](https://clawhub.ai/user/zhang6714268)
- [Related Xiaodu control skill card](https://clawhub.ai/dueros-mcp/xiaodu-control-official)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [Markdown guidance with single-file HTML, JSON feature lists, and shell-backed tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML should be self-contained, touch-friendly, no more than 60KB, and compatible with Android 8.1 WebView.]

## Skill Version(s):

1.0.31 (source: server release metadata, artifact metadata.json, clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
