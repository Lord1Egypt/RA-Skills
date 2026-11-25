## Description:

Search Git projects and normal files for literal text quickly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[selectxx](https://clawhub.ai/user/selectxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can search a file or directory for a literal string, including tracked and untracked files in nested Git worktrees. The skill returns matching file paths and indicates how each match was found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When searching a Git worktree with attacker-controlled local Git configuration, running the search may trigger an external Git hook.

Mitigation: Review the script before installing and avoid running it on worktrees with attacker-controlled local Git configuration. Scanner coverage was incomplete, so the results do not establish that the skill is safe.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/selectxx/skills/tree/main/git-fast-content-search)
- [ClawHub skill release](https://clawhub.ai/selectxx/skills/git-fast-content-search)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON Lines by default; optional tab-separated text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each match reports an absolute path, whether it is a Git project file, and the search method.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
