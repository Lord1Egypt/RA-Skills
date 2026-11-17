## Description:

Fetch WeChat Official Account articles from either a public account name or a WeChat article URL, with URL-first extraction and graceful fallback when account search is unreliable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nasplycc](https://clawhub.ai/user/nasplycc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-operations users use this skill to extract full WeChat Official Account article content, identify the publishing account, retrieve recent account articles, and manage the WeChat MP session needed for account-level queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores WeChat MP backend session cookies and tokens in plaintext session cache files.

Mitigation: Use an isolated workspace, prefer environment variables for temporary credentials, and do not commit, publish, or share scripts/cache session files.

Risk: The article command can fetch user-supplied URLs, and the security review specifically flags arbitrary URL fetching.

Mitigation: Pass only real https://mp.weixin.qq.com article URLs and review network activity before installation or execution.

Risk: Account search and article listing depend on a valid WeChat MP backend session and brittle WeChat endpoints.

Mitigation: Check session status before account-level queries, treat partial results and warnings as expected, and prefer URL-first extraction when search is unreliable.

Risk: The artifact handoff references external memory files that are not part of the packaged evidence.

Mitigation: Avoid following external memory-file checklists unless you explicitly intend to expose that local context.

## Reference(s):

- [WeChat MP Reader Design](references/design.md)
- [WeChat MP Reader Usage Guide](references/usage.md)
- [ClawHub Skill Listing](https://clawhub.ai/nasplycc/skills/nasply-wechat-mp-reader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-shaped article, account, session, and warning objects plus shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include article HTML, cleaned markdown content, image URLs, account metadata, session status, account article lists, and warnings about fallbacks or missing session state.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
