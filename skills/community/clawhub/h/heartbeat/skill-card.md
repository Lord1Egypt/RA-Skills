## Description: <br>
Design better OpenClaw HEARTBEAT.md files with adaptive cadence, safe checks, and cron handoffs for precise schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to design HEARTBEAT.md behavior for adaptive monitoring, proactive check-ins, and cron handoffs for exact-time tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated heartbeat or cron guidance could create unwanted proactive checks, noisy alerts, or schedule changes if enabled without review. <br>
Mitigation: Manually confirm generated cron and heartbeat changes before enabling them, and use the included QA checklist, cooldown rules, quiet hours, and rollback snapshot guidance. <br>
Risk: Heartbeat preferences, drafts, and snapshots stored under ~/heartbeat/ could expose sensitive workflow details if secrets are added there. <br>
Mitigation: Avoid storing secrets in ~/heartbeat/ and keep heartbeat memory limited to cadence preferences, scope, and tuning decisions. <br>
Risk: Ungated paid API or expensive checks could increase cost if added to a heartbeat cycle. <br>
Mitigation: Place expensive checks behind cheap prechecks and require explicit user acceptance before paid APIs run on heartbeat cycles. <br>


## Reference(s): <br>
- [Heartbeat on ClawHub](https://clawhub.ai/ivangdavila/heartbeat) <br>
- [Heartbeat homepage](https://clawic.com/skills/heartbeat) <br>
- [OpenClaw Docs - Heartbeats](https://docs.openclaw.ai/advanced/heartbeats) <br>
- [OpenClaw Docs - Cron vs Heartbeat](https://docs.openclaw.ai/advanced/cron-vs-heartbeat) <br>
- [OpenClaw CLI System Skill](https://docs.openclaw.ai/openclaw-cli/system-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration instructions, Shell commands, Guidance] <br>
**Output Format:** [Markdown with heartbeat templates, checklists, and inline configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local files under ~/heartbeat/ and cron handoff guidance for user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
