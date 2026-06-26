## Description: <br>
Creates short AI-generated videos for ads, social media, brand, product, and explainer content in 16:9, 9:16, or 1:1 aspect ratios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madu1seo-bit](https://clawhub.ai/user/madu1seo-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and developers use this skill to submit short-video requests to Pexo, upload optional reference media, monitor generation progress, preview options, and retrieve final video URLs. It supports product ads, social clips, UGC-style content, brand videos, explainers, and revision workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive Pexo API key from environment variables or ~/.pexo/config. <br>
Mitigation: Keep the config file private, avoid sharing or committing the key, and rotate the key if exposure is suspected. <br>
Risk: Prompts and selected media are sent to Pexo as an external video-generation service. <br>
Mitigation: Submit only media and prompt content that is acceptable to send to Pexo. <br>
Risk: A misconfigured PEXO_BASE_URL could send credentials or content to the wrong endpoint. <br>
Mitigation: Verify PEXO_BASE_URL points to the real Pexo endpoint before running the skill. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/madu1seo-bit/pexoai-agent-madu) <br>
- [Pexo Homepage](https://pexo.ai) <br>
- [Pexo OpenClaw Setup](https://pexo.ai/connect/openclaw) <br>
- [Setup and Troubleshooting](references/SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON status snippets, project links, preview URLs, and final video URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PEXO_API_KEY, PEXO_BASE_URL, curl, jq, and file; generated videos are produced asynchronously by the Pexo service.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
