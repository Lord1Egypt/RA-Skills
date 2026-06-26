## Description: <br>
Audits local and remote Git branches, classifies merged, stale, orphaned, and active branches, and produces a prioritized cleanup plan with review guidance and delete commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to audit branch state, identify merged or stale branches, and prepare cleanup commands while preserving protected and active work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated delete commands can remove local or remote branches, including branches shared with collaborators. <br>
Mitigation: Treat generated commands as a manual change plan; review branch names, the default branch, protected branch patterns, and remote deletes before running them. <br>
Risk: Stale or unmerged branch classifications can miss context that is not visible from Git metadata or optional PR lookup. <br>
Mitigation: Confirm stale and force-delete candidates with branch owners or PR status before deleting unmerged work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-git-branch-janitor) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables and inline bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are presented as a manual cleanup plan for user review before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
