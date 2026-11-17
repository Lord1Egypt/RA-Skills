## Description:

ABA搜索词周快照速查（SFR+Top ASIN点击/转化份额）与Amazon关键词挖掘扩展（搜索建议词扩展+Widget分类卡片挖掘），批量产出长尾词库并导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce operators use this skill to look up weekly ABA search-frequency rankings, top clicked ASIN share data, and related keyword opportunities. It also helps agents mine Amazon search suggestions and Widget category cards, then summarize or export keyword lists for market and listing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword queries, prompts, session metadata, and optional feedback reports may be shared with LinkFox services.

Mitigation: Install only when the publisher is trusted, avoid entering sensitive business data, and review any feedback content before submission.

Risk: Credential and network handling depends on LINKFOX_* environment configuration.

Mitigation: Use trusted HTTPS LinkFox endpoints only, avoid untrusted gateway overrides, and run the skill in an isolated environment with pinned dependencies where possible.

Risk: The file-upload helper can turn local files into publicly accessible URLs.

Mitigation: Do not upload private files, and confirm each file is suitable for public access before using the upload workflow.

## Reference(s):

- [Primary Skill Definition](SKILL.md)
- [ABA Snapshot API Reference](skills/amazon-aba-kw-snapshot/references/api.md)
- [ABA Snapshot Contract](skills/amazon-aba-kw-snapshot/references/contract.json)
- [ABA Intelligent Query API Reference](skills/linkfox-aba-intelligent-query/references/api.md)
- [Amazon Suggestion Miner API Reference](skills/linkfox-amazon-suggestion-miner/references/api.md)
- [Amazon Widget Miner API Reference](skills/linkfox-amazon-widget-miner/references/api.md)
- [File Upload API Reference](skills/linkfox-file-upload/references/api.md)
- [Analysis Report Component Library](skills/linkfox-report-generator/references/analysis-layouts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown tables and summaries, JSON responses, optional CSV download links, Excel/JSON files, and HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [ABA queries may consume LinkFox credits; search-suggestion and widget mining are described as direct Amazon public API calls. Some workflows save session files or return public URLs when export or upload is requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
