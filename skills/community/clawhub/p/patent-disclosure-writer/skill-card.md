## Description:

撰写中文专利交底书。Use when: 用户需要撰写专利交底书、技术交底书、专利申请文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[changye](https://clawhub.ai/user/changye)

### License/Terms of Use:


## Use Case:

External users, inventors, and technical teams use this skill to collect required invention details and draft Chinese patent disclosure documents. It helps structure technical background, invention purpose, technical solution, benefits, implementation details, and optional figures for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow collects inventor/contact details and technical invention information that may be confidential.

Mitigation: Use it only in an environment appropriate for storing confidential material, review the output directory before generation, and avoid entering sensitive material when local storage is not acceptable.

Risk: The skill saves generated Markdown drafts, images, and converted Word files locally.

Mitigation: Confirm the destination folder before writing files and review generated artifacts before sharing or filing.

## Reference(s):

- [Patent Writing Skills](references/Patent_Writing.md)
- [Patent Disclosure Example](references/patent_example.md)
- [Mermaid Live Editor](https://mermaid.live/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Chinese Markdown patent disclosure draft with optional Mermaid diagrams, PNG image outputs, and Word document conversion.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided patent metadata and technical invention details. Optional Word and image generation depend on pandoc and mmdc availability.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
