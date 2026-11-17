## Description:

Search and hire real humans for tasks -- photography, delivery, research, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[human-pages-ai](https://clawhub.ai/user/human-pages-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agents use this skill to search for people, inspect public or full profiles when authorized, register an agent, create job offers, record USDC payments, manage payment streams, and leave reviews for completed work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts an unpinned external MCP package through npx.

Mitigation: Use a pinned, reviewed version of the Human Pages MCP server before deployment.

Risk: The skill can access full profiles and payment-related workflows.

Mitigation: Run it with only the required environment variables and require clear user approval before fetching full profiles, creating job offers, sending or recording payments, starting streams, or leaving reviews.

Risk: Agent API keys and webhook secrets are sensitive and may not be recoverable after registration.

Mitigation: Store returned credentials securely and avoid exposing them in prompts, logs, or shared workspace files.

## Reference(s):

- [Human Pages](https://humanpages.ai)
- [ClawHub Skill Listing](https://clawhub.ai/human-pages-ai/skills/humanpages)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Text or Markdown guidance with inline shell commands and MCP tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and the HUMANPAGES_AGENT_KEY environment variable for authenticated workflows.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
