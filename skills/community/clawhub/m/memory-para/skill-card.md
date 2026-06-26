## Description: <br>
Memory Management (PARA) helps OpenClaw agents distill raw daily memory logs into structured Root and PARA memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hugo-Zhu](https://clawhub.ai/user/Hugo-Zhu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and agent maintainers use this skill to maintain long-term memory by distilling daily logs, routing durable facts into Root and PARA files, archiving processed logs, and updating a global memory index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite persistent OpenClaw memory files. <br>
Mitigation: Keep the skill manually invoked or require reviewable diffs before applying updates to core memory files. <br>
Risk: The maintenance SOP deletes processed raw daily logs after archiving. <br>
Mitigation: Back up memory files and confirm archive updates before allowing deletion of processed logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hugo-Zhu/memory-para) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with file-update and shell-install instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce proposed edits to persistent memory files and archival cleanup steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
