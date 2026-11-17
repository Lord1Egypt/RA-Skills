## Description:

Control Little Snitch firewall on macOS. View logs, manage profiles and rule groups, monitor network traffic. Use when the user wants to check firewall activity, enable/disable profiles or blocklists, or troubleshoot network connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to administer Little Snitch on macOS, inspect firewall activity, manage profiles and rule groups, and troubleshoot network traffic through documented CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Little Snitch CLI access and sudo commands can make high-impact firewall, profile, rule group, preference, restore, or traffic-capture changes.

Mitigation: Install only when the agent should help administer Little Snitch, and confirm each privileged action before running it.

Risk: Enabling CLI access can be misused if untrusted processes obtain root privileges.

Mitigation: Keep root access restricted to trusted processes and review proposed commands before execution.

## Reference(s):

- [Little Snitch command line documentation](https://help.obdev.at/littlesnitch5/adv-commandline)
- [ClawHub skill page](https://clawhub.ai/gumadeiras/skills/little-snitch)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sudo commands for Little Snitch administration on macOS.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
