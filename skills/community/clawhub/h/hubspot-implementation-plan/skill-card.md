## Description: <br>
Generate a phased implementation plan from a HubSpot audit report. Creates prioritized, sequenced cleanup processes with effort estimates, dependencies, and automation feasibility. Use after running /hubspot-audit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HubSpot administrators, CRM operators, and implementation consultants use this skill after a HubSpot audit to turn findings into a sequenced cleanup and optimization roadmap with dependencies, effort estimates, and automation feasibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cleanup recommendations may lead to contact deletion, suppression, reassignment, or other CRM changes if followed without review. <br>
Mitigation: Verify the audit findings first, export or back up affected HubSpot data, and review each cleanup task before execution. <br>
Risk: Optional custom skill creation and contribution steps may create files, commits, pushes, or pull requests. <br>
Mitigation: Review generated skill files, commits, and pull request content before approving repository or publication actions. <br>
Risk: Hybrid HubSpot automation steps can be misconfigured because some CRM changes require manual workflows or UI-only setup. <br>
Mitigation: Build required workflows in the HubSpot UI, verify triggers and actions manually, and confirm workflow behavior before running related scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomgranot/hubspot-implementation-plan) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, code, shell commands] <br>
**Output Format:** [Markdown implementation plan saved as reports/implementation-plan-{YYYY-MM-DD}.md, with optional skill files and contribution commands when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the most recent reports/hubspot-audit-*.md as input and should include only tasks supported by the audit findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; SKILL.md metadata lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
