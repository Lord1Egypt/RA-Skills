## Description: <br>
Automatically cleans up inactive sessions older than one hour and sends a notification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[artwebs](https://clawhub.ai/user/artwebs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to periodically identify inactive sessions, notify the target channel, save a session summary, and terminate stale sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can terminate inactive sessions automatically. <br>
Mitigation: Use only after confirming the cleanup policy, timeout, and target environment; add dry-run, exclusions, or approval gates before production deployment. <br>
Risk: The skill reads session content and stores conversation-derived summaries locally. <br>
Mitigation: Disclose this behavior to users, store summaries only in approved locations, and define retention and deletion controls before enabling the job. <br>
Risk: The storage path and inactivity threshold are fixed in the bundled script. <br>
Mitigation: Make the summary path and timeout configurable so operators can align them with local policy and access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/artwebs/lite-session-cleaner) <br>
- [Publisher profile](https://clawhub.ai/user/artwebs) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Text status messages and notifications, with local JSON files for saved session summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the openclaw CLI; the bundled script defaults to a 3600-second inactivity threshold and writes summaries under the lite-session-cleaner summaries directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
