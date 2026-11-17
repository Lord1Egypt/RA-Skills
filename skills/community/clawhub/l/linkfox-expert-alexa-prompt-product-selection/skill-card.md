## Description:

基于 Alexa 提示词的亚马逊选品研究专家，帮助亚马逊卖家、选品分析师、Listing 优化师和品牌运营基于市场数据生成并执行 Alexa 购物提示词、COSMO 关系提示词和选品洞察报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, product researchers, listing specialists, and brand operators use this skill to gather LinkFox-powered Amazon product and Alexa shopping-assistant data, generate 8-15 strategic Chinese prompts, execute them through Alexa search, and summarize product-selection opportunities in an HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives broad agent-routing instructions across several LinkFox helper skills.

Mitigation: Review the intended workflow before installation and monitor early runs to confirm the agent only invokes the expected LinkFox tools for the user request.

Risk: The skill requires a LinkFox API key and sends Amazon research prompts and related data to LinkFox cloud services.

Mitigation: Install it only for intended LinkFox workflows, protect the API key, and avoid endpoint overrides unless the destination is controlled and trusted.

Risk: Tool responses are saved locally and may include full product, prompt, and market-research outputs.

Mitigation: Avoid submitting sensitive inputs and periodically review or remove generated local LinkFox output files when they are no longer needed.

Risk: The bundled upload helper creates publicly accessible URLs for uploaded files.

Mitigation: Upload only files that are safe to publish and verify report or media contents before sharing URLs.

Risk: The skill can optionally create or manage remote scheduled tasks for recurring research workflows.

Mitigation: Confirm schedule, notification targets, and task text before enabling automation, and keep task-management actions in interactive sessions.

Risk: Generated HTML reports may render content derived from remote product or analysis data.

Mitigation: Open generated reports only when the source data is trusted and review report contents before distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-alexa-prompt-product-selection)
- [Publisher Profile](https://clawhub.ai/user/linkfox-ai)
- [Alexa Shopping Assistant API Reference](artifact/skills/linkfox-amazon-alexa-search/references/api.md)
- [Amazon Product Detail API Reference](artifact/skills/linkfox-amazon-product-detail/references/api.md)
- [AI Text Generation API Reference](artifact/skills/linkfox-aigc-textgen/references/api.md)
- [File Upload API Reference](artifact/skills/linkfox-file-upload/references/api.md)
- [Report Layout Component Library](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)
- [Task Scheduler API Reference](artifact/skills/linkfox-task-scheduler/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Chinese Markdown summaries, structured prompt lists, JSON-backed tool results, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts are generated from collected market data, executed one at a time through Alexa search, and summarized with source/tool attribution; final long-form findings are written as an HTML report with a returned path and short summary.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
