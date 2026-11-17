## Description:

X/Twitter CLI and SDK for reading, searching, posting, and engagement via cookie auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeroptis](https://clawhub.ai/user/zeroptis)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate the hume-x CLI for X/Twitter account reading, search, posting, engagement, social graph, list, trending, notification, bookmark, like, and scheduled tweet workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and invokes an unaudited global npm package that can receive account credentials.

Mitigation: Review the package before installation and prefer a pinned or otherwise verified package version before providing credentials.

Risk: Cookie authentication and browser-cookie access can expose active X/Twitter sessions.

Mitigation: Use a dedicated or low-risk X account when possible, avoid passing tokens on the command line, and do not allow browser-cookie access unless explicitly approved.

Risk: The CLI can perform live account actions such as posting, deleting, liking, following, muting, blocking, and scheduling tweets.

Mitigation: Review proposed commands before execution and confirm the target account, tweet IDs, media, and action type before running mutating commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON]

**Output Format:** [Markdown with inline bash code blocks and optional plain text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform live account actions through cookie-authenticated CLI commands; JSON output is available with --json and raw API JSON with --json-full.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
