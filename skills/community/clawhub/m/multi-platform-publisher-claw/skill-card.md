## Description:

Helps agents plan and prototype multi-platform content distribution by adapting content for Douyin, Xiaohongshu, WeChat Channels, Bilibili, and Weibo, optimizing titles and tags, recommending publishing times, and summarizing publishing status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, operators, and developers use this skill to prepare platform-specific publishing commands, title and description adaptations, hashtag guidance, posting-time recommendations, and publishing summaries for Chinese social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill can overstate real posting capability and report fake publication success.

Mitigation: Treat publishing results and generated links as unverified prototype output until real platform adapters, confirmation checks, and operator review are in place.

Risk: The security guidance warns against using production account credentials with the current implementation.

Mitigation: Test only in a private working directory with non-production accounts or dummy inputs, and add credential handling plus explicit confirmation controls before production use.

## Reference(s):

- [Platform Rules](artifact/references/platform-rules.md)
- [SEO Optimization Rules](artifact/references/seo-optimization.md)
- [Best Posting Times](artifact/references/best-posting-time.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and publishing-status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script may write timestamped JSON publishing records; security evidence says reported success and links should be treated as prototype outputs unless real platform adapters and confirmation controls are added.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
