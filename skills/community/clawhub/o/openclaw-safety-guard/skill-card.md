## Description:

Openclaw Safety Guard monitors OpenClaw workspaces across security, memory, heartbeat, cron, shared files, communications, and code-standard checks, then produces health scores, local dashboard files, JSON logs, and Feishu private-message reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonzhangshuo](https://clawhub.ai/user/jasonzhangshuo)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to run scheduled or manual health checks, review local dashboards and JSON reports, and receive Feishu summaries for workspace maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can install frontend dependencies, write configuration, register a persistent cron scan, and run an immediate scan.

Mitigation: Install only in an intended OpenClaw workspace, review setup behavior first, and run setup only where cron persistence and the first automatic scan are acceptable.

Risk: The skill scans private local OpenClaw data and writes persistent JSON and HTML reports.

Mitigation: Avoid scanning repositories or memory files that may contain secrets until report redaction and dashboard escaping are fixed; review generated reports before sharing them.

Risk: Feishu notifications and optional Drive upload use bot credentials and can transmit report information outside the local machine.

Mitigation: Use a dedicated least-privilege Feishu bot, keep Feishu Drive upload disabled unless explicitly needed, and confirm the notification recipient before enabling scheduled runs.

## Reference(s):

- [Openclaw Safety Guard on ClawHub](https://clawhub.ai/jasonzhangshuo/skills/openclaw-safety-guard)
- [Publisher profile](https://clawhub.ai/user/jasonzhangshuo)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type})
- [Feishu bot info API](https://open.feishu.cn/open-apis/bot/v3/info)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, generated JSON reports, local HTML dashboard files, and Feishu text notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local report artifacts under data/, registers a weekday cron scan when setup succeeds, and may send Feishu notifications when credentials and recipient configuration are present.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
