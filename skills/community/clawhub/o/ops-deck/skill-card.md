## Description:

Ops Deck provides a self-hosted operational dashboard for AI agent setups, including cron visibility, agent intel, security posture, infrastructure mapping, code search, prompt management, and backlog tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, indie developers, small teams, and CS students use this skill to set up a local dashboard that centralizes operational visibility across agent jobs, infrastructure, security status, code search, prompt templates, and project backlog data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network-reachable dashboard or API services without authentication can expose sensitive local operations data.

Mitigation: Bind services to 127.0.0.1 unless authentication, restricted CORS, firewall rules, and a hardened production frontend are configured.

Risk: Operational JSON files may contain secrets, raw cron payloads, private keys, or internal topology that should not be exposed.

Mitigation: Keep secrets and unnecessary internal details out of JSON data files before serving them through the dashboard.

Risk: PM2 boot persistence can keep services running after installation and increase exposure if access controls are incomplete.

Mitigation: Treat PM2 startup persistence as an opt-in production step after access controls and network restrictions are in place.

## Reference(s):

- [Ops Deck ClawHub Page](https://clawhub.ai/solomonneas/skills/ops-deck)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, JavaScript, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup guidance for local dashboard services and JSON-backed operational data; the skill itself does not execute system commands.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
