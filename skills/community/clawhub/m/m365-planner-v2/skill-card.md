## Description: <br>
M365 Planner helps agents manage Microsoft 365 Planner plans, buckets, and tasks through Microsoft Graph, including group-based plan management, task assignment, progress tracking, and recurring-task guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felox63](https://clawhub.ai/user/felox63) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, administrators, and developers use this skill to create, list, assign, update, and delete Microsoft 365 Planner resources from an agent workflow. It is most useful for tenant-scoped Planner automation where Microsoft Graph app credentials and administrator consent are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Microsoft 365 app credentials can grant broad access to Planner and related group data. <br>
Mitigation: Have a Microsoft 365 administrator review the Graph permissions, use the least-privilege scopes that work, and protect and rotate the client secret. <br>
Risk: Cleanup and delete commands can change or remove live Planner tasks. <br>
Mitigation: Verify the tenant, group, plan, bucket, and task targets before running destructive commands. <br>


## Reference(s): <br>
- [Planner API Overview](references/planner-api.md) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Common Patterns](references/common-patterns.md) <br>
- [Microsoft Graph API Docs](https://docs.microsoft.com/en-us/graph/api/overview) <br>
- [Planner REST API Reference](https://docs.microsoft.com/en-us/graph/api/resources/planner-overview) <br>
- [ClawHub Skill Page](https://clawhub.ai/felox63/m365-planner-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JavaScript examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Node.js helper scripts that call Microsoft Graph when credentials and tenant targets are configured.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release evidence, SKILL.md frontmatter, package.json, CHANGELOG released 2026-04-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
