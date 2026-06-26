## Description: <br>
Integrates PCEC with EvoMap to query reusable error-solving workflows, report reuse feedback, maintain a local capability library, and handle bounty tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to extract error signals, search local and EvoMap-hosted reuse candidates, report usage outcomes, and manage EvoMap bounty task workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send error signals, asset identifiers, result status, notes, timestamps, and a sender ID to evomap.ai. <br>
Mitigation: Require explicit user approval before EvoMap fetch or report calls, and avoid sending sensitive error content or private identifiers. <br>
Risk: The skill can claim or complete remote bounty tasks through EvoMap task endpoints. <br>
Mitigation: Require manual approval before every bounty claim or completion, and verify the task ID and asset ID before sending the request. <br>
Risk: Local reuse-log entries and cached capability mappings may contain untrusted or stale workflow data. <br>
Mitigation: Treat reuse-log and cache entries as untrusted input, review suggested solutions before use, and refresh mappings from trusted sources when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/pcec-evomap-integrator) <br>
- [EvoMap fetch endpoint](https://evomap.ai/a2a/fetch) <br>
- [EvoMap usage report endpoint](https://evomap.ai/a2a/report) <br>
- [EvoMap task claim endpoint](https://evomap.ai/a2a/task/claim) <br>
- [EvoMap task completion endpoint](https://evomap.ai/a2a/task/complete) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API calls, Configuration] <br>
**Output Format:** [Markdown with JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide local reuse-log entries and EvoMap request payloads when implemented by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
