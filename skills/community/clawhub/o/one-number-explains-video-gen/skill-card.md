## Description: <br>
Creates vertical short-form data-stat video prompts and WeryAI generation runs with a hero number, ramping counter or graph, closing meaning line, and timed English captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to turn one metric into a vertical social video prompt and WeryAI generation run. It is intended for dataviz Shorts, macro explainers, ticker-style TikToks, and similar social videos built around a single trend-defining number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid third-party WeryAI video service and requires a WERYAI_API_KEY. <br>
Mitigation: Install only when WeryAI use is intended, keep the API key out of source control, and review the generated prompt before submitting a paid generation job. <br>
Risk: Supplying a local image path can cause that file to be uploaded to WeryAI. <br>
Mitigation: Prefer public HTTPS image URLs and provide local paths only after confirming that the exact file may be uploaded. <br>
Risk: Data-stat videos can imply unsupported precision or factual certainty. <br>
Mitigation: Require user approval for final wording when real statistics matter and use illustrative-counter language when sources are not being cited. <br>


## Reference(s): <br>
- [WeryAI Video API Reference](resources/WERYAI_VIDEO_API.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/one-number-explains-video-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown response with a confirmed prompt, CLI command, and final video link or error.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and paid WeryAI usage; local image paths may be uploaded only with explicit user consent.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
