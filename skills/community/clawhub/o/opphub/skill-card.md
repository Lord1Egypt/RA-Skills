## Description:

OppHub connects an OpenClaw bot to the OppHub service so users can sign in, record company profiles, search business opportunities, and receive push notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtty-ai](https://clawhub.ai/user/mtty-ai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill from chat, scheduled jobs, or the OpenClaw backend to authenticate with OppHub, submit company knowledge, inspect status, configure push delivery, and find related business opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles login tokens and connects to an external OppHub service.

Mitigation: Install only in an environment where the OppHub service and companion plugin are trusted, and review token-related behavior before deployment.

Risk: The skill can upload company knowledge and generated cards.

Mitigation: Inspect generated cards and submitted knowledge for private or unwanted local-history content before confirming upload.

Risk: Environment overrides can redirect API or OAuth endpoints.

Mitigation: Do not set OPPHUB_API_BASE or OPPHUB_OAUTH_TOKEN_URL outside a controlled test setup.

Risk: The skill can create a recurring daily cron task.

Mitigation: Check whether the daily cron job is acceptable before installation or login-driven setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mtty-ai/skills/opphub)
- [Publisher profile](https://clawhub.ai/user/mtty-ai)
- [Source homepage from metadata](https://github.com/mtty-ai/opphub-skill)
- [OppHub API base](https://api.opphub.ruiplus.cn)
- [OAuth device-code endpoint](https://api.opphub.ruiplus.cn/api/oauth/device/code)
- [OAuth token endpoint](https://api.opphub.ruiplus.cn/api/oauth/device/token)
- [OAuth userinfo endpoint](https://api.opphub.ruiplus.cn/api/oauth/userinfo)
- [Refresh-token endpoint](https://api.opphub.ruiplus.cn/api/oauth/token)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chat-facing text and markdown, command-line JSON, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include OAuth login links, status summaries, generated knowledge cards, confirmation prompts, match results, and setup or uninstall commands.]

## Skill Version(s):

5.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
