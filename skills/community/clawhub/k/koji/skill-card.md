## Description: <br>
Manage Koji build system tasks, packages, tags, repositories, users, archives, buildroots, SRPMs, and RPMs with broad command guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and build-system administrators use this skill to operate Koji build infrastructure, including builds, tasks, packages, tags, repositories, users, permissions, and buildroots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact Koji operations such as deletions, cancellations, permission changes, uploads, repository changes, and cleanup actions. <br>
Mitigation: Use a least-privileged Koji account and require explicit human approval before executing those operations. <br>
Risk: Commands may target the wrong Koji instance, package, tag, repository, task, buildroot, or user if inputs are not verified. <br>
Mitigation: Verify the configured Koji instance and all object names or IDs before running generated commands. <br>


## Reference(s): <br>
- [ClawHub Koji skill page](https://clawhub.ai/weidongkl/koji) <br>
- [Koji official documentation](https://koji.fedoraproject.org/docs/) <br>
- [Koji API documentation](https://koji.fedoraproject.org/docs/developer/) <br>
- [Fedora packaging guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/) <br>
- [Fedora DistGit](https://src.fedoraproject.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output for Koji administration workflows.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
