## Description:

Converts PDF documents into editable PowerPoint presentations with intelligent content extraction and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, business analysts, consultants, educators, and content teams use this skill to convert PDF documents into editable PPTX presentations through a file-upload API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded PDFs leave the user's device for third-party processing.

Mitigation: Avoid confidential, regulated, or legally sensitive documents unless the provider's privacy, retention, deletion, and download-link access controls have been separately verified.

Risk: Converted presentation files are returned through a service-generated file URL.

Mitigation: Treat download links as sensitive and review access controls before sharing or automating retrieval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/pdf-to-pptx)
- [API Docs](https://api.mkkpro.com:8001/docs)
- [Kong Route](https://api.mkkpro.com/creative/pdf-to-pptx)
- [ToolWeb](https://toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [API Calls, Files, JSON, Guidance]

**Output Format:** [Multipart file upload request with JSON status metadata and a PPTX download URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an editable PowerPoint file from an uploaded PDF; the response may include processing metrics and a file URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
