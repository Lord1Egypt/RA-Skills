## Description:

Guides agents through Xiacai registration, match browsing, Da Liu Ren sports predictions, settlement checks, and performance tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjbcctv-123](https://clawhub.ai/user/xjbcctv-123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to interact with the Xiacai sports-prediction platform: registering or checking an account, browsing eligible matches, preparing predictions, submitting prediction calls, and reviewing settled results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses account-bound external API calls to xiacai.coze.site, which may expose user profile and prediction activity to that service.

Mitigation: Use only when the user trusts the Xiacai service, and confirm intent before account registration, prediction submission, profile update, or other POST requests.

Risk: The XIACAI_API_KEY credential is tied to the user's account.

Mitigation: Store the API key in secret storage or environment variables, avoid printing full keys, and redact it from logs and summaries.

Risk: Raw API responses, errors, or URLs may contain account-linked or untrusted data if stored persistently.

Mitigation: Avoid writing raw responses to persistent memory; when retention is needed, redact sensitive fields and treat stored API content as untrusted.

Risk: Sports predictions may be inaccurate or misleading if presented as reliable outcomes.

Mitigation: Present predictions as entertainment or platform interaction output, and avoid treating them as financial, betting, or factual certainty.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xjbcctv-123/skills/liuxian-dubao)
- [Authentication guide](artifact/认证.md)
- [Match browsing guide](artifact/赛事.md)
- [Prediction workflow guide](artifact/预测.md)
- [Results and settlement guide](artifact/战绩.md)
- [Error handling guide](artifact/错误处理.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples and user-facing prediction or results summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
