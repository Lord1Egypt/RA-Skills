## Description:

InfoDashboard guides agents through cloning, configuring, starting, and using OpenClaw's InfoDashboard service to generate Streamlit dashboards from natural-language requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyxapple98](https://clawhub.ai/user/zyxapple98)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to set up InfoDashboard, configure LLM and SQL Server access, verify the service, and submit dashboard-generation requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path runs unpinned remote InfoDashboard code, Docker workloads, and a bundled frpc tunnel binary.

Mitigation: Pin and review a specific commit, verify frpc provenance or checksums, and run the service in a constrained environment.

Risk: The service depends on LLM provider keys and SQL Server credentials configured in .env.local.

Mitigation: Keep secrets out of chat, edit .env.local locally, and use a least-privilege database account.

Risk: Generated dashboards and the local service could expose sensitive data if made publicly reachable without protection.

Mitigation: Avoid public exposure unless access controls are in place and limit network access to trusted users.

## Reference(s):

- [InfoDashboard ClawHub Skill Page](https://clawhub.ai/zyxapple98/skills/infodashboard)
- [Clone Or Reuse Existing Repo](references/clone.md)
- [Configure Environment](references/config.md)
- [Start And Verify](references/startup.md)
- [Generate Flow](references/generate-flow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, environment variable examples, and API request and response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires per-step user confirmation before state-changing actions and keeps secrets out of chat.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
