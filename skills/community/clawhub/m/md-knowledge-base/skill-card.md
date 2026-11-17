## Description:

Knowledge-Base guides agents through creating, organizing, searching, and maintaining a structured Markdown knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otweihan](https://clawhub.ai/user/otweihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and agent users use this skill to manage notes, project records, source material, daily logs, and knowledge-base health checks in a structured Markdown repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Git workflow can commit and push the entire configured repository, including unrelated or sensitive files.

Mitigation: Require git status and staged diff review, stage only intended paths, and ask for approval before any git push.

Risk: Knowledge-base repositories may contain private drafts, credentials, local configuration, or unrelated files.

Mitigation: Review the skill before installation and use placeholders instead of writing passwords, tokens, API keys, private keys, customer privacy data, or commercial secrets.

## Reference(s):

- [HanSphere Knowledge-Base Reference](references/hansphere.md)
- [ClawHub Skill Page](https://clawhub.ai/otweihan/skills/md-knowledge-base)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with note structures, relative links, file naming rules, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language knowledge-base conventions with repository-specific reference configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
