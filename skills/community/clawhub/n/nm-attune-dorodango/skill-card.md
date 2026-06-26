## Description: <br>
Polishes working code through successive quality passes in fresh subagents after tests pass and code needs multi-dimension refinement before release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a structured polishing workflow over working code before review or release. It guides correctness, clarity, consistency, and final polish passes, with optional fresh subagents for larger targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can iteratively edit target code while polishing it. <br>
Mitigation: Install and run it only for targets where agent review and modification are intended, then review the diff and run the relevant tests before merge or release. <br>
Risk: The workflow may create a local .attune/dorodango-state.json progress file. <br>
Mitigation: Run it in the intended workspace and inspect or remove the progress file if persisted state is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-attune-dorodango) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code edits, shell commands, and JSON state file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .attune/dorodango-state.json to track polishing progress.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
