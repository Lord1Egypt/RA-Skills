## Description: <br>
Programmatic NotebookLM control with auto-recovery for authentication errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antaripnandi](https://clawhub.ai/user/antaripnandi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to control NotebookLM from an agent and recover from expired authentication after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill extracts live Google/NotebookLM session cookies and stores them locally for reuse. <br>
Mitigation: Install only when deliberately accepting this behavior, prefer official login flows where possible, and treat the stored files and environment variable as sensitive secrets. <br>
Risk: Authentication recovery can refresh and inject cookies after a NotebookLM authentication failure. <br>
Mitigation: Run the recovery script only after explicit user approval and review the proposed command before execution. <br>
Risk: Stored auth files or NOTEBOOKLM_AUTH_JSON can expose account sessions if shared or retained longer than needed. <br>
Mitigation: Restrict access to ~/.notebooklm/storage_state.json, ~/.notebooklm/auth_payload.json, and NOTEBOOKLM_AUTH_JSON, and remove them when finished. <br>


## Reference(s): <br>
- [OpenClaw Framework](https://github.com/openclaw/openclaw) <br>
- [NotebookLM](https://notebooklm.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a user-consent gate before running cookie recovery automation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
