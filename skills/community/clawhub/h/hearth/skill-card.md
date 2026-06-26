## Description: <br>
Hearth runs a configuration-driven, read-only health-check sweep across homelab devices, reporting reachability, uptime/load, memory/disk, services, and app health in a consistent format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nj070574-gif](https://clawhub.ai/user/nj070574-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Homelab admins, sysadmins, network engineers, and OpenClaw users use Hearth to check configured devices and receive a consistent read-only health snapshot before investigating failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use SSH credentials and bearer tokens while probing networked devices. <br>
Mitigation: Audit devices.yaml before use, prefer SSH keys and scoped tokens, and keep long-lived secrets out of shell profiles. <br>
Risk: Configured command probes can run shell commands on devices even though the skill presents itself as read-only. <br>
Mitigation: Use command probes only when the commands were written and reviewed by the operator, and run --dry-run before probing a new configuration. <br>
Risk: The security guidance notes weakened SSH credential safety and recommends caution around host-key verification. <br>
Mitigation: Review the SSH options before use and keep host-key verification enabled wherever possible. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nj070574-gif/hearth) <br>
- [README](README.md) <br>
- [Configuration reference](docs/CONFIG.md) <br>
- [Installation guide](docs/INSTALL.md) <br>
- [Probe reference](docs/PROBES.md) <br>
- [Platform support](docs/PLATFORMS.md) <br>
- [Troubleshooting guide](docs/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and terminal-style health-check output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows raw sweep output for each configured device and can guide dry runs, single-device checks, group checks, and configuration updates.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata and user changelog entry) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
