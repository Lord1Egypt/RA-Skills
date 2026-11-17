## Description:

Scenario-focused Sparki skill for turning long videos into short-form clips while using official Sparki setup, API-key, and upload workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn podcasts, interviews, talks, streams, and other long-form videos into short-form clips, reels, and shorts with stronger hooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, project metadata, and the Sparki API key are sent through the CLI during normal use.

Mitigation: Use the skill only with content suitable for Sparki processing, prefer SPARKI_API_KEY over saved credentials when possible, and review local config file permissions after setup.

Risk: The CLI supports overriding the Sparki API base URL, which can route credentials and video metadata to another endpoint.

Mitigation: Avoid --base-url unless the endpoint is fully trusted and intended for this workflow.

## Reference(s):

- [ClawHub Long to Short skill page](https://clawhub.ai/fischerlam/skills/long-to-short)
- [Sparki homepage](https://sparki.io)
- [Sparki Telegram upload link](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can upload selected local MP4 or MOV files to Sparki, create and poll edit projects, and download rendered MP4 results.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
