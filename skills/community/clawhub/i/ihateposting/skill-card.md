## Description:

iHatePosting helps schedule and manage social media and chat posts across 15 platforms, upload media, and review analytics from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayankkasavala](https://clawhub.ai/user/mayankkasavala)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media teams use the skill to discover connected channels, follow channel rules, prepare and schedule posts, manage post status, and review analytics from a command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A mistaken schedule or deletion can affect social content on connected channels.

Mitigation: Review the selected channels, post settings, and status; use drafts while checking content and confirm the target before deleting.

Risk: The skill uses API key or saved sign-in credentials to access connected accounts.

Mitigation: Keep keys and saved credentials private, store them securely, and verify authentication before using other commands.

Risk: The security scan was partial because local references were missing, leaving some evidence incomplete.

Mitigation: Review the current CLI and linked reference documentation before installation and use.

## Reference(s):

- [iHatePosting agent guide](https://ihateposting.com/ai-agents)
- [iHatePosting Agent CLI package](https://www.npmjs.com/package/ihateposting-agent)
- [iHatePosting Agent repository](https://github.com/iHatePostingOrg/iHatePosting-Agent)
- [Provider settings guide](https://github.com/iHatePostingOrg/iHatePosting-Agent/blob/main/PROVIDER_SETTINGS.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and settings vary by connected platform; review channel rules and required settings before scheduling.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
