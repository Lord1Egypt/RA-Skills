## Description: <br>
Lingzao helps agents research public creator content on Xiaohongshu/XHS, Douyin, and WeChat official accounts, including creator and post lookup, profile and comment analysis, article detail, short-video copy extraction, and requested creator image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itxiaohao](https://clawhub.ai/user/itxiaohao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, creator operators, and their agents use Lingzao to research public creator content, benchmark accounts, inspect posts, comments, and articles, and prepare content packages, titles, covers, scripts, and review outputs for Xiaohongshu, Douyin, and WeChat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lingzao uses a paid remote API and stores or reads a local API key. <br>
Mitigation: Install only when the user is comfortable providing a Lingzao API key, and avoid exposing keys or internal error details in shared outputs. <br>
Risk: Public-content lookup, deep search, and image generation may spend credits. <br>
Mitigation: Confirm credit-spending searches, deep lookups, and image-generation requests before calling paid capabilities. <br>
Risk: Selected links, public-content queries, and chosen reference images may be sent to the configured API. <br>
Mitigation: Send only user-approved public links, prompts, and reference images, and avoid sending private screenshots, backend metrics, or personal data unless intentionally approved. <br>
Risk: Commands can save article Markdown or generated images to local paths. <br>
Mitigation: Check --output and --image paths before execution, use temporary or user-approved locations, and avoid overwriting user files. <br>


## Reference(s): <br>
- [Lingzao ClawHub skill page](https://clawhub.ai/itxiaohao/skills/lingzao) <br>
- [Lingzao dashboard and tutorials](https://lingzao.atian.vip) <br>
- [Publisher profile: itxiaohao](https://clawhub.ai/user/itxiaohao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown and text responses with optional shell commands, JSON, saved Markdown article files, and generated image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LINGZAO_API_KEY for paid remote API calls; selected commands can write local Markdown or image files to explicit output paths.] <br>

## Skill Version(s): <br>
0.1.66 (source: evidence.release.version and artifact/VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
