## Description:

Track nutrition, meals, water, weight, steps, meditation, journal entries, and coaching workflows through the Habit AI REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[habitclaw](https://clawhub.ai/user/habitclaw)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to log and retrieve personal health data in Habit AI, including meals, water, weight, steps, meditation, and journal entries. Agents can also prepare nutrition estimates, structured meal payloads, and coaching requests for the Habit AI API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive health, journal, profile, and food photo data to the Habit AI cloud service.

Mitigation: Use it only for intended Habit AI cloud workflows, avoid sharing unnecessary sensitive data, and confirm before uploading images or sending journal and profile details.

Risk: The Habit AI API key authorizes access to the user's Habit AI account.

Mitigation: Store HABITAI_API_KEY securely, do not paste it into chat transcripts or shared files, and revoke keys that may have been exposed.

Risk: The skill documents endpoints that delete records, update profile data, upload images, and manage API keys.

Mitigation: Require explicit user confirmation before destructive actions, profile changes, image uploads, or API key management.

## Reference(s):

- [Habit AI API Reference](references/api.md)
- [Habit AI](https://habitapp.ai)
- [Habit AI REST API](https://habitapp.ai/api/v1)
- [Habit AI Skill on ClawHub](https://clawhub.ai/habitclaw/skills/habit-ai)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with JSON payload examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses HABITAI_API_KEY for authenticated Habit AI API requests.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
