## Description: <br>
Turn ideas into podcasts, explainer videos, voice narration, and AI images via ListenHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkaticld](https://clawhub.ai/user/kkaticld) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, developers, and agents use this skill to submit topics, URLs, text, scripts, or image prompts to ListenHub-related services for podcast, explainer video, text-to-speech, speech, and image generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted content, source URLs, prompts, and reference-image URLs are sent to ListenHub, Marswave, or Labnana services. <br>
Mitigation: Use this skill only for content you are comfortable sending to those services, and avoid submitting secrets, regulated data, or confidential material. <br>
Risk: The image generation script can install system packages. <br>
Mitigation: Review scripts/generate-image.sh before use and install dependencies manually when automatic package installation is not acceptable. <br>
Risk: The image generation script can persist API keys and output directory settings in shell startup files. <br>
Mitigation: Prefer setting LISTENHUB_API_KEY temporarily or through OpenClaw configuration, and avoid workflows that write credentials into shell startup files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kkaticld/listenhub-ai) <br>
- [Publisher profile](https://clawhub.ai/user/kkaticld) <br>
- [ListenHub podcast library](https://listenhub.ai/app/podcast) <br>
- [ListenHub explainer library](https://listenhub.ai/app/explainer) <br>
- [ListenHub text-to-speech library](https://listenhub.ai/app/text-to-speech) <br>
- [Marswave Labnana image API documentation](https://docs.marswave.ai/openapi-labnana.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON/status responses, hosted result links, and local generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LISTENHUB_API_KEY; image generation can use LISTENHUB_OUTPUT_DIR and may write generated image files to the local filesystem.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
