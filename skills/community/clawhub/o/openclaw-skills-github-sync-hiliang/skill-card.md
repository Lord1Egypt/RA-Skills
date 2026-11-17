## Description:

OpenClaw Skills GitHub Sync helps users manually synchronize OpenClaw skill repositories to GitHub after creating or modifying skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hi-jiajun](https://clawhub.ai/user/hi-jiajun)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure local private and public skill repositories, review pending changes, and push selected repository updates to GitHub after manual confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync script can commit and push broad local repository contents from configured skill repositories.

Mitigation: Run git status and git diff before syncing, verify repository visibility, and confirm that .gitignore excludes credentials, .env files, tokens, keys, logs, and other sensitive files.

Risk: The generated scripts/config.sh file stores local repository paths and is sourced by the sync script.

Mitigation: Treat scripts/config.sh as security-sensitive configuration and review it before running synchronization commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hi-jiajun/skills/openclaw-skills-github-sync-hiliang)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides local setup and sync workflows; scripts may create configuration files, update .gitignore, commit repository changes, and push to GitHub after confirmation.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
