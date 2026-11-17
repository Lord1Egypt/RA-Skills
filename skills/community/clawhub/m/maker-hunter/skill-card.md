## Description:

Automatically discovers vibe-coding entrepreneurs across technical communities and helps generate personalized recruiting direct messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinc913](https://clawhub.ai/user/robinc913)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, community builders, and operator-led teams use this skill to find promising AI-assisted indie makers, review profile and posting history, and draft tailored outreach messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cookie or credential sharing could expose user accounts because cookies can act like passwords.

Mitigation: Prefer browser-based login, OAuth, or throwaway accounts; do not paste raw cookies into an agent chat.

Risk: The skill suggests running a global script whose behavior should be reviewed before installation.

Mitigation: Inspect and verify external scripts before running them, especially scripts installed from global paths.

Risk: Plaintext credential storage can expose platform accounts.

Mitigation: Avoid storing platform credentials in plaintext credentials.json and use safer credential storage where possible.

## Reference(s):

- [DM Guide](references/dm-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/robinc913/skills/maker-hunter)
- [Hacker News API](https://hacker-news.firebaseio.com/v0/)
- [Jike Login](https://m.okjike.com/login)
- [X Login](https://x.com/login)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style candidate lists, JSON-like candidate records, personalized direct-message drafts, and setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual outreach copy, profile-review summaries, match scores, source post links, and local memory-file guidance.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
