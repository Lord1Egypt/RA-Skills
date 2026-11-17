## Description:

解说中国和西欧历史上的政治斗争事件，涵盖中国从先秦到清末、西欧从古罗马到19世纪的宫廷政变、党争、权臣专权、宗教冲突、革命等重大政治斗争，并支持中西对比分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd1993](https://clawhub.ai/user/wd1993)

### License/Terms of Use:


## Use Case:

External users can ask for concise Chinese-language explanations of Chinese and Western European political struggles, palace coups, factional conflicts, usurpations, religious conflicts, revolutions, and cross-civilization comparisons. The skill uses bundled references by default and can optionally search for differing viewpoints when a Tavily API key is intentionally configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional search mode can run a local Python script through Bash and send search terms to Tavily.

Mitigation: Use the bundled reference mode by default; enable search only after intentionally configuring TAVILY_API_KEY and reviewing outbound-query handling.

Risk: The skill text includes a hardcoded fallback path outside the package.

Mitigation: Prefer the packaged script path and verify any fallback path before executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wd1993/skills/political-struggle)
- [中国历史政治斗争参考资料](artifact/reference.md)
- [西欧历史政治斗争参考资料](artifact/western-europe-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown with structured event summaries and optional search-result synthesis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search mode requires TAVILY_API_KEY and may send user search terms to Tavily.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
