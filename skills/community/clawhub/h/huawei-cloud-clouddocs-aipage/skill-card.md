## Description:

Turns user-provided topics or notes into a new online page document and a local Word copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

External users can turn a topic, text, or outline into a shareable online page and receive a local Word copy. The skill is intended for creating new pages; it does not edit existing pages or create slides, tables, mind maps, PDFs, or themed pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install a bundled executable and change PATH; the security scan says coverage is partial and the executable was not fully analyzed.

Mitigation: Review the installer and checksum, and obtain user approval before installation or PATH changes.

Risk: Creating a page sends the local draft content to the cloud service.

Mitigation: Review the draft and confirm the intended account and service before submitting content.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-clouddocs-aipage)
- [Page content guidance](references/page-content.md)
- [Service permissions and access guidance](references/iam-policies.md)
- [CLI installation guide](bin/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown content, an online document link, and a Word (.docx) file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a new page and exports a local Word copy when export succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata; bundled artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
