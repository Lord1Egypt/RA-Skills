## Description: <br>
AI Agent Observability & Debug Console - flight recorder and debug console for autonomous AI systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noeldelisle](https://clawhub.ai/user/noeldelisle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use LobsterOps to instrument AI agents, record structured activity, inspect traces, analyze behavior patterns, configure alerts, and export logs for debugging or auditing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LobsterOps logs can contain private prompts, internal reasoning, tool arguments, tool results, credentials, customer data, and errors. <br>
Mitigation: Treat logs as sensitive data, restrict access to log files or Supabase tables, and avoid broad Supabase service-role keys unless the deployment is locked down. <br>
Risk: PII or secrets can remain in logs if filtering is disabled, misconfigured, or not tested against expected data. <br>
Mitigation: Enable and test PII filtering for the deployed agent, use short retention periods, and prefer local or memory storage for sensitive work. <br>
Risk: Cloud storage can expand the exposure of agent traces beyond the local machine. <br>
Mitigation: Use local or memory storage for sensitive work and configure Supabase only when access controls, table permissions, and credential handling are appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noeldelisle/lobsterops) <br>
- [Publisher profile](https://clawhub.ai/user/noeldelisle) <br>
- [Project homepage from metadata](https://github.com/noeldelisle/LobsterOps) <br>
- [LobsterOps site](https://lobsterops.dev) <br>
- [npm package](https://www.npmjs.com/package/lobsterops) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, CSV] <br>
**Output Format:** [Markdown guidance with JavaScript and JSON configuration examples; runtime exports can be JSON, CSV, or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces observability records, debug traces, analytics summaries, alerts, and exportable agent logs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter and package.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
