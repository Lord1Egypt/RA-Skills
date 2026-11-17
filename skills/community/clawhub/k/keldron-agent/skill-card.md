## Description:

GPU monitoring with risk intelligence. Local + cloud fleet monitoring, health tracking, proactive alerts, and AI-powered fleet analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horne-ra](https://clawhub.ai/user/horne-ra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, infrastructure operators, and GPU users use this skill to set up or query Keldron Agent, inspect local GPU telemetry and risk scores, connect Keldron Cloud, and monitor fleet history, alerts, and dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can download mutable release binaries or run a mutable container tag.

Mitigation: Prefer pinned releases or verified checksums before installing or starting the agent.

Risk: Docker examples can expose monitoring ports beyond localhost when bound broadly.

Mitigation: Bind exposed ports to 127.0.0.1 unless LAN access is intentionally required.

Risk: Cloud API keys may be persisted or sent to a custom endpoint.

Mitigation: Prefer CLI login or environment variables over plaintext YAML, mask keys in transcripts, and confirm any custom cloud endpoint before use.

Risk: A restart policy can make the monitoring container persistent.

Mitigation: Use Docker restart policies only when a persistent service is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horne-ra/skills/keldron-agent)
- [Keldron Agent GitHub repository](https://github.com/keldron-ai/keldron-agent)
- [Keldron Agent releases](https://github.com/keldron-ai/keldron-agent/releases)
- [Keldron Cloud application](https://app.keldron.ai)
- [Docker Linux post-installation guide](https://docs.docker.com/engine/install/linux-postinstall/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, jq filters, URLs, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose localhost and Keldron Cloud API calls when credentials and endpoints are configured.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
