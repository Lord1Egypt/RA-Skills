## Description: <br>
Use when auditing and remediating an OpenClaw Linux host with a nightly 23:00 security run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scorpion7slayer](https://clawhub.ai/user/scorpion7slayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit and harden an OpenClaw Linux host, schedule nightly checks, and guide remediation for firewall, SSH, Docker, updates, disk, login, and VirusTotal review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent privileged system changes automatically. <br>
Mitigation: Install it only on the intended OpenClaw Linux host, review or pin the npm package, inspect the configuration, and run an initial pass with auto-remediation disabled when possible. <br>
Risk: SSH hardening can lock out administrators if key access, firewall rules, or the new SSH port are wrong. <br>
Mitigation: Verify key-based access and recovery access before changing SSH settings, allow the target port in the firewall, and test the new login from a second terminal before removing legacy access. <br>
Risk: Docker allowlist enforcement, unexpected-port blocking, disk cleanup, or service changes can disrupt running workloads. <br>
Mitigation: Review expected ports, allowed containers, and cleanup settings before strict enforcement; treat Docker and disk cleanup controls as service-impacting. <br>
Risk: VirusTotal file uploads may disclose samples outside the organization. <br>
Mitigation: Prefer hash-based public report review and upload files only after explicit user approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scorpion7slayer/nxtsecure-openclaw) <br>
- [OpenClaw Homepage](https://openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privileged remediation commands, cron setup, and browser-assisted VirusTotal review steps.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
