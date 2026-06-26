## Description: <br>
King's Watching helps developers translate and run multi-step AI workflows as sequential, checkpointed execution plans with progress reporting, heartbeat support, and step verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d0roro](https://clawhub.ai/user/d0roro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to structure long-running or high-volume agent work into explicit steps, checkpoints, progress reports, and verification checks. It is suited to research, reporting, data processing, and similar workflows where users want clearer progress and resumability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the skill overstates workflow-enforcement, resume, verification, and audit-trace guarantees. <br>
Mitigation: Validate the workflow on representative tasks before relying on these guarantees, and require users to review progress and final outputs. <br>
Risk: Broad automated bulk-download or bulk-API prompts can create unwanted activity or collect from untrusted sources. <br>
Mitigation: Set explicit task bounds, trusted sources, rate limits, and output folders before execution. <br>
Risk: Local checkpoint files may persist workflow state or task content. <br>
Mitigation: Use controlled storage locations, avoid sensitive data where possible, and clean up checkpoint files after completion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/d0roro/kingswatching) <br>
- [README](artifact/README.md) <br>
- [User Guide](artifact/USER_GUIDE.md) <br>
- [Installation Guide](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets, shell commands, configuration examples, and runtime status/result dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflow execution may write local checkpoint and state files in configured state directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and setup.py report 0.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
