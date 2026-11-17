## Description:

Operate a multi-agent shared knowledge layer backed by one GitHub repository. Use when setting up shared/private knowledge folders, enforcing branch+PR workflow, syncing branches, resolving merge conflicts, and standardizing how agents write/promote knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up and maintain a shared GitHub-backed knowledge layer for private notes, shared knowledge promotion, branch synchronization, and conflict handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync workflow can automatically commit local knowledge-repository changes and push to the configured branch, including the default main branch.

Mitigation: Configure an agent-specific branch, prefer sync with --no-push, inspect status and diffs before committing, and enforce GitHub branch protection for main.

## Reference(s):

- [Ops Playbook](references/ops-playbook.md)
- [Knowledgebase Configuration](references/kb-config.json)
- [ClawHub Skill Page](https://clawhub.ai/reed1898/skills/knowledgebase-share)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Git branch, pull request, sync, and conflict-resolution procedures for a configured knowledge repository.]

## Skill Version(s):

0.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
