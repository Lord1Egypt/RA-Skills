## Description: <br>
Helps agents browse MongoDB Atlas administration API categories, inspect endpoint details and schemas, and prepare or execute Atlas management API calls with dry-run support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect MongoDB Atlas management API endpoints, review request and response schemas, and run dry-run or approved administrative API calls for cloud database resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad live MongoDB Atlas administrative API actions using credentials. <br>
Mitigation: Use least-privileged Atlas API credentials, restrict use to known projects, run dry-runs first, and require explicit human approval before any live --yes operation. <br>
Risk: The inspected artifact does not include the scripts referenced by the skill instructions. <br>
Mitigation: Confirm the referenced scripts are present and reviewed before relying on the skill for live API operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/mongodb-atlas-admin-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe dry-run checks, endpoint details, schema fields, credential configuration, and API call results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
