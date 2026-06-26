## Description: <br>
Complete Magento 2 store administration via SSH key authentication, REST API, GraphQL, and direct database access for server owners on their own infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nj070574-gif](https://clawhub.ai/user/nj070574-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Magento store owners and administrators use this skill to inspect, maintain, and operate their own Magento 2 infrastructure through SSH, Magento CLI commands, REST and GraphQL calls, and database queries. It is intended for owner-operated environments where the user can review privileged actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad production-store access through SSH, database credentials, Magento admin credentials, and privileged service commands. <br>
Mitigation: Install only for Magento servers the user owns and administers, and use dedicated least-privilege SSH, database, and Magento admin accounts. <br>
Risk: Destructive or business-impacting actions include refunds, deletes, restores, service restarts, Composer changes, Redis flushes, and database writes. <br>
Mitigation: Keep production use non-autonomous and require explicit confirmation before any write, refund, restore, restart, Composer, Redis flush, or database delete action. <br>
Risk: Incomplete guardrails around substituted command inputs can make malformed or unsafe commands possible. <br>
Mitigation: Validate or quote every substituted value before execution and review generated commands before running them. <br>
Risk: Operational queries can expose customer or administrator personal data. <br>
Mitigation: Redact personal data unless full details are explicitly needed for the administrative task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nj070574-gif/magento-admin) <br>
- [Publisher profile](https://clawhub.ai/user/nj070574-gif) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration variables, SQL queries, REST calls, and GraphQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are operational instructions for user-owned Magento infrastructure and may include commands that require explicit review before execution.] <br>

## Skill Version(s): <br>
5.6.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
