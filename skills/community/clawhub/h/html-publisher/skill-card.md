## Description:

Publishes HTML content as an online webpage and returns an accessible public URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huyi9531](https://clawhub.ai/user/huyi9531)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish static HTML content, generated pages, or local HTML files and return a shareable public URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing an unpinned third-party CLI globally.

Mitigation: Review the gnomic-cli package first, prefer a pinned trusted version, and avoid elevated privileges during installation.

Risk: Published HTML is exposed through a public URL.

Mitigation: Publish only HTML that is safe to make public and does not contain private data or sensitive embedded resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huyi9531/skills/html-publisher)
- [gnomic-cli repository](https://github.com/huyi9531/gnomic_cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a public URL for static HTML when publishing succeeds.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
