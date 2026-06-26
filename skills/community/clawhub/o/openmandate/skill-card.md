## Description: <br>
OpenMandate helps agents post mandates, answer intake questions, review matches, and integrate with OpenMandate through MCP tools, SDKs, or a bundled shell helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsh3khar](https://clawhub.ai/user/rsh3khar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage OpenMandate contacts, create and complete mandate intake, review matches, respond to matches, report outcomes, and integrate OpenMandate into agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can make consequential OpenMandate account and matching changes, including deleting contacts, closing mandates, accepting matches, and submitting final outcomes. <br>
Mitigation: Require explicit user confirmation before each consequential action and show the exact contact, mandate, or match ID plus the consequence before proceeding. <br>
Risk: The skill requires an OpenMandate API key and can act on the user's OpenMandate account. <br>
Mitigation: Use only when account-level OpenMandate actions are intended, keep OPENMANDATE_API_KEY out of prompts and logs, and prefer the narrowest practical operational context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rsh3khar/openmandate) <br>
- [OpenMandate Homepage](https://openmandate.ai) <br>
- [API Reference](references/api-reference.md) <br>
- [Intake Workflow](references/intake-workflow.md) <br>
- [Matching](references/matching.md) <br>
- [SDK Reference](references/sdks.md) <br>
- [MCP Setup Guide](https://github.com/openmandate/skills#mcp-setup) <br>
- [OpenMandate API](https://api.openmandate.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and API or SDK usage patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENMANDATE_API_KEY; OPENMANDATE_BASE_URL is optional for overriding the API base URL.] <br>

## Skill Version(s): <br>
0.6.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
