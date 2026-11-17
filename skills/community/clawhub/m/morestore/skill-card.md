## Description:

Access the MoreStore A2A marketplace to sign up or log in, create buyer and seller campaigns, generate product photos, find matches, analyze brands, and manage B2B pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyler-odenthal](https://clawhub.ai/user/tyler-odenthal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to onboard to MoreStore, create and manage buyer or seller marketplace campaigns, analyze brands and matches, send campaign messages, and generate product marketing images through MoreStore APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a MoreStore account password and reusable API key for authenticated actions.

Mitigation: Prefer session-only API key use unless ongoing access is needed, avoid printing secrets, and remove or rotate the key after use.

Risk: The skill can create persistent marketplace campaigns, update prospect statuses, and send campaign messages.

Mitigation: Use explicit user confirmation gates before saving credentials, creating campaigns, changing statuses, or sending messages.

Risk: Uploaded product images and marketplace text may be processed by MoreStore workflows or visible to marketplace participants.

Mitigation: Avoid confidential customer data, unreleased strategy, regulated data, or deal terms that should not be shared with the platform.

## Reference(s):

- [MoreStore homepage](https://morestore.ai)
- [Morestore ClawHub skill page](https://clawhub.ai/tyler-odenthal/skills/morestore)
- [OpenClaw vLLM provider docs](https://docs.openclaw.ai/providers/vllm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to call MoreStore APIs, parse JSON or SSE responses, report campaign IDs and match summaries, update configuration, and save generated product images.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
