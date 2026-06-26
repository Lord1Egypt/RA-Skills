## Description: <br>
Build and run help centers with provider selection, migration playbooks, workflow mapping, content taxonomy, and support deflection metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Support, operations, and documentation teams use this skill to plan new help centers, migrate existing help content, compare vendor and custom-stack options, and connect self-service content to support workflows and metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local planning files may contain support strategy, operational constraints, or customer-related context if the user records them. <br>
Mitigation: Avoid storing secrets or sensitive customer data in ~/help-center/ planning files, consistent with the security guidance. <br>
Risk: Automatic activation could cause ordinary support-documentation discussions to trigger help-center planning behavior. <br>
Mitigation: Choose explicit activation during setup when the user does not want normal support-docs conversations to invoke the skill. <br>
Risk: Provider, migration, or launch recommendations could affect customer-facing support operations if applied without review. <br>
Mitigation: Require user approval before creating or modifying local planning files, provider production content, redirects, or rollout steps. <br>


## Reference(s): <br>
- [Help Center on ClawHub](https://clawhub.ai/ivangdavila/help-center) <br>
- [Help Center Homepage](https://clawic.com/skills/help-center) <br>
- [Setup](artifact/setup.md) <br>
- [Provider Matrix](artifact/provider-matrix.md) <br>
- [Build Your Own Stack](artifact/build-own-stack.md) <br>
- [Migration Playbook](artifact/migration-playbook.md) <br>
- [Content Operations](artifact/content-ops.md) <br>
- [Launch Checklist](artifact/launch-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, planning checklists, scoring tables, and local planning-file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local planning files under ~/help-center/ after user confirmation; no executable code or default external data sharing is included.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
