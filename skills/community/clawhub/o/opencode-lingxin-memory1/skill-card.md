## Description: <br>
为 OpenCode AI 助手提供轻量级跨会话记忆持久化，面向灵芯派等低资源设备，并支持通过 Git 和 Gitee 同步备份。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmww](https://clawhub.ai/user/nmww) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using OpenCode on SmartPi, ARM64, or other constrained Debian-style devices use this skill to preserve local assistant context, review prior work, and synchronize memory files to a configured Gitee repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files may contain private chat context, host details, credentials, or other sensitive information that could be pushed to a remote Gitee repository. <br>
Mitigation: Use a private repository, review memory files before synchronization, and avoid storing secrets or private chat content. <br>
Risk: The security scan reports a plaintext credential exposure in the package. <br>
Mitigation: Remove or rotate any plaintext credentials before installation or synchronization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nmww/opencode-lingxin-memory1) <br>
- [Project homepage](https://gitee.com/st_gitee_1/old-version-of-lingxin-sect) <br>
- [Publisher profile](https://clawhub.ai/user/nmww) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory files and Git/Gitee synchronization steps for agent context persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
