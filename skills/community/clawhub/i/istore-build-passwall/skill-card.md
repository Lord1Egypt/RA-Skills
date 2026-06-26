## Description: <br>
Clones the iStoreOS repository, creates a PassWall GitHub Actions build workflow, and pushes it to a specified GitHub repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veelove](https://clawhub.ai/user/veelove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and router maintainers use this skill to add a GitHub Actions workflow to an iStoreOS fork, build PassWall packages, and package a .run installer for supported architectures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive GitHub credentials with write access. <br>
Mitigation: Use a fine-grained, short-lived token limited to the target fork or GitHub CLI authentication, and revoke the token after use. <br>
Risk: The documented push flow can overwrite repository contents. <br>
Mitigation: Use a disposable fork or new branch and back up the repository before running the workflow setup. <br>
Risk: The generated workflow and .run installer affect router software installation. <br>
Mitigation: Inspect the workflow and generated installer before running it on a router. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veelove/istore-build-passwall) <br>
- [Build PassWall workflow](artifact/references/build-passwall.yml) <br>
- [iStoreOS repository](https://github.com/istoreos/istoreos.git) <br>
- [OpenWrt PassWall releases](https://api.github.com/repos/Openwrt-Passwall/openwrt-passwall/releases/latest) <br>
- [OpenWrt PassWall2 releases](https://api.github.com/repos/Openwrt-Passwall/openwrt-passwall2/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with inline bash commands and workflow configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and push a GitHub Actions workflow that produces .run installer artifacts.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
