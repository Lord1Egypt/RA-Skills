## Description:

Installs, upgrades, and registers the jun-invest-option-master-agent isolated OpenClaw investment workspace with automated backup and versioning to ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gm4leejun-stack](https://clawhub.ai/user/gm4leejun-stack)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to install and maintain an isolated investment research agent workspace. The workspace assembles data-backed options and portfolio approval packets for human review rather than placing trades automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent publishing automation can upload local workspace contents to ClawHub without a clear per-release review step.

Mitigation: Review or disable the launchd publishing job, require manual approval before publishing, and replace broad workspace sync with an allowlist.

Risk: Personal files, credentials, or infrastructure details may enter publishable artifacts if they are stored in the workspace.

Mitigation: Keep credentials in environment variables or local-only configuration, remove personal files before release, and scan artifacts before publishing.

Risk: Investment recommendations may be wrong or incomplete when market data, broker permissions, or fallback data sources are unavailable.

Mitigation: Require source timestamps and data-quality notes, run the policy and contract validator, and keep all trade execution subject to explicit human approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gm4leejun-stack/skills/jun-invest-option-master-agent)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [Futu OpenAPI introduction](https://openapi.futunn.com/futu-api-doc/intro/intro.html)
- [Investment agent overview](artifact/docs/INVESTMENT_AGENT.md)
- [Invest agent team README](artifact/agent/invest_agent/README.md)
- [Futu integration notes](artifact/agent/invest_agent/integrations/FUTU.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command snippets, workspace files, JSON validation reports, and approval-packet Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Investment outputs are advisory and require human approval before any trading action.]

## Skill Version(s):

0.2.202603041248 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
