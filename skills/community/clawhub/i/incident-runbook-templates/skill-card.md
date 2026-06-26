## Description: <br>
Provides incident response runbook templates for detection, triage, mitigation, resolution, communication, escalation, on-call onboarding, and post-incident review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, platform engineers, and incident responders use this skill to create service-specific incident response procedures, escalation paths, recovery steps, and communication templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example rollback, scaling, database termination, network policy, and feature-flag commands could affect production systems if copied without adaptation. <br>
Mitigation: Treat generated runbooks as templates; replace placeholders, confirm the target service and blast radius, and require incident commander or DBA approval before executing high-impact steps. <br>
Risk: Generic incident procedures may omit local approval, verification, monitoring, or communication requirements. <br>
Mitigation: Add organization-specific approval gates, dashboards, escalation contacts, and post-change verification checks before adopting a runbook. <br>


## Reference(s): <br>
- [Google SRE Book - Incident Management](https://sre.google/sre-book/managing-incidents/) <br>
- [PagerDuty Incident Response](https://response.pagerduty.com/) <br>
- [Atlassian Incident Management](https://www.atlassian.com/incident-management) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell, SQL, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are templates and procedural guidance that should be adapted to the target service before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
