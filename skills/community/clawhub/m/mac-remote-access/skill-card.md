## Description:

Diagnose, configure, and recover remote access to a macOS machine over Tailscale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lliangcol](https://clawhub.ai/user/lliangcol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT administrators, and operators use this skill to set up or troubleshoot secure remote access to macOS systems over Tailscale, including SSH, Screen Sharing/VNC, Tailscale ACLs, and GUI fallback tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote access setup can expose persistent administrative access to a Mac if passwords, ACLs, or unattended GUI tools are too broad.

Mitigation: Use dedicated passwords, narrow Tailscale ACLs to specific users and ports, and periodically review unattended AnyDesk or RustDesk startup behavior.

Risk: Running remote-access commands or changing macOS sharing settings on the wrong machine could disrupt access or weaken security.

Mitigation: Use this guidance only for Macs you own or administer, verify the target host and ports before changes, and preserve SSH as a break-glass recovery path.

## Reference(s):

- [ACL template](references/acl-template.md)
- [Baseline checklist](references/checklist.md)
- [SOP](references/sop.md)
- [AnyDesk / RustDesk notes](references/anydesk-rustdesk.md)
- [ClawHub skill page](https://clawhub.ai/lliangcol/skills/mac-remote-access)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Troubleshooting steps and configuration guidance for remote access paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
