## Description: <br>
Recovers broken agent state via crash recovery, context overflow, and merge conflict protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to recover from interrupted or inconsistent coding-agent sessions, including crashes, context overflow, merge conflicts, and divergent task, git, or disk state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest git mutations such as stash, commit, restore, reset, merge-abort, or rebase-abort during recovery. <br>
Mitigation: Review each proposed git mutation before execution and require the agent to inspect status and diffs before changing repository state. <br>
Risk: Broad activation terms such as recovery, context, conflicts, and state can invoke the skill outside the intended failure-recovery scenario. <br>
Mitigation: Confirm that a crash, context overflow, merge conflict, or inconsistent task/git/disk state exists before applying the recovery protocol. <br>
Risk: Recovery actions can preserve or discard partial work incorrectly if current state is not grounded in durable evidence. <br>
Mitigation: Use task records, git history, git status, diffs, and explicit handoff summaries as ground truth before resuming, stashing, or rolling back work. <br>


## Reference(s): <br>
- [ClawHub metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown procedures with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recovery protocols, decision criteria, escalation notes, and risk-assessment checklist templates.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
