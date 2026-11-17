## Description:

Use this skill when installing, upgrading, verifying, or publishing the EverMemory OpenClaw plugin and its companion skill, including local path install, npm install, ClawHub publish, and release-gate verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao321](https://clawhub.ai/user/jiehao321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to install, upgrade, verify, and publish the EverMemory OpenClaw plugin and companion ClawHub skill while following documented release gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publish and verification scripts may under-enforce their documented public release safety checks.

Mitigation: Review the scripts before use, inspect package contents before npm publishing, and manually run the documented release and benchmark gates.

Risk: Installation verification may not fully prove that memory slot binding and skill readiness checks passed.

Mitigation: Do not rely on verify_install.sh alone; confirm gateway status, plugin details, slot binding, and skill readiness from command output.

## Reference(s):

- [EverMemory Install/Publish Playbook](references/publish-and-install-playbook.md)
- [ClawHub Skill Page](https://clawhub.ai/jiehao321/skills/openclaw-evermemory-installer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose installation, verification, release-gate, ClawHub publish, and npm publish commands for human review before execution.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
