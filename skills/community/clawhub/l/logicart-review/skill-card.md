## Description: <br>
AI-powered code analysis via LogicArt that helps find bugs, security issues, code-quality concerns, and logic flow details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JPaulGrayson](https://clawhub.ai/user/JPaulGrayson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to send selected code snippets or files to LogicArt for code review, bug finding, security issue detection, complexity scoring, suggestions, and logic-flow analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected code or file contents are uploaded to LogicArt for analysis. <br>
Mitigation: Use the skill only for code that is approved for sharing with LogicArt, and avoid submitting secrets, private keys, credentials, regulated data, or proprietary code unless authorization is explicit. <br>
Risk: Automated review findings may be incomplete, incorrect, or misleading. <br>
Mitigation: Treat LogicArt results as review assistance and have a qualified developer verify critical bug, security, complexity, and logic-flow findings before making changes. <br>


## Reference(s): <br>
- [LogicArt Code Review on ClawHub](https://clawhub.ai/JPaulGrayson/logicart-review) <br>
- [LogicArt](https://logic.art) <br>
- [LogicArt Agent Analyze API](https://logic.art/api/agent/analyze) <br>
- [Validate Repo](https://validate-repo.replit.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [JSON analysis responses from LogicArt, presented to users as prioritized markdown review findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script accepts inline code or a local file path and posts the selected contents to LogicArt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
