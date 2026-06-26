## Description: <br>
Audit and clean up Git repositories by finding stale or merged branches, large files in history, orphaned tags, repo bloat, and generating cleanup scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit Git repository health, identify branch and file-history cleanup opportunities, and generate reviewable cleanup commands before performing repository maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cleanup scripts can delete local branches and run repository optimization commands. <br>
Mitigation: Treat `--fix` output as a draft, review every command before execution, and keep backups or remote copies of important branches. <br>
Risk: `--force-delete` can generate force-deletion commands for branches that may contain unmerged work. <br>
Mitigation: Avoid `--force-delete` unless the affected branches are disposable or safely backed up. <br>
Risk: Auditing untrusted repositories can produce misleading cleanup recommendations or scripts. <br>
Mitigation: Run the skill only on repositories chosen explicitly and do not execute generated scripts from untrusted repositories without manual verification. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/git-repo-cleaner) <br>
- [Publisher Profile](https://clawhub.ai/user/charlie-morrison) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON, Markdown reports, and generated bash cleanup scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated cleanup scripts are printed for review and are not executed by the skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
