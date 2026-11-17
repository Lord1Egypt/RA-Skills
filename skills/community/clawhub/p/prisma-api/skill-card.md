## Description:

Interact with the Strata Cloud Manager (SCM) API to authenticate, query, create, update, delete, and push Prisma Access configuration objects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leesandao](https://clawhub.ai/user/leesandao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security administrators use this skill to automate Prisma Access configuration operations and inspect live tenant state through Strata Cloud Manager APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, delete, and push Prisma Access security configuration.

Mitigation: Require explicit human review, backup or rollback planning, and confirmation before mutating operations or candidate pushes.

Risk: SCM client secrets or bearer tokens could be exposed through logs or command output.

Mitigation: Use least-privileged or test credentials and avoid printing secrets or bearer tokens.

Risk: Live tenant API calls may affect production configuration.

Mitigation: Prefer test tenants when validating changes and confirm the target folder, resource, and object ID before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leesandao/skills/prisma-api)
- [Declared project homepage](https://github.com/leesandao/prismaaccess-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl commands, JSON snippets, and API-response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCM credentials in environment variables; output may include proposed configuration changes and live API responses.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
