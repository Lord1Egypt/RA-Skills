## Description:

Collects Gitea repository commit activity, asks an AI agent to summarize progress and risks, renders HTML progress reports, and sends them by email to repository administrators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhcolin0313](https://clawhub.ai/user/zhcolin0313)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team leads use this skill to generate routine progress reports from visible Gitea repositories over a default or specified time window and email repository administrators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Gitea personal access token and private repository activity.

Mitigation: Install with a narrowly scoped read-only Gitea token and restrict permissions on ~/.config/gitea-routine-report/.env.

Risk: Reports are sent by email to repository administrator addresses, which can expose repository activity to unintended recipients if configuration or defaults are wrong.

Mitigation: Verify the configured Gitea URL and review recipients before sending reports.

Risk: Repository content and AI-generated summaries may be unsafe or misleading in HTML reports.

Mitigation: Treat repository content and summaries as untrusted until HTML escaping, safer temporary files, and stronger confirmation boundaries are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhcolin0313/skills/gitea-routine-report)
- [Publisher profile](https://clawhub.ai/user/zhcolin0313)

## Skill Output:

**Output Type(s):** [text, JSON, HTML, shell commands, configuration, guidance]

**Output Format:** [Structured JSON from reporting scripts, AI-generated JSON summaries, and HTML email bodies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITEA_URL and a narrowly scoped GITEA_TOKEN; can target all visible repositories or a specific owner/repo and time window.]

## Skill Version(s):

1.2.2 (source: skill.yaml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
