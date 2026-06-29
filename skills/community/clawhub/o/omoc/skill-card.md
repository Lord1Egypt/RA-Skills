## Description: <br>
OMOC runtime for /goal, /ralplan, /team, /ralph, memory, leases, verifiers, and non-overlapping loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkobject](https://clawhub.ai/user/jkobject) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use OMOC to coordinate long-running OpenClaw work with durable goals, planning, task state, memory compaction, leases, verifier lanes, and review gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OMOC writes durable project state under .omoc, and those files can contain sensitive planning notes, task details, mailbox entries, goals, and memory. <br>
Mitigation: Treat .omoc as project-sensitive state, review it before sharing a workspace, and avoid committing or publishing it unless the contents are intended to be disclosed. <br>
Risk: The workflow can guide long-running local agent work, so accidental external messages, deploys, spending, or public actions would carry higher impact. <br>
Mitigation: Keep the documented confirmation boundary: require explicit approval before external messages, deploys, spending, or public actions. <br>
Risk: Completion claims may be unreliable if verifier or review evidence is skipped. <br>
Mitigation: Use the verifier lane and review gates before marking work complete, and record evidence in memory or task state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jkobject/omoc) <br>
- [README](README.md) <br>
- [Ralph cycle prompt template](templates/ralph-cycle.md) <br>
- [Team worker prompt template](templates/team-worker.md) <br>
- [Verifier prompt template](templates/verifier.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-backed local state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local .omoc workflow, memory, goal, team, Ralph, lease, mailbox, and review artifacts.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
