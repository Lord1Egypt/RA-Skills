## Description: <br>
Diagnose, configure, and recover remote access to a macOS machine over Tailscale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lliangcol](https://clawhub.ai/user/lliangcol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to set up, diagnose, and recover remote access to macOS machines over Tailscale, including SSH, Screen Sharing/VNC, Tailscale ACLs, and GUI fallback tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent remote-access settings can expose a Mac if credentials, ACLs, startup access, or macOS privacy permissions are configured too broadly. <br>
Mitigation: Use strong unique passwords or MFA where supported, restrict Tailscale ACLs to trusted administrators, download remote tools only from official sources, review macOS Privacy & Security permissions, and disable unattended or startup access when no longer needed. <br>


## Reference(s): <br>
- [ACL template](references/acl-template.md) <br>
- [AnyDesk / RustDesk notes](references/anydesk-rustdesk.md) <br>
- [Baseline checklist](references/checklist.md) <br>
- [SOP](references/sop.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only remote-access troubleshooting guidance; no external tool calls are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
