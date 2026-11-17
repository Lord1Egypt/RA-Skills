## Description:

说人话 rewrites AI-generated Chinese drafts into natural, platform-specific copy for Xiaohongshu, Douyin, WeChat public accounts, and Weibo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social-media operators use this skill to research recent topic context, choose a publishing platform and writing perspective, and produce natural Chinese posts or scripts. It is intended for adapting AI-generated drafts into a more conversational human style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains and reuses a persistent writing-style profile without clear consent or deletion controls.

Mitigation: Require explicit approval before storing preferences, keep only structured writing preferences, and provide inspect and delete controls for the profile.

Risk: Confidential drafts or user-specific writing habits could be retained in the persistent style profile.

Mitigation: Avoid using the skill on confidential drafts unless the memory behavior is changed to minimize retained content and require user approval.

Risk: The skill uses web searches for topic background, which can introduce stale or unreliable context into generated posts.

Mitigation: Review searched background and citations before publication, especially for timely, factual, or sensitive topics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pengpengliu1212-art/skills/humanize-write)
- [Publisher profile](https://clawhub.ai/user/pengpengliu1212-art)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown-formatted Chinese copy with brief background notes and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a persistent writing-style profile when the user revises generated copy.]

## Skill Version(s):

1.2.0 (source: server release evidence and artifact body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
