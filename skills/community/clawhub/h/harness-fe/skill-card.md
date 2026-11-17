## Description:

Debug, inspect, and drive frontend apps instrumented with the Harness-FE Vite/Webpack plugin, including live browser state, telemetry, source lookup, and replay workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to diagnose UI bugs in instrumented local or test applications by correlating browser behavior, telemetry, and source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect and retain sensitive frontend telemetry, including browser activity, storage changes, network bodies, recordings, visitor timelines, and attachments.

Mitigation: Use the skill on local or test data, avoid production secrets in recorded sessions, ask before inspecting sensitive artifacts, and clear ~/.harness/ when done.

Risk: Setup instructions run packages through the package registry and may use unpinned package versions.

Mitigation: Pin package versions and review package sources before installation or execution.

Risk: Browser evaluation tools can execute JavaScript in the user's page context.

Mitigation: Do not evaluate untrusted code, especially content copied from console, network, or user-controlled page data.

## Reference(s):

- [Harness-FE Documentation](https://harness-fe.com/)
- [Harness-FE Chinese Documentation](https://harness-fe.com/zh/)
- [Harness-FE Integrations](https://harness-fe.com/integrations/)
- [ClawHub Skill Page](https://clawhub.ai/paul-leo/skills/harness-fe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser inspection results, debugging hypotheses, source references, and proposed frontend changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
