## Description:

Manage Higress AI Gateway resources through its Console API, including consumers, routes, AI providers, and MCP server-related settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montycn](https://clawhub.ai/user/montycn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and gateway operators use this skill to administer a trusted Higress AI Gateway manager environment by creating, updating, listing, and deleting consumers, AI routes, and LLM providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses administrator credentials, session cookies, generated consumer keys, provider tokens, and related gateway secrets.

Mitigation: Install and run it only in a trusted Higress manager environment; do not paste, print, commit, or log those secrets.

Risk: Update and delete operations can change or remove live gateway consumers, routes, and providers.

Mitigation: Confirm the exact resource name, inspect or export the current object first, and use the documented GET-modify-PUT flow with version fields where required.

Risk: Route and provider changes can interrupt or misroute live AI gateway traffic.

Mitigation: Review route predicates, domains, upstreams, and allowed consumers before applying changes, then allow for the documented auth plugin activation delay.

## Reference(s):

- [Higress Console OpenAPI Reference](artifact/references/higress-api-doc.json)
- [Higress Console Repository](https://github.com/higress-group/higress-console)
- [ClawHub Skill Release Page](https://clawhub.ai/montycn/skills/higress-gateway-management)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and operational guidance for authenticated local Higress Console API workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
