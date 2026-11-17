## Description:

AI-powered palm reading and analysis from palm images. Supports English, Tamil, Telugu, Kannada, and Hindi. Use when a user wants a palm reading, palmistry analysis, hand line interpretation, fortune reading from palm, or wants to know about their heart line, head line, life line, or fate line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to request palmistry-style readings from user-provided palm images in English, Tamil, Telugu, Kannada, or Hindi. The skill calls the ToolWeb API and returns line-by-line palm reading sections plus an overall interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends users' palm photos and related request metadata to a third-party paid API.

Mitigation: Add a clear notice and affirmative consent step before API submission, and verify ToolWeb privacy, retention, deletion, and secondary-use terms before using the skill with real users.

Risk: Successful API calls are tracked for billing and may affect the user's subscription quota or costs.

Mitigation: Confirm API key ownership and expected cost or quota impact before enabling the skill in production.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/palmistry-ai-palm-reader)
- [ToolWeb Portal](https://portal.toolweb.in)
- [ToolWeb Palmistry API Endpoint](https://portal.toolweb.in/apis/lifestyle/palmistry)
- [ToolWeb Platform](https://toolweb.in)
- [ToolWeb OpenClaw Skills](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown palm reading response with curl-based API call guidance and optional downloadable HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY, curl, and a user-provided palm image; successful API calls may consume paid quota.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
