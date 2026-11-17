## Description:

Own Style Writer helps an agent separate style samples from content materials, convert local documents when needed, extract a reusable style profile, prepare a content brief and outline, and draft writing in the user's own reference style after confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowles](https://clawhub.ai/user/snowles)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and agents use this skill to learn from user-selected style samples while using separate content materials only for facts and examples. It is suited to drafting articles with an explicit outline review step, document conversion, and a final quality report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-selected local writing directories may contain private or sensitive documents.

Mitigation: Point the skill only at intended folders, review the generated manifest, and keep sensitive source material out of shared workspaces.

Risk: Documents may be uploaded to MinerU when upload is allowed.

Mitigation: Disable uploads for sensitive material, or allow upload only after confirming the files and the MinerU API mode are acceptable.

Risk: The local conversion fallback may install Python dependencies for document parsing.

Mitigation: Use a locked or sandboxed Python runtime and review dependency installation before processing untrusted files.

Risk: Converted ZIP or Office inputs and service-supplied result URLs can expand the input and network surface.

Mitigation: Restrict supported extensions to the formats needed for the task and review conversion errors and manifests before relying on the corpus.

Risk: Drafts may contain unsupported facts or high-risk financial, medical, legal, or operational claims from source materials.

Mitigation: Use the quality report to flag claims needing human verification before publication or operational use.

## Reference(s):

- [Own Style Writer homepage](https://github.com/snowles/own-style-writer)
- [ClawHub skill page](https://clawhub.ai/snowles/skills/own-style-writer)
- [MinerU API documentation](https://mineru.net/apiManage/docs)
- [MarkItDown documentation](https://github.com/microsoft/markitdown)
- [MarkItDown security considerations](https://github.com/microsoft/markitdown#security-considerations)
- [Style profile template](references/style_profile_template.md)
- [Content brief template](references/content_brief_template.md)
- [Outline review template](references/outline_review_template.md)
- [Quality check template](references/quality_check_template.md)
- [Writing principles](references/writing_principles.md)
- [写作复盘模板](references/写作复盘模板.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, manifest JSON, conversion error JSON, and inline shell or PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default workflow pauses for outline confirmation before drafting unless the user explicitly skips confirmation.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and changelog state 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
