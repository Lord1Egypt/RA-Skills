## Description:

Automated Hinge dating profile liker using Android emulator + Gemini vision AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattttman](https://clawhub.ai/user/mattttman)

### License/Terms of Use:


## Use Case:

External users use this skill to configure and run Hinge automation on an Android emulator, review dating profiles with Gemini vision, send selected likes or comments, and receive a session report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates dating-app likes and comments, which can create unintended interactions if run without supervision.

Mitigation: Require explicit user confirmation before any run that sends likes or comments, use a dedicated emulator account, and keep conservative per-session limits.

Risk: Profile screenshots, generated summaries, logs, and optional recordings may contain sensitive personal data and may be sent to Google Gemini.

Mitigation: Tell the user what data is processed, avoid saving recordings unless needed, minimize log retention, and delete screenshots and session artifacts after review.

Risk: The artifact documentation suggests hardcoding a Gemini API key for scheduled runs.

Mitigation: Use environment injection or a secret manager for scheduled execution and do not hardcode API keys in cron payloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mattttman/skills/hinge-liker)
- [Google Gemini API endpoint used by the skill](https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Console session report, JSON logs, and Markdown setup instructions with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local screenshots, logs, and optional video recordings during a run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
