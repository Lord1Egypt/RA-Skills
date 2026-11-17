## Description:

Use when an agent needs to read or contribute to the Open Agent Guide public catalog of AI-native organizations, products, models, MCP servers, agent skills, and integrations. Covers signup, API token storage, the v1 read endpoints, and submitting catalog edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[open-agent-guide](https://clawhub.ai/user/open-agent-guide)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to find and compare entries in the public Open Agent Guide catalog, inspect documented product capabilities, and submit evidence-backed catalog changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The signup example can expose an API token in logs or a temporary response file.

Mitigation: Capture the token directly into a secret store, suppress credential output, remove temporary responses, and rotate any token already exposed.

Risk: Authenticated contributions and preserved journals may contain sensitive information or be sent to an unintended API destination.

Mitigation: Submit only information intended for public publication, verify the API destination, and protect submit/watch journals.

## Reference(s):

- [Open Agent Guide](https://www.openagentguide.com)
- [Open Agent Guide OpenAPI specification](https://www.openagentguide.com/api/v1/openapi.json)
- [Open Agent Guide consultation guidance](https://www.openagentguide.com/integrations/SKILL.md)
- [Open Agent Guide setup guide](https://www.openagentguide.com/integrations/guide.md)
- [API reference](references/api-reference.md)
- [Onboarding and token lifecycle](references/onboarding.md)
- [CLI guide](references/cli.md)
- [Contribution guidance](references/contributing.md)
- [Batch contribution guide](references/batch-populating.md)
- [Portability evidence guide](references/portability.md)
- [Pricing evidence guide](references/pricing-evidence.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, API calls, Shell commands, Configuration instructions, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API requests or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Catalog reads are anonymous; authenticated endpoints use OAG_TOKEN. Contributions are prepared for a public catalog.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
