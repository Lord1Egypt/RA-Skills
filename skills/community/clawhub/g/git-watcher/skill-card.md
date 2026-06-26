## Description: <br>
Tracks, commits, compares, and rolls back OpenClaw configuration changes with local Git checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create local Git checkpoints for OpenClaw configuration, inspect config diffs, and restore prior versions after a risky or broken change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage broad local configuration changes, including credential files, before committing. <br>
Mitigation: Review the files selected for commit, avoid committing real credentials, and use sanitized staging copies or explicit exclusions for sensitive credential material. <br>
Risk: The skill can rewrite live credential files during redaction and can restore older configuration over the current working tree. <br>
Mitigation: Back up ~/.openclaw before use, preview restore diffs, and require explicit confirmation before overwriting current configuration. <br>


## Reference(s): <br>
- [Git Watcher on ClawHub](https://clawhub.ai/wangjipeng977/git-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Git commits and restore tracked OpenClaw configuration files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
