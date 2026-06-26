## Description: <br>
Control Little Snitch firewall on macOS to view logs, manage profiles and rule groups, monitor network traffic, check firewall activity, enable or disable profiles and blocklists, and troubleshoot network connections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate the Little Snitch command-line interface on macOS for firewall inspection, profile changes, rule-group management, log review, traffic monitoring, backups, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide privileged Little Snitch firewall changes, including profile changes, rule-group changes, preference writes, restores, backup exports, and traffic captures. <br>
Mitigation: Prefer read-only log and status commands first, verify the official Little Snitch CLI is installed, and approve privileged commands only when specifically requested. <br>
Risk: Enabling Little Snitch command-line access can be misused if untrusted processes gain root privileges. <br>
Mitigation: Enable CLI access only on trusted macOS systems and keep root access restricted to trusted processes. <br>


## Reference(s): <br>
- [Little Snitch Command Line Interface](https://help.obdev.at/littlesnitch5/adv-commandline) <br>
- [ClawHub Skill Page](https://clawhub.ai/gumadeiras/little-snitch) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/gumadeiras) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose privileged macOS Little Snitch commands that require explicit user approval before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
