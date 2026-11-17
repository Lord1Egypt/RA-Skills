## Description:

A web and CLI tool for generating images with AceData Nano Banana models, slicing them into 2/4/6/9-grid outputs, and managing generated work with previews and ZIP downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyunnet](https://clawhub.ai/user/xiyunnet)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate prompt-based or reference-image visuals for short-form storytelling, split outputs into multi-panel grids, and manage or download the resulting image assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner summary says the tool exposes powerful unauthenticated web APIs that can disclose local files, alter or delete data, save credentials, and stop the service.

Mitigation: Run it only in a tightly controlled local environment; bind it to localhost, add authentication and CSRF protection, protect shutdown/admin/config routes, and restrict file-serving, crop, and upload paths to a dedicated workspace.

Risk: The scanner guidance warns that credentials and Authorization headers may be exposed if logs or the service are accessible.

Mitigation: Stop logging Authorization headers, protect saved credentials, and rotate any API keys used with this version if logs or the service were exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiyunnet/skills/nano-banana-cut)
- [AceData Nano Banana access link](https://share.acedata.cloud/r/1uN88BrUTQ)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with command examples; the tool itself produces image files, sliced image grids, thumbnails, ZIP archives, and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided AceData API credentials for image generation and optional platform credentials for image upload/edit workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
