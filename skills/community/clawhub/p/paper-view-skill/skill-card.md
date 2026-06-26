## Description: <br>
PaperView API helps agents generate ECharts visualizations, AI scientific diagrams, and word clouds from data, text, or PDF papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyccR](https://clawhub.ai/user/yyccR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to call PaperView APIs for charts, scientific diagrams, and keyword word clouds, then render the returned visualization outputs for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided datasets, text, or document URLs are sent to PaperView for processing. <br>
Mitigation: Do not submit confidential datasets, private paper links, regulated data, secrets, or unpublished material unless PaperView processing is acceptable for the use case. <br>
Risk: The PaperView API token can grant access to the user's quota-backed account. <br>
Mitigation: Keep PAPERVIEW_API_TOKEN in an environment variable and avoid pasting it into shared chats, prompts, logs, or files. <br>
Risk: Generated diagram images are returned as CDN URLs and may persist outside the local environment. <br>
Mitigation: Avoid generating diagrams from sensitive or unpublished material unless external image hosting and retention are acceptable. <br>


## Reference(s): <br>
- [PaperView ClawHub Skill Page](https://clawhub.ai/yyccR/paper-view-skill) <br>
- [PaperView Homepage](https://www.ipaperview.com) <br>
- [PaperView API Base](https://api.ipaperview.com) <br>
- [ECharts Visualization Endpoint](https://api.ipaperview.com/api/v1/viz/generate/) <br>
- [AI Scientific Diagram Endpoint](https://api.ipaperview.com/api/diagram/ai-generate/) <br>
- [Word Cloud Endpoint](https://api.ipaperview.com/api/wordcloud/extract/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JSON, HTML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PAPERVIEW_API_TOKEN and may produce ECharts options, image URLs, or word-frequency JSON for visual rendering.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
