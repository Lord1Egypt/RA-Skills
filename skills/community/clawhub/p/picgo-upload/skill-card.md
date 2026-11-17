## Description:

Upload an image or file with PicGo and get back a hosted, shareable URL for documentation, markdown, screenshots, or public file sharing when no specific destination is named.

This skill is ready for commercial/non-commercial use.

## Publisher:

[molunerfinn](https://clawhub.ai/user/molunerfinn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and other external users use this skill to turn local images or files into hosted URLs for READMEs, blogs, notes, wikis, and shareable downloads. It routes uploads through an existing PicGo desktop or CLI setup and guides login or installation only when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GUI helper can be pointed at arbitrary HTTP hosts and may send a local auth secret and file paths to that endpoint.

Mitigation: Use the GUI helper only with localhost or 127.0.0.1 unless the endpoint is explicitly trusted, and avoid passing sensitive secrets or confidential filenames.

Risk: PicGo Cloud links are public and deleted files may remain cached.

Mitigation: Confirm before uploading sensitive non-image files and remind users that returned links are publicly accessible.

Risk: PicGo CLI setup may depend on global installation, login state, quota, and configured uploader.

Mitigation: Probe the existing PicGo app or CLI first, avoid blocking browser login flows, and provide one concrete next step for login, quota, file type, or configuration failures.

## Reference(s):

- [PicGo Upload on ClawHub](https://clawhub.ai/molunerfinn/skills/picgo-upload)
- [GUI upload usage](references/gui-upload-usage.md)
- [Upload error triage](references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and returned hosted URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns bare URLs by default, markdown image links in document contexts, and plain links for non-image files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
