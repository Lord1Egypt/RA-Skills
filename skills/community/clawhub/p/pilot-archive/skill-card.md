## Description: <br>
Index and search historical data exchanges, messages, and file transfers over Pilot Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create a searchable local archive of Pilot Protocol messages, file transfers, and communication metadata for auditing or historical analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The archive commands can persist Pilot messages and file-transfer details in plaintext local JSONL files. <br>
Mitigation: Use the skill only where archiving all accessible Pilot communications is acceptable, restrict file permissions on the archive directory, and define retention or deletion rules before indexing. <br>
Risk: Stored message content may include sensitive data that should not be searchable by every local user or downstream process. <br>
Mitigation: Apply filters or redaction before writing archive records, and limit access to $HOME/.pilot/archive. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-archive) <br>
- [Publisher profile](https://clawhub.ai/user/teoslayer) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JSONL archive indexes under $HOME/.pilot/archive when the suggested commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
