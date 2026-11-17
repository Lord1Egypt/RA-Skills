## Description:

Publish ONE skill to ALL agent-skill channels from a single source of truth: the ClawHub skill registry, a ClawHub bundle-plugin package, and a Claude Code plugin marketplace (plain GitHub repo).

This skill is ready for commercial/non-commercial use.

## Publisher:

[readysoon](https://clawhub.ai/user/readysoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to publish, release, rename, or version-bump a single skill across ClawHub skill registry, ClawHub bundle-plugin package, and Claude Code plugin marketplace channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public release commands can accidentally include secrets or unintended local files before a GitHub push.

Mitigation: Run git status --short, inspect the staged diff, confirm .gitignore covers secrets and local files, and prefer explicit git add paths before committing or pushing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/readysoon/skills/multi-channel-skill-publisher)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
