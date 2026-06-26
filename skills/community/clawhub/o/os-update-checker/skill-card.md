## Description: <br>
Checks available OS and global npm package updates, summarizes changelog context, and classifies update risk without installing or modifying packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to inspect pending system and global npm package updates before approving upgrades or running periodic health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run read-only local package-manager and global npm inventory commands. <br>
Mitigation: Review the proposed command execution in sensitive environments and run only where local package inventory disclosure is acceptable. <br>
Risk: Changelog and registry metadata lookups may disclose package names to distribution servers or the npm registry. <br>
Mitigation: Use --no-changelog, or avoid the skill in private, sensitive, or air-gapped environments where package names should not leave the machine. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pfrederiksen/os-update-checker) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON package update report with changelog summaries and risk labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only local package-manager inventory; optional changelog and npm registry metadata lookup can be skipped with --no-changelog.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
