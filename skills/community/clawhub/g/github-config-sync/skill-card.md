## Description: <br>
一键同步Hermes配置和数据到GitHub，支持多设备间无缝切换。每次修改后只需一句命令就能同步所有内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangwenhao66](https://clawhub.ai/user/zhangwenhao66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hermes users use this skill to synchronize configuration, memories, skills, and other local Hermes data between machines through a GitHub-backed workflow. It is intended for people moving settings between Mac and Windows or maintaining a backup of Hermes files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync workflow can copy credentials, authentication files, sessions, or other secrets into a Git repository. <br>
Mitigation: Do not sync .env, auth.json, sessions, or other sensitive files; remove those copy commands or add the paths to .gitignore before running the workflow. <br>
Risk: The documentation and helper script point users toward a specific repository URL, which could lead to pushing private Hermes data to a repository the user does not control. <br>
Mitigation: Use only a repository you own, preferably private, and verify git remote -v before any push. <br>
Risk: Pulled Hermes skills and configuration may execute or influence agent behavior after restoration. <br>
Mitigation: Review restored skills and configuration as code from the remote repository, scan them before use, and back up local Hermes files before pulling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangwenhao66/github-config-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and an optional shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes push and pull workflows for copying Hermes files to and from a GitHub-backed sync directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
