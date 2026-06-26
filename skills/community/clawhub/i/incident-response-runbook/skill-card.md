## Description: <br>
Create, maintain, and use incident response runbooks for production outages, including triage, stakeholder communication, and post-incident review support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and incident responders use this skill to create runbook templates, guide outage triage, draft incident communications, and produce post-incident reviews for production systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested diagnostic commands or incident communications could be incorrect or unsuitable during an active outage. <br>
Mitigation: Review commands, status updates, and stakeholder messages before using them in production incident response. <br>
Risk: Incident descriptions, timelines, and historical outage details can contain sensitive operational information. <br>
Mitigation: Share only incident context the operator is comfortable having the agent process, and redact secrets or sensitive customer-impact details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/incident-response-runbook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown runbooks, response prompts, communication drafts, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included local script can print a Markdown runbook or write it to a user-specified output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
