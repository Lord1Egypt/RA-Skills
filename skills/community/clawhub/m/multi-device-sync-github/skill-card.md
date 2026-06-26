## Description: <br>
Synchronizes OpenClaw workspace data across multiple machines through a private GitHub repository, with setup guidance, file watching, periodic pulls, and conflict handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RegulusZ](https://clawhub.ai/user/RegulusZ) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure and operate GitHub-backed synchronization of workspace files across Linux and macOS devices, including initialization, status checks, conflict resolution, and device onboarding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can continuously sync sensitive OpenClaw workspace files and behavior settings to GitHub. <br>
Mitigation: Use a private, dedicated GitHub repository, verify exactly which files are selected for sync, and exclude SOUL.md, skills/, MEMORY.md, or memory/ unless that context is intended to be shared across devices. <br>
Risk: The installer can be run as remote shell code. <br>
Mitigation: Download or clone the installer, review it locally, and run it only after confirming the requested file access and GitHub repository target. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RegulusZ/multi-device-sync-github) <br>
- [README](README.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that install dependencies, initialize sync repositories, manage the sync daemon, and resolve conflicts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
