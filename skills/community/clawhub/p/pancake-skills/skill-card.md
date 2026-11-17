## Description:

Pancake Skills helps agents use the Pancake Platform API to manage pages, conversations, messages, customers, analytics, tags, posts, users, media uploads, and chat plugin operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suminhthanh](https://clawhub.ai/user/suminhthanh)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to inspect and manage Pancake Platform sales-channel data from an agent-assisted shell workflow, including conversations, customer records, staff assignments, analytics, media uploads, and outbound messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pancake access tokens can authorize page, customer, conversation, and messaging operations.

Mitigation: Use least-privilege Pancake tokens, keep them out of repositories and logs, avoid shell tracing, and rotate tokens according to your internal policy.

Risk: Write-capable commands can send messages, generate tokens, update customer data, change assignments or tags, upload media, and export data.

Mitigation: Require `CONFIRM_WRITE=YES`, run a read-only command first to confirm IDs and payload shape, and manually review every write payload before execution.

Risk: `PANCAKE_BASE_URL` can redirect API calls to an alternate host.

Mitigation: Leave the default `https://pages.fm` endpoint in place unless using a trusted test host.

Risk: The helper scripts execute local shell and curl commands.

Mitigation: Install only from a trusted publisher and run the skill in a controlled shell environment.

## Reference(s):

- [OpenAPI Pancake Specification](references/openapi-pancake.yaml)
- [ClawHub skill page](https://clawhub.ai/suminhthanh/skills/pancake-skills)
- [Pancake User API](https://pages.fm/api/v1)
- [Pancake Page API v1](https://pages.fm/api/public_api/v1)
- [Pancake Page API v2](https://pages.fm/api/public_api/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that call Pancake APIs with user-provided access tokens.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
