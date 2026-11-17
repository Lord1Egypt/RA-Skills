## Description:

A bird-like LinkedIn CLI for searching profiles, checking messages, and summarizing your feed using session cookies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arun-8687](https://clawhub.ai/user/arun-8687)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to operate a LinkedIn command-line workflow for profile lookup, people search, feed summaries, and recent message checks. It is intended for users who can supply their own active LinkedIn session cookies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires active LinkedIn session cookies that can grant access to the user's LinkedIn account.

Mitigation: Use only in an isolated environment and avoid sharing terminal history, shell profiles, or logs that may contain cookie values.

Risk: The skill passes session cookies to an unpinned third-party package.

Mitigation: Review and pin dependencies before installation, and install only in an environment where account and local system exposure are acceptable.

Risk: Message and feed commands can display private LinkedIn content in the terminal.

Mitigation: Run commands only in trusted terminals and redact output before sharing logs, screenshots, or support bundles.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/arun-8687/skills/linkedin-cli)
- [Publisher profile](https://clawhub.ai/user/arun-8687)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line text output and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, LINKEDIN_LI_AT, LINKEDIN_JSESSIONID, and the linkedin-api Python package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
