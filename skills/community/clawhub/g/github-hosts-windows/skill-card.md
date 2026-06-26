## Description: <br>
Optimize GitHub access speed on Windows by finding faster IP addresses and updating the hosts file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vay-qz](https://clawhub.ai/user/vay-qz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Windows users use this skill when GitHub access is slow and they want an agent to propose or run a hosts-file based routing update for GitHub domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent system-wide hosts-file changes can route GitHub domains through incorrect or stale IP addresses. <br>
Mitigation: Require the agent to show proposed entries, validate each GitHub domain separately, and back up the existing hosts file before any administrator-level change. <br>
Risk: A general GitHub slowness request could lead to unnecessary administrator privileges and difficult rollback. <br>
Mitigation: Confirm that the user intentionally chose the hosts-file fix and provide exact rollback steps before requesting elevation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vay-qz/github-hosts-windows) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with PowerShell and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Windows hosts-file entries and DNS cache commands that require administrator review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
