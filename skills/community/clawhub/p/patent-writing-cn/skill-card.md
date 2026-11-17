## Description:

Creates patent-disclosure drafts and supporting review notes from R&D materials or an initial technical idea.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External inventors, product teams, and developers can turn technical disclosures, R&D reports, or an initial idea into a patent-disclosure draft and review notes for a patent professional to refine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paid service key could be exposed through chat, local files, or a redirected connection.

Mitigation: Keep keys out of chat, use the documented environment-variable setup, restrict authenticated connections to the intended HTTPS service, and protect local credential files.

Risk: Invention materials may be sensitive and uploads are retained during the account's lifetime.

Mitigation: Share only authorized invention material and review PatentMax's privacy and retention terms before uploading.

Risk: Generating or revising a draft can incur charges.

Mitigation: Explain the cost before submission and obtain the user's consent before each paid generation or revision.

## Reference(s):

- [Materials Guide](artifact/references/materials-guide.md)
- [Workflow](artifact/references/workflow.md)
- [FAQ](artifact/references/faq.md)
- [PatentMax API Platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Files, Analysis, Guidance]

**Output Format:** [Microsoft Word (.docx) patent draft and review notes, with structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft materials require inventor review and patent-professional finalization; patentability or grant is not guaranteed.]

## Skill Version(s):

1.1.9 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
