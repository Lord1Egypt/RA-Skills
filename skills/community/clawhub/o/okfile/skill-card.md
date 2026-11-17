## Description:

Uploads and publishes files or static site folders to OkFile, with direct links, preview URLs, and multipart support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okfilecom](https://clawhub.ai/user/okfilecom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Okfile to upload, publish, and share files or static site folders through OkFile, including workflows that need generated direct, preview, playback, or site URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files or folders uploaded through this skill may become accessible through generated links or subdomains.

Mitigation: Use the skill only for content intended for OkFile sharing, and avoid uploading secrets, credentials, internal documents, or private folders unless sharing is explicitly intended.

Risk: The optional CLI install relies on external package distribution.

Mitigation: Use trusted package sources and pin versions when reproducibility or supply-chain review is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/okfilecom/skills/okfile)
- [Server-resolved source repository](https://github.com/okfilecom/okfile)
- [OkFile official site](https://www.okfile.com/)
- [OkFile upload page](https://www.okfile.com/en/upload/)
- [OkFile PyPI package](https://pypi.org/project/okfile/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with HTTP request examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated public URLs such as url, playUrl, siteUrl, and entryUrl.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
