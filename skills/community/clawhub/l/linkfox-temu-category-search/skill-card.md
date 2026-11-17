## Description:

Searches locally synchronized Temu category data by keyword to find Chinese names, English names, and category IDs for product and shop filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to locate Temu category IDs after category data has been synchronized locally. The IDs can then be used as category filters in Temu product or shop queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes remote authenticated calls to LinkFox-hosted services and handles API keys.

Mitigation: Install and run it only in trusted environments, keep LINKFOX_AGENT_API_KEY and LINKFOXAGENT_API_KEY out of untrusted shells or workspaces, and review endpoint environment variables before use.

Risk: The onboarding flow can ask users to provide phone numbers, SMS codes, and billing or payment choices.

Mitigation: Use onboarding only when account setup or billing support is expected, and provide those values only when the publisher and runtime environment are trusted.

Risk: Search results depend on Temu category data that has already been synchronized into the local data store.

Mitigation: Synchronize Temu category data before relying on returned category IDs, and treat empty results as possibly caused by missing or stale synchronization.

## Reference(s):

- [Temu category search API reference](references/api.md)
- [Authentication and billing onboarding guide](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-category-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command output and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Category search responses may be saved as JSON files, summarized for large payloads, and cached for repeated parameter sets.]

## Skill Version(s):

1.0.9 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
