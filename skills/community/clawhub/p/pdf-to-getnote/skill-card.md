## Description: <br>
Converts a PDF into a single GetNotes note with an AI-generated summary and embedded page images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pieces201020](https://clawhub.ai/user/pieces201020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents handling PDF workflows use this skill to convert a local PDF into one GetNotes note with a generated summary and page images, optionally adding it to a GetNotes knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports a live-looking GetNotes credential shipped with this release. <br>
Mitigation: Do not install this version until the publisher removes and rotates the exposed credential; use credentials only from the local OpenClaw configuration. <br>
Risk: PDF text and page images may be sent to GetNotes/OSS and possibly MiniMax during summarization and note creation. <br>
Mitigation: Use only PDFs approved for those services, verify the configured GetNotes account and topic ID before running, and delete leftover /tmp PDF image artifacts after processing. <br>


## Reference(s): <br>
- [PDF Import to GetNotes SOP](references/full_sop.md) <br>
- [GetNotes API Behavior Notes](references/api_behavior.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown note content with shell command examples and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local PDF path, GetNotes credentials, and optional topic ID or custom title; temporary page images are written under /tmp/pdf_pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
