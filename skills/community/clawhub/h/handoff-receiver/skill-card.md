## Description: <br>
Receive a prior session handoff and continue execution safely by validating repo state, resuming from next steps, and refreshing the handoff artifact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to resume work from a prior session handoff, validate repository state against the handoff, continue the next recorded task, and refresh the handoff artifact before yielding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and updates handoff files, so stale, orphaned, or parallel handoffs could cause the agent to resume the wrong work stream. <br>
Mitigation: Review the CURRENT pointer and INDEX before proceeding, surface paused or orphan streams, and ask for clarification when the active handoff is ambiguous. <br>
Risk: Repository state may differ from the state recorded in the handoff. <br>
Mitigation: Run git branch, status, diff, and recent log checks before editing, then ask for clarification if the mismatch is major. <br>
Risk: Normal use can modify handoff metadata files. <br>
Mitigation: Keep updates factual and concise, remove completed next steps, and review file changes before committing or publishing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clarezoe/handoff-receiver) <br>
- [README](artifact/README.md) <br>
- [Resolved orphan handoffs issue](artifact/RESOLVED/ISSUE-orphan-handoffs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and a structured takeover status report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update handoff files and status metadata during normal use.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
