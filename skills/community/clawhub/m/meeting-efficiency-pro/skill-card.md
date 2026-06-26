## Description: <br>
Meeting Efficiency Pro analyzes calendar events and meeting notes to score meeting efficiency, suggest optimizations, extract action items, and generate follow-up and reporting outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JacealLLC](https://clawhub.ai/user/JacealLLC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and productivity-focused teams use this skill to review meeting schedules and notes, identify inefficient meetings, extract action items, and generate briefings or weekly reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says secrets may be stored and printed in plaintext configuration. <br>
Mitigation: Move AI, task-manager, calendar, and email credentials out of plaintext config and redact configuration output before using real credentials. <br>
Risk: The security evidence says mock calendar and reporting results may be presented as real integrations. <br>
Mitigation: Treat outputs as demo-quality until integrations are verified against live providers and mock-data behavior is clearly documented. <br>
Risk: Meeting notes can contain confidential business or personal information. <br>
Mitigation: Avoid processing confidential notes until privacy handling, export storage, and retention behavior are reviewed and documented. <br>


## Reference(s): <br>
- [Meeting Efficiency Pro API Documentation](references/api-docs.md) <br>
- [Meeting Efficiency Pro ClawHub Listing](https://clawhub.ai/JacealLLC/meeting-efficiency-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, Markdown-style reports, JSON or CSV exports, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Calendar, task-manager, email, and AI-provider features depend on user-supplied configuration and credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
