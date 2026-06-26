## Description: <br>
Shared web task memory for AI agents that queries community workflow knowledge before browsing and reports execution traces after tasks to improve shared navigation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yourens](https://clawhub.ai/user/Yourens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use NaviMem to plan browser automation tasks with community workflow memory, query for page actions when stuck, and report completed workflow traces for future reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser task descriptions and workflow traces may be sent to a third-party shared service. <br>
Mitigation: Use the skill for public, low-sensitivity browsing workflows and avoid logged-in accounts, internal URLs, credentials, personal data, financial, health, legal, or confidential work. <br>
Risk: Workflow traces may contain sensitive details if collected from real browsing sessions. <br>
Mitigation: Review and redact traces before reporting them to NaviMem, especially when using exported browser recordings. <br>
Risk: Plans returned from shared workflow memory may be stale or not match the current website. <br>
Mitigation: Treat returned plans as guidance, verify each step against the live page, and fall back to normal exploration when the page differs. <br>


## Reference(s): <br>
- [NaviMem ClawHub Release](https://clawhub.ai/Yourens/navimem) <br>
- [NaviMem API Base URL](https://i.ariseos.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with bash commands and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an optional NAVIMEM_BASE_URL environment variable; default service endpoint is https://i.ariseos.com.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
