## Description: <br>
Advanced reputation analytics and trend visualization for Pilot Protocol agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to record Pilot Protocol reputation snapshots, inspect recent peer score history, and calculate reputation trends for trust decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local reputation snapshots can retain peer history that may be sensitive. <br>
Mitigation: Periodically rotate or delete ~/.pilot/reputation/data when the history is no longer needed. <br>
Risk: The continuous collection example keeps running and records snapshots on a schedule. <br>
Mitigation: Run the loop only deliberately, monitor it while active, and stop it when collection is finished. <br>
Risk: The skill provides Bash snippets that write local files and call pilotctl. <br>
Mitigation: Review the commands before running them and confirm pilotctl, jq, bc, and the Pilot daemon are available. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can create local JSON snapshot files under ~/.pilot/reputation/data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
