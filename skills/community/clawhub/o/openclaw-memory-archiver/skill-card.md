## Description: <br>
Memory Archiver scans older memory logs, summarizes important information into long-term memory, archives the logs, and can clean up expired files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangkai258](https://clawhub.ai/user/yangkai258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep memory logs manageable by archiving files older than a configured threshold while preserving important decisions, context, and todos in MEMORY.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Original memory logs can be deleted after archiving when delete_after_archive is enabled. <br>
Mitigation: Keep deletion disabled unless cleanup is intended, and verify archives are readable and backed up before allowing original logs to be removed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md, create zip archives under memory/archive/, and delete original logs when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
