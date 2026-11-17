## Description:

Find trending topics, create editorial-style social media graphics, and post to X/Twitter and Instagram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashmonmc](https://clawhub.ai/user/ashmonmc)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and social media operators use this skill to research trending topics, draft content workflows, generate editorial-style carousel graphics, and publish posts to Instagram and X/Twitter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live social account credentials and saved sessions.

Mitigation: Use isolated, low-privilege social accounts, rotate credentials after testing, and avoid sharing session files.

Risk: The skill can publish posts to public social platforms.

Mitigation: Require manual preview and confirmation before any generated post, story, reel, or carousel is published.

Risk: The security evidence reports exploitable command-generation patterns.

Mitigation: Avoid untrusted query or action values and review generated shell commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashmonmc/skills/insta-content-engine)
- [Publisher profile](https://clawhub.ai/user/ashmonmc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, prompts, configuration notes, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke external services and social posting tools when configured with the required credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
