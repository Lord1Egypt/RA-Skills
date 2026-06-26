## Description: <br>
Write professional incident updates, blameless postmortems, maintenance announcements, and status reports for a status page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openstatus](https://clawhub.ai/user/openstatus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
On-call engineers, SREs, DevOps teams, engineering managers, and status page owners use this skill bundle to draft incident updates, postmortems, maintenance notices, and periodic reliability reports with consistent service context and tone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reusable .agents/status-page-context.md file can preserve service, SLA, tone, escalation, or incident details for later status-page tasks. <br>
Mitigation: Keep secrets, customer data, and sensitive unreleased incident details out of that context file unless they are intended to be reused by other status-page skills. <br>


## Reference(s): <br>
- [OpenStatus homepage](https://openstatus.dev) <br>
- [ClawHub skill page](https://clawhub.ai/openstatus/incident-communication-playbook) <br>
- [README](artifact/README.md) <br>
- [Skill bundle manifest](artifact/skills.md) <br>
- [Incident communication examples](artifact/skills/incident-communication/references/examples.md) <br>
- [Incident communication framework](artifact/skills/incident-communication/references/framework.md) <br>
- [Maintenance examples](artifact/skills/maintenance/references/examples.md) <br>
- [Maintenance framework](artifact/skills/maintenance/references/framework.md) <br>
- [Postmortem examples](artifact/skills/postmortem/references/examples.md) <br>
- [Postmortem framework](artifact/skills/postmortem/references/framework.md) <br>
- [Status page context examples](artifact/skills/status-page-context/references/examples.md) <br>
- [Status page context framework](artifact/skills/status-page-context/references/framework.md) <br>
- [Status report examples](artifact/skills/status-report/references/examples.md) <br>
- [Status report framework](artifact/skills/status-report/references/framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown drafts, templates, checklists, and status page context guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update .agents/status-page-context.md when the user configures reusable status page context.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and skills.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
