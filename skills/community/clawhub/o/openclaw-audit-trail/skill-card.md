## Description: <br>
The Immutable Black Box for AI Decisions - Track, audit, and verify AI agent decisions with cryptographic guarantees <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI teams use this skill to record, verify, query, and export local audit trails for AI agent decisions, including prompts, context, reasoning, outputs, execution time, and cost. It supports compliance review, debugging, incident investigation, and transparency workflows through CLI and TypeScript/JavaScript interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit logs and exports can contain sensitive prompts, context, reasoning, decisions, personal data, or cost information. <br>
Mitigation: Use a protected storage path, avoid logging secrets or unnecessary personal data, review exports before sharing, and keep generated audit records under appropriate access controls. <br>
Risk: Global or shared installation can make it harder to control the exact package source used by an agent workflow. <br>
Mitigation: Prefer a pinned or project-local npm install after reviewing the package source for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/ZhenStaff/openclaw-audit-trail) <br>
- [Project homepage](https://github.com/ZhenRobotics/openclaw-audit-trail) <br>
- [Project documentation](https://github.com/ZhenRobotics/openclaw-audit-trail#readme) <br>
- [NPM package](https://www.npmjs.com/package/openclaw-audit-trail) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown with bash, TypeScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audit records and exports in JSON, CSV, HTML, or Markdown formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
