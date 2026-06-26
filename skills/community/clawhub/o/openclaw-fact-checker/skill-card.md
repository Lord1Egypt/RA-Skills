## Description: <br>
Fact-check news articles, social media posts, images, and videos, including claim verification, misinformation checks, and media authenticity review in any language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cliffyan28](https://clawhub.ai/user/cliffyan28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to verify factual claims, news articles, images, and videos, with structured verdicts, confidence scores, and cited evidence. It is suited for multilingual fact-checking workflows where web search and optional media-analysis tools are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fact-check inputs, URLs, media metadata, extracted frames, or audio may be processed by search providers or third-party APIs. <br>
Mitigation: Avoid confidential or sensitive material unless cloud/API paths are disabled and the configured providers are approved for the data. <br>
Risk: Some setup checks echo API-key environment variables while determining whether optional services are configured. <br>
Mitigation: Review and remove API-key echo commands before using real secrets or running in shared logs. <br>
Risk: The skill can ask to add persistent routing instructions to AGENTS.md after a successful fact-check. <br>
Mitigation: Approve the persistence prompt only if automatic future routing to this skill is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cliffyan28/openclaw-fact-checker) <br>
- [Project Homepage](https://github.com/cliffyan28/fact-checker) <br>
- [Text Verification Pipeline](references/text_pipeline.md) <br>
- [Image Verification Pipeline](references/image_pipeline.md) <br>
- [Video Verification Pipeline](references/video_pipeline.md) <br>
- [External API Reference](references/api_docs.md) <br>
- [Structured Output Schema](references/output_schema.json) <br>
- [Google Fact Check Tools API](https://developers.google.com/fact-check/tools/api/reference/rest) <br>
- [Brave Search API](https://brave.com/search/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports by default, with optional JSON structured output when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include per-claim or per-media verdicts, confidence scores, source URLs, and analysis-method notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
