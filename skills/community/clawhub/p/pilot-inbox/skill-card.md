## Description: <br>
Unified inbox for incoming Pilot Protocol messages, files, tasks, and trust requests in one view. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and Pilot Protocol users use this skill to inspect and triage incoming messages, received files, received tasks, and pending trust requests from a single agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents commands that clear inbox items and received files. <br>
Mitigation: Review inbox contents first and only run clear commands after explicit user confirmation. <br>
Risk: The workflow depends on a local pilotctl installation and running Pilot Protocol daemon. <br>
Mitigation: Confirm pilotctl is trusted, on PATH, and connected to the intended daemon before using the skill. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [Pilot Inbox ClawHub release](https://clawhub.ai/teoslayer/pilot-inbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot Protocol daemon, and jq for the sample triage script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
