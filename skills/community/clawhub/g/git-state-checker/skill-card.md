## Description:

Reports git repository status including modified files, untracked files, recent commits, and stash list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review working tree changes, recent commits, and stashes before solidify operations or when diagnosing repository issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reported a benign result with medium confidence, but one component was only partially inspected and the tool-misuse check was degraded.

Mitigation: Consider the limited scan coverage and review the skill before installation.

Risk: The report can include repository paths, commit messages, and stash details that may be sensitive.

Mitigation: Review the report before sharing it outside the repository team.

## Reference(s):

- [git-state-checker on ClawHub](https://clawhub.ai/147258xuan/skills/git-state-checker)
- [Publisher profile: 147258xuan](https://clawhub.ai/user/147258xuan)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text repository status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports staged, modified, and untracked paths; up to five recent commits and stash entries; and warns when more than ten stashes exist.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
