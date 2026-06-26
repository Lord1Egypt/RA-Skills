## Description: <br>
Migrate Prisma Access configurations between SCM tenants, including security policies, NAT rules, address objects, and compatibility handling based on real-world migration testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leesandao](https://clawhub.ai/user/leesandao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to plan and execute Prisma Access tenant-to-tenant migrations via the Strata Cloud Manager API while handling dependency order, conflicts, validation, and user-confirmed commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change security configuration in a target Prisma Access tenant. <br>
Mitigation: Use least-privilege service accounts, verify source and destination tenant IDs, review planned imports or overwrite decisions, and test in a non-production tenant when possible. <br>
Risk: Running configuration could be committed before the candidate state is fully reviewed. <br>
Mitigation: Validate the candidate configuration first and require explicit user confirmation before pushing to running configuration. <br>
Risk: Missing permissions or unavailable referenced profiles can cause incomplete migrations or broken references. <br>
Mitigation: Check service-account permissions, detect conflicts across all folders, strip only known invalid references when needed, and manually restore inaccessible profile references after target-side creation. <br>


## Reference(s): <br>
- [Migration workflow reference](reference/migration-workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/leesandao/prisma-migrate) <br>
- [Project homepage](https://github.com/leesandao/prismaaccess-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API request examples, and configuration checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCM OAuth credentials plus curl and jq; emphasizes dry-run review and explicit confirmation before committing running configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
