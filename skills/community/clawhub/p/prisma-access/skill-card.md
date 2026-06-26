## Description: <br>
All-in-one Prisma Access management for Strata Cloud Manager (SCM). Generate configurations, audit against best practices, migrate between tenants, troubleshoot issues, and automate via SCM API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leesandao](https://clawhub.ai/user/leesandao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network security engineers and administrators use this skill to generate, audit, migrate, troubleshoot, and automate Prisma Access configuration through Strata Cloud Manager APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage live security configuration and includes deletion and push operations. <br>
Mitigation: Use credentials scoped to the minimum required folders and resources, and require explicit review of tenant, folder, resource type, immutable object ID, and planned effect before any delete or configuration push. <br>
Risk: The security summary notes insufficient visible guardrails around destructive actions. <br>
Mitigation: Prefer dry-run or read-only use until explicit destructive-action safeguards are documented and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leesandao/prisma-access) <br>
- [Skill homepage](https://github.com/leesandao/prismaaccess-skill) <br>
- [Strata Cloud Manager API base URL](https://api.sase.paloaltonetworks.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SCM API endpoints, folder parameters, audit findings, migration plans, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
