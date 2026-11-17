## Description:

Scenario-focused Sparki skill for highlight extraction while using official Sparki setup, API-key, and upload workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to direct an agent to extract the strongest moments from sports, event, speech, recap, or similar footage and produce a concise highlight reel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, and project metadata may be sent to the configured Sparki service.

Mitigation: Install and use the skill only for videos and prompts that may be processed by Sparki; review the configured endpoint before upload.

Risk: API keys and endpoint settings can be persisted in the local OpenClaw config directory.

Mitigation: Prefer SPARKI_API_KEY for session-scoped credentials, avoid untrusted --base-url values, and remove ~/.openclaw/config/sparki.json when stored credentials are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/highlight-reels)
- [Sparki homepage](https://sparki.io)
- [Sparki Telegram upload link](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can upload mp4 or mov inputs to Sparki, poll for processing, and download MP4 results.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter, _meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
