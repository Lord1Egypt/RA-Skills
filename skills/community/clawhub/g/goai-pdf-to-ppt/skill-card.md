## Description:

Convert PDF documents to PowerPoint presentations via GoAI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goai](https://clawhub.ai/user/goai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert a local or remote PDF into a PowerPoint presentation through the GoAI conversion service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents and generated result URLs are sent to or received from the GoAI service.

Mitigation: Use the skill only for documents appropriate for upload to that service, and avoid sharing sensitive result URLs in broader conversations.

Risk: GOAI_BASE_URL can redirect API-key use and document uploads to a different endpoint.

Mitigation: Leave GOAI_BASE_URL unset unless the endpoint is a trusted HTTPS service with an appropriate scoped credential.

Risk: Downloaded presentations are written to the working directory and may be opened automatically.

Mitigation: Run the skill in a low-impact directory and review or disable automatic opening before handling untrusted outputs.

## Reference(s):

- [GoAI PDF to PPT on ClawHub](https://clawhub.ai/goai/skills/goai-pdf-to-ppt)
- [GoAI](https://mustgoai.com)
- [GoAI PPT Service](https://ppt.mustgoai.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Plain text result lines with a local PowerPoint file path and public result URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a .pptx file after uploading local PDFs or using a remote PDF URL.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and pyproject.toml show 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
