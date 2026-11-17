## Description:

Meta-skill for the Longevity OS bundle that routes natural language health conversations to the right capability: nutrition logging, health profile updates, pattern discovery, experiments, news, or daily coaching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madeyexz](https://clawhub.ai/user/madeyexz)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use Longevity OS to route personal health conversations into meal logging, health profile updates, curated longevity news, self-experiment tracking, and daily coaching workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle asks users or agents to run an unpinned external installer that may change OpenClaw configuration.

Mitigation: Use a pinned commit or signed release, inspect the installer and sub-skills before running them, and verify any changes to ~/.openclaw/openclaw.json.

Risk: The bundle handles sensitive health data and can send automated Telegram messages.

Mitigation: Review what health data may be stored or sent, confirm the Telegram destination chat id, and enable cron or Telegram delivery only after that review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/madeyexz/skills/longevity-os)
- [Artifact README](README.md)
- [Artifact Skill Definition](skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration steps, and structured health workflow summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes natural language health requests to the relevant OpenClaw bundle capability; may summarize local health, nutrition, experiment, and news context when available.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
