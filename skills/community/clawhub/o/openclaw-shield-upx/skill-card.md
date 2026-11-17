## Description:

OpenClaw Shield helps agents check Shield health, inspect security events, manage cases, and explain redacted telemetry from the OpenClaw Shield plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunopradof](https://clawhub.ai/user/brunopradof)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security operators use this skill to monitor OpenClaw agent activity, review Shield status and events, investigate security cases, and guide remediation without exposing raw diagnostic data unnecessarily.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required gateway plugin observes agent activity and sends redacted security telemetry to UPX.

Mitigation: Review the plugin package, permissions, privacy terms, retention and deletion process, subscription terms, and installed version before enabling it.

Risk: Shield logs can contain internal paths, commands, URLs, and other diagnostic details from agent activity.

Mitigation: Summarize findings for users and avoid exposing raw log field values unless the user explicitly requests them for investigation in the current session.

Risk: Uninstalling or deleting Shield data can affect local redaction history and platform subscription state.

Mitigation: Run uninstall and data-deletion commands manually, confirm retention needs first, and deactivate the instance through the UPX dashboard when appropriate.

Risk: Resolving or closing cases changes security case state.

Mitigation: Present case details and get explicit user approval before resolving, closing, or marking a case as a false positive.

## Reference(s):

- [OpenClaw Shield ClawHub listing](https://clawhub.ai/brunopradof/skills/openclaw-shield-upx)
- [OpenClaw Shield package](https://www.npmjs.com/package/@upx-us/shield)
- [UPX OpenClaw Shield page](https://www.upx.com/en/lp/openclaw-shield-upx)
- [UPX Shield dashboard](https://uss.upx.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands and security case summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize status, logs, vault inventory, subscription state, and security cases; raw diagnostic values should be withheld unless explicitly requested by the user.]

## Skill Version(s):

1.4.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
