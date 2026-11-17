## Description:

Provides LinkFox gateway scripts and documentation for Temu EU Partner promotion APIs, including campaign lookup, candidate goods query, goods enrollment, enrolled goods query, operation status query, and goods update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Temu EU sellers and operators use this skill to call LinkFox-mediated Partner Promotion APIs for promotion discovery, product enrollment, enrolled-goods review, operation status checks, and promotion goods updates.

### Deployment Geography for Use:

Europe

## Known Risks and Mitigations:

Risk: The skill can expose LinkFox and Temu account credentials through gateway calls and local token storage.

Mitigation: Use only accounts intended for this connector, avoid broad or long-lived tokens, and protect or remove the plaintext local token store when it is no longer needed.

Risk: The generic proxy and file-download scripts provide broader API and data-access capability than the named EU promotion workflow requires.

Mitigation: Prefer the specific promotion scripts, use the generic proxy only when necessary, and verify operation type, payment, deactivation, and update parameters before execution.

Risk: Saved LinkFox output directories may contain sensitive seller, promotion, product, or billing data.

Mitigation: Treat local linkfox output directories as sensitive data and restrict access, retention, and sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-promotion-eu)
- [Temu accessToken 授权与获取](references/access-token.md)
- [linkfox-temu-promotion-eu API 参考](references/api.md)
- [Promotion 接口文档索引](references/apis/README.md)
- [Partner EU Promotion 接口目录](references/partner-eu-catalog.md)
- [Temu 授权流程](references/authorization-flow.md)
- [解决认证和积分问题](references/onboarding.md)
- [Temu Partner EU Documentation](https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896)
- [Temu EU OpenAPI Router](https://openapi-b-eu.temu.com/openapi/router)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance, shell command examples, Python scripts, and JSON API responses saved to local files with stdout summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are written under a local linkfox session data directory; small responses may be printed inline and larger responses are summarized unless --inline is used.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
