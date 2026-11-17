## Description:

Automates short-video publishing to Douyin, WeChat Channels, Kuaishou, Xiaohongshu, and Bilibili through Playwright-driven local Chrome sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kay1003](https://clawhub.ai/user/kay1003)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and automation-focused agents use this skill to prepare local video files and publish them to supported Chinese video platforms after account login. It is intended for workflows where the user has reviewed the video, title, tags, target platform, and account before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish videos to public creator accounts.

Mitigation: Review every video, title, tag, target platform, and account before running publish commands; avoid the all-platform trigger unless intentionally publishing everywhere.

Risk: Reusable platform login sessions are persisted in the cookies directory with weak scoping and protection.

Mitigation: Keep the cookies directory private, exclude it from backups and commits, and refresh or revoke account sessions if the workspace may have been exposed.

Risk: The setup flow installs dependencies and accepts a local Chrome path.

Mitigation: Run setup without elevated privileges and provide only a trusted Chrome executable path.

## Reference(s):

- [Platform support notes](references/platforms.md)
- [ClawHub skill page](https://clawhub.ai/kay1003/skills/kay-video-upload)
- [social-auto-upload](https://github.com/dreammis/social-auto-upload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cause browser automation to log in, reuse saved sessions, and publish videos through local scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
