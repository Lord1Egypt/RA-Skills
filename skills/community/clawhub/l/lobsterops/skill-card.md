## Description:

AI Agent Observability & Debug Console - flight recorder and debug console for autonomous AI systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noeldelisle](https://clawhub.ai/user/noeldelisle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use LobsterOps to instrument AI agents, record activity, inspect traces, analyze behavior, configure alerts, and export logs for debugging or audit review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LobsterOps can record sensitive agent prompts, reasoning traces, tool inputs, tool outputs, credentials, customer data, or proprietary context.

Mitigation: Disable reasoning and tool-output capture unless needed, review what is captured before installation, and use storage locations with restrictive access permissions.

Risk: Cloud storage can expose agent logs if Supabase access controls or key handling are not configured correctly.

Mitigation: Prefer local storage for sensitive environments, and use Supabase only with explicit credentials, least-privilege keys, and project access controls.

Risk: The built-in PII filter is not sufficient as a general secret scrubber.

Mitigation: Treat filtering as a convenience layer, keep secrets out of logged fields, and review logs before sharing or exporting them.

Risk: CSV exports may be unsafe to open in spreadsheet software if formula-like values are present.

Mitigation: Neutralize spreadsheet formula prefixes or export to JSON or Markdown when opening logs in spreadsheet tools is not required.

## Reference(s):

- [LobsterOps ClawHub skill page](https://clawhub.ai/noeldelisle/skills/lobsterops)
- [LobsterOps homepage](https://github.com/noeldelisle/LobsterOps)
- [LobsterOps npm package](https://www.npmjs.com/package/lobsterops)
- [LobsterOps dashboard](https://lobsterops.dev/demo)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and JSON configuration snippets; runtime exports can be JSON, CSV, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local or Supabase-backed event logs, trace summaries, analytics, alerts, and exported agent activity records.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
