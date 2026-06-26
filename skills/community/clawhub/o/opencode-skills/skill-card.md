## Description: <br>
Opencode automates website creation, project analysis, script execution, file management, server preview, and code generation tasks efficiently. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[linshuikeji](https://clawhub.ai/user/linshuikeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate opencode workflows for website generation, project analysis, file operations, local preview servers, task execution, and code generation in a supervised workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local automation can inspect, modify, copy, archive, extract, or delete workspace files. <br>
Mitigation: Use the skill only inside a known workspace, review commands before execution, and redact secrets before printing configuration or environment files. <br>
Risk: Local opencode servers may be exposed if started without authentication or bound beyond localhost. <br>
Mitigation: Bind servers to localhost and enable authentication where available before sharing access. <br>
Risk: Admin-style or destructive commands can disrupt the host environment. <br>
Mitigation: Require manual approval for sudo, firewall, chmod/chown, kill, archive extraction, copy, and rm -rf commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linshuikeji/opencode-skills) <br>
- [Publisher profile](https://clawhub.ai/user/linshuikeji) <br>
- [Opencode documentation](https://opencode.ai/docs) <br>
- [Opencode GitHub](https://github.com/opencode) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Artifact usage guide](artifact/README.md) <br>
- [Artifact references](artifact/REFERENCES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and example scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead an agent or user to execute local shell commands; privileged, destructive, server, cleanup, copy, extraction, and configuration inspection steps require explicit human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
