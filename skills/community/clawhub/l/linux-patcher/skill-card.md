## Description: <br>
Automated Linux server patching and Docker container updates. Use when the user asks to update, patch, or upgrade Linux servers, apply security updates, update Docker containers, check for system updates, or manage server maintenance across multiple hosts. Supports Ubuntu, Debian, RHEL, AlmaLinux, Rocky Linux, CentOS, Amazon Linux, and SUSE. Includes PatchMon integration for automatic host detection and intelligent Docker handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JGM2025](https://clawhub.ai/user/JGM2025) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, system administrators, and infrastructure operators use this skill to preview and apply Linux package updates, Docker image refreshes, and container restarts across one or more SSH-accessible hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically modify multiple remote hosts and Docker containers using powerful credentials. <br>
Mitigation: Start with dry-run on staging hosts, require explicit host scope and confirmation before applying updates, and schedule production use during maintenance windows. <br>
Risk: Passwordless sudo and PatchMon credentials can increase impact if misconfigured or exposed. <br>
Mitigation: Use restricted sudoers entries or controlled wrapper commands, protect SSH keys and PatchMon credentials, and keep credential files readable only by the intended user. <br>
Risk: Docker updates can recreate containers and briefly interrupt services. <br>
Mitigation: Make Docker updates opt-in for production when appropriate, use the skip-Docker mode for package-only patching, and verify container health after updates. <br>
Risk: Several supported Linux distributions are documented as untested. <br>
Mitigation: Test untested distributions in a non-production environment before broad rollout and verify package manager behavior after the first run. <br>


## Reference(s): <br>
- [PatchMon Integration Guide](references/patchmon-setup.md) <br>
- [PatchMon Documentation](https://docs.patchmon.net) <br>
- [PatchMon Repository](https://github.com/PatchMon/PatchMon) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke SSH, package manager, Docker, and PatchMon-related commands when used by an agent.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
