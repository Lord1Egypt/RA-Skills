## Description:

Helps agents draft, validate, schedule, and review social media posts across ten networks using the PostQuest API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aleksandrsamokhin](https://clawhub.ai/user/aleksandrsamokhin)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to prepare and validate social posts, manage posting calendars, and read analytics through PostQuest. Scheduling, publishing, and deletion require explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent with the PostQuest API key can access and change social media content.

Mitigation: Install only if you trust PostQuest and intend to authorize the agent; keep the API key out of URLs, files, and replies.

Risk: Scheduling, publishing, or deleting a post can have public or destructive consequences.

Mitigation: Review the final captions, target accounts, and time with timezone; require explicit confirmation for each action.

Risk: Uploading local media sends those files to PostQuest.

Mitigation: Upload local media only when the user is comfortable sharing the files with PostQuest.

## Reference(s):

- [PostQuest OpenAPI specification](https://api.post-quest.com/openapi.yaml)
- [PostQuest website](https://post-quest.com)
- [PostQuest ClawHub listing](https://clawhub.ai/aleksandrsamokhin/skills/postquest-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PostQuest API key and curl; public and destructive actions require user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
