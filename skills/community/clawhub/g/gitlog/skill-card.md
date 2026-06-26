## Description: <br>
View formatted commit history, author stats, and commit frequency patterns. Use when reviewing logs, comparing contributions, or generating repo reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Gitlog to record and review local notes about git and release workflows, including checks, validations, changelog generation, diffs, lint results, and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gitlog stores typed log entries persistently on the local machine, which could retain secrets, tokens, confidential unreleased details, or sensitive compliance notes. <br>
Mitigation: Avoid entering sensitive information and review or delete ~/.local/share/gitlog when local retention is no longer needed. <br>
Risk: The tool is described as a local logging utility and does not inspect git history itself. <br>
Mitigation: Use it as a manual note log for git and release workflow entries, not as an automated source of repository truth. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/gitlog) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text with optional JSON, CSV, or plain-text exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-entered log entries locally under ~/.local/share/gitlog and can export accumulated entries.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
