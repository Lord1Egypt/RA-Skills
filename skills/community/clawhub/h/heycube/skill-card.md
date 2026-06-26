## Description: <br>
Guides OpenClaw users through setting up HeyCube's personal profile memory service, including API-key configuration, local SQLite storage, and helper skills for retrieving and updating profile data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MMMMMMTL](https://clawhub.ai/user/MMMMMMTL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to install a HeyCube memory workflow that stores structured profile data locally and loads or updates it through explicit phrase-triggered helper skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local profile data may contain sensitive personal information. <br>
Mitigation: Avoid storing highly sensitive details, periodically review the SQLite profile data, and remove the helper skills or create .heycube-off when the memory workflow is no longer wanted. <br>
Risk: HeyCube API calls use an API key and send redacted conversation summaries to the HeyCube service. <br>
Mitigation: Use a revocable API key through HEYCUBE_API_KEY and ensure summaries remain redacted before API calls. <br>
Risk: Setup copies helper skills and scripts into the user's workspace and agent skill directory. <br>
Mitigation: Review the proposed file copies, TOOLS.md changes, and npm dependency installation before executing each setup step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MMMMMMTL/heycube) <br>
- [HeyCube service](https://heifangti.com) <br>
- [HeyCube API endpoint](https://heifangti.com/api/api/v1/heifangti/agent/analyze) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown instructions with inline shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation for setup steps; helper behavior uses redacted summaries, a revocable API key, and local SQLite profile data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
