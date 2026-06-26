## Description: <br>
Recovers broken agent state via crash recovery, context overflow, and merge conflict protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to recover interrupted work sessions after agent crashes, context overflow, merge conflicts, or inconsistent task and git state. It provides procedural playbooks for triage, checkpointing, conflict escalation, and safe continuation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recovery playbooks can steer agents toward git state-changing actions such as stash, commit, merge abort, and file restoration. <br>
Mitigation: Use the skill in repositories where those recovery actions are appropriate, inspect diffs before state changes, and keep human review for ambiguous conflicts or destructive choices. <br>
Risk: Broad recovery triggers may activate the skill for routine errors that do not require session-level recovery. <br>
Mitigation: Confirm the session involves an agent crash, context loss, merge conflict, or inconsistent task and git state before applying the protocols. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-damage-control) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell command examples, checklists, and recovery protocols.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces procedural recovery guidance and does not require API calls or generated files by itself.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
