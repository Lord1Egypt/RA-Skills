## Description: <br>
Guides agents through OSTree atomic system update administration, including repository setup, commits, deployments, rollback, remote sync, branch management, and rpm-ostree workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and system administrators use this skill to plan and execute OSTree and rpm-ostree workflows for immutable Linux systems. It is most useful when an agent needs to produce operational guidance, command sequences, or configuration examples for atomic updates and rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes high-impact OSTree deployment, undeploy, rollback, prune, and repository modification examples that can affect host boot state or remove recovery options. <br>
Mitigation: Review commands before use, verify the target host and repository, inspect current deployment status, back up configuration, preserve rollback entries, and test recovery procedures before unattended cleanup. <br>
Risk: The security review marked the release suspicious because the administrative examples do not include enough safeguards for automated use. <br>
Mitigation: Treat generated commands as examples for a qualified operator to adapt, not safe defaults for direct unattended execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/weidongkl/ostree) <br>
- [OSTree Official Docs](https://ostreedev.github.io/ostree/) <br>
- [Fedora Silverblue Docs](https://silverblue.fedoraproject.org/) <br>
- [RHEL CoreOS Docs](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_coreos/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Administrative commands should be reviewed against the target host, repository, deployment status, and recovery plan before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
