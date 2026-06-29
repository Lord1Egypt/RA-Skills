## Description: <br>
NetBox Sync Ops guides agents through safe deployment, scheduling, extension, and troubleshooting of netbox-proxmox-sync for idempotent NetBox inventory updates from Proxmox VE, UniFi, and optional iDRAC/Redfish enrichment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddygk](https://clawhub.ai/user/eddygk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to configure, run, schedule, extend, and troubleshoot NetBox inventory syncs for Proxmox VE, UniFi, and optional iDRAC/Redfish enrichment while preserving idempotent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect operational guidance or unreviewed changes could affect NetBox inventory records in a production environment. <br>
Mitigation: Use the documented dry-run and report flow first, confirm the target and credentials, and review proposed create, update, or delete actions before applying. <br>
Risk: The reaper lifecycle can mark or delete sync-owned VM records when a Proxmox VMID is no longer present. <br>
Mitigation: Run with --no-reap until ownership rules and reaper thresholds are reviewed, and enable deletion only when the environment intentionally allows it. <br>
Risk: The skill requires infrastructure credentials and is intended for users who understand its administrative scope. <br>
Mitigation: Install and run it only in a trusted ClawHub or staff development environment, and confirm credentials and production targets before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eddygk/skills/netbox-sync-ops) <br>
- [netbox-proxmox-sync homepage](https://github.com/eddygk/netbox-proxmox-sync) <br>
- [Extending](references/extending.md) <br>
- [Gotchas](references/gotchas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run, reporting, scheduling, troubleshooting, and idempotency-check recommendations.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
