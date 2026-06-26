## Description: <br>
Incident Fupan guides agents through evidence-based incident postmortems, root-cause analysis, impact assessment, prevention rules, and action items for production failures, outages, bugs, near-misses, and consequential agent mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scytheshan-pixel](https://clawhub.ai/user/scytheshan-pixel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and incident responders use this skill to turn production incidents, outages, near-misses, and agent mistakes into sourced postmortem reports with timelines, 5 Whys analysis, quantified impact, prevention rules, and action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to inspect logs, repository history, service status, configs, and related data that may contain secrets, customer data, internal topology, or sensitive operational details. <br>
Mitigation: Redact sensitive data from evidence and saved reports, and limit incident artifacts to the minimum information needed for review. <br>
Risk: The skill can store incident lessons in long-term memory or update AGENTS.md, TOOLS.md, or related skill files, which may alter future agent behavior. <br>
Mitigation: Require explicit user approval before long-term memory entries or edits to persistent agent guidance. <br>


## Reference(s): <br>
- [Incident Fupan ClawHub page](https://clawhub.ai/scytheshan-pixel/incident-fupan) <br>
- [Publisher profile](https://clawhub.ai/user/scytheshan-pixel) <br>
- [Incident-to-Rule Pattern Library](references/patterns.md) <br>
- [Postmortem Report Template](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown incident report with sourced timeline entries, root-cause analysis, impact tables, prevention rules, and action items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a postmortem report under ~/incidents/ and may propose updates to long-term rules or local agent guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
