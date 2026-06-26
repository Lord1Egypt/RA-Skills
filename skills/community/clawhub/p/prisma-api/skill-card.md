## Description: <br>
Interact with the Strata Cloud Manager API to manage Prisma Access configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leesandao](https://clawhub.ai/user/leesandao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and network engineers use this skill to authenticate to Strata Cloud Manager and query, create, update, delete, or push Prisma Access configuration objects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Prisma Access tenant configuration when SCM credentials are provided. <br>
Mitigation: Use least-privilege SCM credentials, start with test or non-production tenants, and review planned create, update, delete, and push actions before execution. <br>
Risk: OAuth client secrets, bearer tokens, or Authorization headers could be exposed in logs or transcripts. <br>
Mitigation: Avoid logging secrets or bearer tokens, keep credentials in environment variables, and redact Authorization headers from shared output. <br>
Risk: Bulk API operations may hit rate limits or apply unintended changes across many resources. <br>
Mitigation: Use dry-run planning where possible, paginate deliberately, add delays for bulk operations, and keep an audit log of API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leesandao/prisma-api) <br>
- [Project homepage](https://github.com/leesandao/prismaaccess-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCM_CLIENT_ID, SCM_CLIENT_SECRET, SCM_TSG_ID, curl, and jq.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
