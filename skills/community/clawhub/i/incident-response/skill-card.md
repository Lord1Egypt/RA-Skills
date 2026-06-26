## Description: <br>
Structured 7-phase incident response for OpenClaw system failures, guiding agents through triage, evidence collection, root cause analysis, restore, prevention, monitoring, and documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to investigate OpenClaw incidents such as config loss, binding changes, gateway crashes, missing settings, and routing failures. It helps collect evidence, identify root cause, restore known-good state, add prevention controls, monitor for recurrence, and document lessons learned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote recovery actions can change live OpenClaw configuration or restart services. <br>
Mitigation: Require explicit review, a narrow target host and scope, and a rollback plan before restoring configs or restarting services. <br>
Risk: The workflow can edit agent rules, commit changes, change permissions, and create persistent cron monitoring. <br>
Mitigation: Allow these actions only for trusted agents, review each proposed persistent change, and define when monitoring should stop. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/incident-response) <br>
- [README](artifact/README.md) <br>
- [Quick Diagnosis Checklists](artifact/references/checklists.md) <br>
- [Cron Job Template for Incident Monitoring](artifact/references/cron-template.md) <br>
- [Prevention Patterns](artifact/references/prevention-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands, investigation notes, root cause statements, restore confirmations, prevention steps, monitoring cron prompts, and documentation updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires exec access, SSH access to the affected OpenClaw host, config backups, and a git audit trail for full workflow execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.yml, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
