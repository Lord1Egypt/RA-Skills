## Description:

Routes tasks that need human judgment, local knowledge, or cultural context to verified Loopuman workers for verification, translation, moderation, image labeling, data collection, quality assurance, surveys, and opinion tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seesayearn-boop](https://clawhub.ai/user/seesayearn-boop)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill when a task needs human verification, perception, cultural judgment, local knowledge, translation, labeling, moderation, or subjective review instead of AI-only processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task instructions and referenced material may be sent to Loopuman and human workers.

Mitigation: Do not submit secrets, credentials, private customer data, regulated data, or confidential internal documents.

Risk: Create and cancel commands can spend balance or change paid task state.

Mitigation: Manually review task descriptions, budgets, worker counts, and cancellation requests before running commands.

Risk: The API key is forwarded by the shell script and may be exposed if stored loosely or sent to an untrusted endpoint.

Mitigation: Store the API key with restrictive file permissions and avoid custom apiUrl values unless the endpoint is fully trusted.

## Reference(s):

- [Loopuman API Reference](references/api-reference.md)
- [Loopuman Website](https://loopuman.com)
- [Loopuman ERC-8004 Agent](https://www.8004scan.io/agents/celo/17)
- [Loopuman MCP Manifest](https://api.loopuman.com/.well-known/mcp.json)
- [Loopuman A2A Agent Card](https://api.loopuman.com/.well-known/agent-card.json)
- [ClawHub Skill Listing](https://clawhub.ai/seesayearn-boop/skills/loopuman)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; task creation, cancellation, and polling call the Loopuman API.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
