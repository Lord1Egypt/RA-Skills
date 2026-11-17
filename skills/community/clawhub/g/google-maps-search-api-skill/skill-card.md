## Description:

This skill helps agents run BrowserAct's Google Maps Search API workflow to extract structured business listings from Google Maps search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to collect local business listings for market research, lead generation, competitor mapping, and CRM or database export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and workflow data are sent to BrowserAct during execution.

Mitigation: Use the skill only for workflows where sending that data to BrowserAct is acceptable under the user's or organization's policies.

Risk: The skill requires a reusable BrowserAct API key and may prompt users to provide it.

Mitigation: Configure BROWSERACT_API_KEY through an environment variable or approved secret manager, not by pasting the key into chat.

Risk: Lead generation and CRM export workflows can collect business or contact data at broad scope.

Mitigation: Confirm that collection and use of the data complies with applicable laws, platform terms, and organizational policies before running those workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/google-maps-search-api-skill)
- [BrowserAct Console](https://www.browseract.com/reception/integrations)
- [BrowserAct Workflow API endpoint](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and plain-text or JSON-like API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BROWSERACT_API_KEY; outputs status logs while polling and structured Google Maps business result fields when available.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
