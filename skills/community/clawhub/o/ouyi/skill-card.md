## Description:

Ouyi API Tool uses a local Node.js script to send user prompts to the Ouyi chat completions API and return conversation analysis results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlsjzj](https://clawhub.ai/user/dlsjzj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to route chat-style questions through the Ouyi API for bilingual analysis and reasoning tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent to a third-party Ouyi API without a clear opt-in or sensitivity check.

Mitigation: Require explicit user confirmation before sending prompts and avoid secrets, personal data, regulated data, or proprietary code unless the provider is trusted and approved.

Risk: API credentials could be mishandled if operators edit the script directly instead of using environment configuration.

Mitigation: Set OUYI_API_KEY through the runtime environment and keep hard-coded placeholders out of deployed configurations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlsjzj/skills/ouyi)
- [Ouyi chat completions endpoint](https://api.rcouyi.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON response consumed and summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns content, reasoning token count, model, and error fields from the API wrapper.]

## Skill Version(s):

1.0.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
