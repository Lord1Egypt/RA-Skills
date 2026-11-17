## Description:

OpenClaw Control Center generates a local browser dashboard for OpenClaw system status, AI usage metrics, sessions, scheduled tasks, skills, plugins, and security settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinxiao607](https://clawhub.ai/user/qinxiao607)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users, operators, and developers use this skill to generate a local visual control center for routine status checks, AI usage monitoring, session review, cron visibility, plugin review, and security posture inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated local dashboard may reveal OpenClaw session, cron, plugin, gateway, and security metadata.

Mitigation: Keep the generated HTML file local, avoid sharing or syncing it, and review professional-mode output before displaying it publicly.

Risk: The skill requests exec capability, which is broader authority than a status dashboard typically needs.

Mitigation: Review command behavior before deployment and run the skill in an environment where command execution is restricted to the intended OpenClaw status and browser-opening workflow.

Risk: The optional full deployment path uses a remote npm project and dependencies.

Mitigation: Use the static local dashboard for normal operation; if remote deployment is needed, review and pin the repository and dependencies first.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qinxiao607/skills/openclaw-control-center)
- [Dashboard Rules](artifact/references/dashboard-rules.md)
- [Professional Mode](artifact/references/pro-mode.md)
- [Deployment Guide](artifact/references/deployment.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands and generated HTML, CSS, and JavaScript for a local dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a persistent local HTML dashboard at ~/.qclaw/workspace/control-center.html and open it in a browser.]

## Skill Version(s):

1.0.0 (source: server release evidence, metadata.json, changelog released 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
