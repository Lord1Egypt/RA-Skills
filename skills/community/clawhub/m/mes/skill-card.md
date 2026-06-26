## Description: <br>
Manufacturing execution system tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to run a local command-line tracker for MES status, entries, search, statistics, configuration, and exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MES entries and export files may contain sensitive operational data stored on the local machine. <br>
Mitigation: Use an appropriate MES_DIR, protect local storage and exports, and avoid storing secrets or regulated production data unless local storage is acceptable. <br>
Risk: The remove command deletes the selected entry immediately and there is no built-in undo. <br>
Mitigation: Verify the entry number before removal and keep a backup or export when records need to be recoverable. <br>


## Reference(s): <br>
- [Mes on ClawHub](https://clawhub.ai/xueyetianya/mes) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text stdout with local JSONL storage and optional JSON or CSV export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses exit code 0 on success and 1 on error; stores data under MES_DIR or ~/.mes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
