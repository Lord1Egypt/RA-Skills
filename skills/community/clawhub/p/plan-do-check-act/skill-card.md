## Description: <br>
PDCA workflow automation with session binding and progress recovery. Requires Python 3.6 and Git (optional). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucezhu888](https://clawhub.ai/user/brucezhu888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to break complex work into plan.md checklists, track execution status, recover incomplete work by session, and archive completed plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plan files may contain real session IDs or sensitive project details. <br>
Mitigation: Use a dedicated workspace and avoid storing sensitive identifiers or confidential project details in plan files that may be shared. <br>
Risk: Recovered progress may be inferred from recent file changes and can be incomplete or misleading. <br>
Mitigation: Review the reported progress before acting on it or resuming work. <br>
Risk: Archive cleanup can delete old archived plan files. <br>
Mitigation: Run cleanup with --dry-run first and confirm the target workspace and retention period. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucezhu888/plan-do-check-act) <br>
- [Publisher Profile](https://clawhub.ai/user/brucezhu888) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plan files, terminal status text, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local plan*.md files in the configured workspace; archive cleanup can remove old archived plan files.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
