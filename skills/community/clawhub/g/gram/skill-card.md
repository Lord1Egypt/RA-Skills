## Description:

Instagram CLI for viewing feeds, posts, profiles, and engagement via cookies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arein](https://clawhub.ai/user/arein)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to operate the gram CLI for Instagram feed, post, profile, search, and engagement workflows through an authenticated web session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned third-party npm package with access to Instagram session cookies.

Mitigation: Use only a trusted, pinned, verified package version and review the package before installation.

Risk: Session cookies or browser profile access can expose the user's Instagram account session.

Mitigation: Avoid storing cookies in plaintext configuration, pass credentials only when needed, and use a browser profile dedicated to this workflow where practical.

Risk: Like, comment, save, follow, and unfollow commands perform immediate live account actions.

Mitigation: Review generated commands before execution and require explicit user confirmation for engagement actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arein/skills/gram)
- [gram project homepage](https://github.com/arein/gram)
- [@cyberdrk/gram npm package](https://www.npmjs.com/package/%40cyberdrk%2Fgram)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gram binary and authenticated Instagram session cookies or browser profile access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
