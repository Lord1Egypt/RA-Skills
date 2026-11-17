## Description:

Convert images to PowerPoint presentations through the GoAI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goai](https://clawhub.ai/user/goai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert local image files or image URLs into PPTX presentations with GoAI's hosted conversion service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images or PDFs may be sent to GoAI for conversion.

Mitigation: Use only files approved for GoAI processing and avoid sensitive inputs unless the deployment policy permits this transfer.

Risk: The skill requires GOAI_API_KEY and allows GOAI_BASE_URL to override the destination endpoint.

Mitigation: Store the API key only in the configured skill environment and set GOAI_BASE_URL only for fully trusted endpoints with an appropriate key.

Risk: Generated PPT files are downloaded and may be opened automatically.

Mitigation: Review the saved file path before opening the presentation and prefer a sandboxed viewer in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goai/skills/goai-image-to-ppt)
- [GoAI publisher profile](https://clawhub.ai/user/goai)
- [GoAI homepage](https://mustgoai.com)
- [GoAI PPT service endpoint](https://ppt.mustgoai.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text result lines with a local PPTX path and generated media URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and GOAI_API_KEY; successful runs produce a downloaded PPTX file and public result URL.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
