## Description: <br>
Memory Manager helps agents maintain OpenClaw memory with snapshots, health checks, search troubleshooting, review workflows, safe archival, and provider/index diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hazemelerefey](https://clawhub.ai/user/hazemelerefey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to protect and maintain OpenClaw workspace memory before risky work, troubleshoot memory retrieval, draft durable memory reviews, and archive older daily notes safely. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references PowerShell scripts that were not present in the artifact evidence. <br>
Mitigation: Review the installed package before running commands and only execute scripts that exist at the resolved skill package path. <br>
Risk: Repair, archive, and long-term memory workflows can modify persistent workspace memory files. <br>
Mitigation: Manually approve those operations and create a snapshot before moving, rewriting, or repairing memory files. <br>


## Reference(s): <br>
- [Memory Manager workflow](references/workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/hazemelerefey/openclaw-memory-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with PowerShell command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose memory snapshots, diagnostics, review drafts, search workflows, and archive steps for user approval.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
