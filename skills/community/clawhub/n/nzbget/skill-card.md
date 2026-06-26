## Description: <br>
Check NZBGet download status and queue information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aricus](https://clawhub.ai/user/aricus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to check a configured NZBGet instance for active download counts, current speed, queue contents, and concise status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses NZBGET_USER, NZBGET_PASS, and NZBGET_HOST to query NZBGet, so credentials and host configuration affect exposure. <br>
Mitigation: Install only in trusted environments, prefer localhost or a trusted private network for NZBGET_HOST, and avoid exposing NZBGet over untrusted networks. <br>
Risk: The helper script builds an HTTP JSON-RPC URL containing credentials for the configured NZBGet endpoint. <br>
Mitigation: Use HTTPS or a safer curl authentication pattern if supported by the NZBGet setup, and keep secrets in environment variables rather than prompts or chat text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aricus/nzbget) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queue listings are capped at 10 items to keep responses concise.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
