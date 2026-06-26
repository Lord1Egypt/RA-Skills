## Description: <br>
Checks the integrity and operational status of a local mem0 memory system when asked about mem0 functionality, status, or completeness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chircken891](https://clawhub.ai/user/chircken891) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who maintain a local mem0 memory setup use this skill to run health checks for semantic search, memory count retrieval, cron jobs, and the Chroma vector store, then summarize normal and missing functionality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the status checks can expose local mem0 records and system paths. <br>
Mitigation: Require explicit diagnostic consent before running checks, report counts and status by default, and redact memory contents from the final report. <br>
Risk: The checklist includes destructive capabilities such as delete, delete_all, and reset. <br>
Mitigation: Keep destructive checks out of any automatic status flow and require separate user confirmation before testing or invoking them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chircken891/mem0-status-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown status report with PowerShell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local mem0 status and counts; raw memory contents should be redacted unless explicitly approved.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
