## Description: <br>
当用户需要追热点产出稿件、围绕指定话题仿爆款写法、对已有文章做质量、违禁词或 SEO 优化、或需要成稿、爆款理由、可选封面与多平台适配方案时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content marketers, new-media editors, and creators use this skill to turn a topic, trend, or draft into platform-adapted Chinese articles with titles, SEO suggestions, publication guidance, quality checks, and optional cover-image direction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may search the web for trends and competitor content, which can expose sensitive draft topics or campaign plans. <br>
Mitigation: Use a no-network or text-only mode for sensitive topics, drafts, or unreleased campaigns, or require confirmation before any web search. <br>
Risk: The workflow may generate cover-image prompts or images that include campaign context or unsuitable visual claims. <br>
Mitigation: Require confirmation before image generation and review generated prompts or images for platform compliance, rights, and factual accuracy. <br>
Risk: Trend, ranking, reading-count, or source claims can be misleading when live data sources are unavailable or incomplete. <br>
Mitigation: Disclose unavailable data, use verifiable sources, and avoid fabricating rankings, engagement numbers, or citations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/hotspot-article-generator) <br>
- [Core workflow](references/core_workflow.md) <br>
- [Article template](assets/article-template.md) <br>
- [Viral article guide](references/viral-article-guide.md) <br>
- [Hotspot analysis framework](references/hotspot-analysis-framework.md) <br>
- [Style analysis framework](references/style-analysis-framework.md) <br>
- [Quality check guide](references/quality-check-guide.md) <br>
- [Cover image specification](references/cover-image-spec.md) <br>
- [Prohibited words checker](scripts/check_prohibited_words.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown articles, title variants, SEO metadata, quality reports, publication guidance, and optional cover-image prompts or specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can adapt drafts for multiple Chinese content platforms and may include risk-word findings, revision suggestions, and publish-time recommendations.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
