## Description: <br>
Own Style Writer helps an agent learn writing style from user-provided style materials, keep those separate from factual content materials, convert local documents with MinerU when upload is approved or local MarkItDown fallback otherwise, and produce a style profile, content brief, outline, draft, and quality report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowles](https://clawhub.ai/user/snowles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and writing-focused agent operators use this skill to separate style samples from content materials, prepare local writing corpora, and draft articles in the user's requested style after outline confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected style and content folders, which may contain private documents. <br>
Mitigation: Provide only intended folders and files, and use the local MarkItDown path for private materials. <br>
Risk: MinerU upload can send source documents to a third-party service when enabled. <br>
Mitigation: Enable upload only after explicit consent and only for files suitable for third-party processing. <br>
Risk: The generated workspace may contain converted copies and manifests of source materials. <br>
Mitigation: Review and manage the .own-style-writer output directory according to the sensitivity of the source documents. <br>
Risk: Drafts can carry unsupported or high-risk claims from supplied materials. <br>
Mitigation: Review the content brief, outline, draft, and quality report; verify names, dates, numbers, quotes, and regulated-domain claims before use. <br>


## Reference(s): <br>
- [Own Style Writer homepage](https://github.com/snowles/own-style-writer) <br>
- [MinerU API documentation](https://mineru.net/apiManage/docs) <br>
- [Writing principles](references/writing_principles.md) <br>
- [Style profile template](references/style_profile_template.md) <br>
- [Content brief template](references/content_brief_template.md) <br>
- [Outline review template](references/outline_review_template.md) <br>
- [Quality check template](references/quality_check_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable workspace artifacts such as converted corpora, manifests, style profiles, content briefs, outlines, drafts, and quality reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
