## Description: <br>
Explain anything by turning ideas, URLs, text, and image prompts into podcasts, explainer videos, voice narration, or generated images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xFANGO](https://clawhub.ai/user/0xFANGO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Listenhub to route media-generation requests through bundled shell scripts for podcasts, explainer videos, text-to-speech, multi-speaker speech, and image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected content, URLs, and image references are sent to ListenHub/Labnana APIs for processing. <br>
Mitigation: Do not submit confidential text, private URLs, secrets, or sensitive images unless you trust the provider and any image host involved. <br>
Risk: The image-generation setup can save API keys and output paths in shell startup files. <br>
Mitigation: Set LISTENHUB_API_KEY and LISTENHUB_OUTPUT_DIR through your shell or secret manager before use, and review any shell startup file changes made by first-run setup. <br>
Risk: The image-generation script can attempt to install missing curl or jq dependencies through system package managers. <br>
Mitigation: Install and review curl and jq yourself before running the skill, especially on shared or managed systems. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/0xFANGO/listenhub-official-skills) <br>
- [ListenHub API Key Settings](https://listenhub.ai/settings/api-keys) <br>
- [Labnana Image Generation API Documentation](https://docs.marswave.ai/openapi-labnana.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations, JSON responses, URLs, and local file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return generated media URLs or local image file paths; long-running media jobs can require status polling.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
