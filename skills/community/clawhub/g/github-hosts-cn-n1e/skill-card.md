## Description: <br>
Updates a system hosts file with GitHub-related host entries for users in China while preserving non-GitHub entries, showing risk warnings, and supporting backup-oriented workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n1e](https://clawhub.ai/user/n1e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to preview or apply GitHub-related hosts-file entries when troubleshooting GitHub access from China. It is intended for environments where the user accepts privileged hosts-file modification and verifies proposed network changes first. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes the system hosts file for GitHub access and requires sudo or administrator access, which can affect network behavior. <br>
Mitigation: Use preview mode first, verify the proposed entries, run only in a trusted environment, and keep a manual hosts-file backup before applying changes. <br>
Risk: The advertised restore flow appears broken, creating rollback risk for a privileged networking change. <br>
Mitigation: Do not rely solely on the built-in restore command until fixed; keep a separate manual backup and verify rollback steps before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n1e/github-hosts-cn-n1e) <br>
- [README.md](README.md) <br>
- [HelloGitHub hosts source](https://raw.hellogithub.com/hosts) <br>
- [GitLab ineo6 hosts source](https://gitlab.com/ineo6/hosts/-/raw/master/hosts) <br>
- [Gitee hosts mirror](https://gitee.com/peng_zhihui/hosts/raw/master/hosts) <br>
- [JSDelivr hosts mirror](https://cdn.jsdelivr.net/gh/ineo6/hosts@master/hosts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and terminal guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce privileged hosts-file changes and command output when the generated commands are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
