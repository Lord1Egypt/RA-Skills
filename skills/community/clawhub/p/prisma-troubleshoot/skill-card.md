## Description: <br>
Troubleshoot Prisma Access issues including GlobalProtect connectivity, policy matching, tunnel status, SCM API errors, and configuration push failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leesandao](https://clawhub.ai/user/leesandao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network security engineers and Prisma Access administrators use this skill to diagnose connectivity, policy, tunnel, API, and configuration push issues in Strata Cloud Manager workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated SCM API examples may affect Prisma Access configuration if executed without review. <br>
Mitigation: Review the HTTP method, tenant, folder, payload, and job status before running or approving commands. <br>
Risk: SCM credentials and tenant identifiers are required for authenticated troubleshooting. <br>
Mitigation: Provide SCM_CLIENT_ID, SCM_CLIENT_SECRET, and SCM_TSG_ID through protected environment variables and avoid pasting secrets into prompts, logs, or generated reports. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/leesandao/prismaaccess-skill) <br>
- [ClawHub skill page](https://clawhub.ai/leesandao/prisma-troubleshoot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline HTTP and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference SCM_CLIENT_ID, SCM_CLIENT_SECRET, SCM_TSG_ID, and curl for authenticated Strata Cloud Manager troubleshooting.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
