## Description: <br>
Install OpenClaw WORKSPACE_GOVERNANCE in minutes. Get guided setup, upgrade checks, migration, and audit for long-running workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Adamchanadam](https://clawhub.ai/user/Adamchanadam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, workspace operators, and teams using OpenClaw use this skill to install, upgrade, migrate, audit, and uninstall workspace governance flows with reviewable configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer and governance commands can make impactful workspace configuration changes. <br>
Mitigation: Back up important workspace configuration and review proposed openclaw.json, Brain Docs, migration, and uninstall changes before approving them. <br>
Risk: Using @latest can reduce reproducibility in production installs. <br>
Mitigation: Pin the package version for production workflows that require repeatable installation. <br>
Risk: The artifact includes an experimental gov_apply flow for controlled UAT only. <br>
Mitigation: Use the GA setup, migration, audit, uninstall, config, and diagnostic flows for production rollout; keep gov_apply behind explicit human approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Adamchanadam/openclaw-workspace-governance-installer) <br>
- [Project homepage](https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE) <br>
- [English README](https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.md) <br>
- [Governance handbook](https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.en.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and OpenClaw chat commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the openclaw binary and review of proposed workspace configuration changes.] <br>

## Skill Version(s): <br>
0.2.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
