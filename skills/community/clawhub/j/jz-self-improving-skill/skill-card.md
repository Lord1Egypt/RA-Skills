## Description: <br>
Helps writing-style skills learn from human edits by recording original and final drafts, extracting recurring rules, and updating a target SKILL.md for Claude Code or OpenClaw workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzocb](https://clawhub.ai/user/jzocb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and writing-skill maintainers use this skill to record AI-generated originals and human-approved finals, identify recurring edit patterns, and turn those patterns into proposed or applied updates for a target skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores full draft and final text locally, which can include sensitive content. <br>
Mitigation: Use explicit per-project log directories, avoid secret-bearing content, and review stored logs before sharing or syncing them. <br>
Risk: The improve workflow can automatically rewrite another skill's instructions on disk. <br>
Mitigation: Run extract, show, and apply manually first; review proposals and diffs before enabling auto mode or scheduled execution. <br>
Risk: Automatically generated improvement rules can introduce incorrect or misleading guidance. <br>
Mitigation: Apply only reviewed proposals, rely on backups for rollback, and test rollback behavior before unattended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jzocb/jz-self-improving-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown proposals, CLI status text, JSONL observation logs, and updated skill instruction files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local logs, proposal files, backups, and target SKILL.md updates when the user runs the included scripts.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
