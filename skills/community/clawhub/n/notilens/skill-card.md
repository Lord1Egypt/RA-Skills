## Description: <br>
Send real-time alerts to NotiLens from any script, app, or AI agent for task lifecycle events, errors, completions, metric tracking, and custom alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notilens](https://clawhub.ai/user/notilens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send structured NotiLens notifications from scripts, applications, and agents so task starts, progress, errors, human-input requests, completions, and metrics are visible in real time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification payloads may send secrets, personal data, internal hostnames, stack traces, approval links, or sensitive report URLs to an external webhook. <br>
Mitigation: Only include information intended to leave the local environment, keep NOTILENS_SECRET private, and ensure any linked resources are access-controlled. <br>
Risk: Frequent progress notifications can create noisy alert streams. <br>
Mitigation: Use terminal events consistently and avoid sending progress events more often than needed for operational visibility. <br>


## Reference(s): <br>
- [NotiLens homepage](https://www.notilens.com) <br>
- [NotiLens ClawHub skill page](https://clawhub.ai/notilens/notilens) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON payload examples and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTILENS_TOKEN, NOTILENS_SECRET, and curl to send webhook notifications.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
