## Description: <br>
Memory Enhancer Pro helps OpenClaw agents search, summarize, classify, clean up, and optimize local memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwg2025](https://clawhub.ai/user/williamwg2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to manage local agent memory, inspect token usage, generate memory-related suggestions, and optionally run scheduled cleanup or optimization tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads sensitive local OpenClaw memory, session, user, soul, and agent files. <br>
Mitigation: Install and run it only in workspaces where those local files are appropriate for memory analysis, and review outputs before sharing them. <br>
Risk: Cleanup and scheduled optimization flows can write logs or configuration and may delete older memory files when destructive modes are enabled. <br>
Mitigation: Run analysis or dry-run modes first, back up memory files, and use destructive execution only after confirming the target path and retention window. <br>
Risk: Security evidence reports confusing hardcoded paths that can write outside the Pro skill folder if installed under a different directory name. <br>
Mitigation: Verify the installed path and update hardcoded memory-enhancer paths before enabling schedules or write operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williamwg2025/openclaw-memory-enhancer-pro) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown memory content, and JSON configuration or statistics files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local OpenClaw memory files and scheduler configuration may affect what the scripts read, write, or report.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
