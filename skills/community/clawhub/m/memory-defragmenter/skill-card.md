## Description: <br>
Defragment and optimize agent memory files by cleaning duplicates, merging similar entries, archiving stale content, and ensuring proper tiering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klemenska](https://clawhub.ai/user/klemenska) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect, plan, and apply cleanup for local agent memory markdown files so duplicate, stale, or overlarge entries can be reviewed and reorganized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local agent memory markdown and create backup copies from broad home-directory paths. <br>
Mitigation: Run it only against a known memory directory with an explicit --path, and remove .defrag_backup copies after confirming they are no longer needed. <br>
Risk: Execution behavior is less scoped and less accurate than advertised. <br>
Mitigation: Run --plan or --dry-run first, inspect the generated plan manually, and run verify_memory.py after any execution. <br>
Risk: Memory files and backups may contain sensitive personal or operational information. <br>
Mitigation: Limit access to generated plans and backups, review them before sharing, and delete sensitive backup copies when retention is no longer required. <br>


## Reference(s): <br>
- [Memory Defragmentation Rules](references/rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Console reports and Markdown defragmentation plans with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create backup copies and plan files when execution or plan modes are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
