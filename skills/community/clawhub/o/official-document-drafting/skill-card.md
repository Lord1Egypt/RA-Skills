## Description: <br>
Drafts, revises, standardizes, summarizes, and exports Chinese official documents and formal administrative texts with document-type templates, fact-bound drafting rules, and optional Word export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaohui-yang](https://clawhub.ai/user/zhaohui-yang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to draft or refine Chinese official documents, administrative reports, notices, briefings, speeches, work plans, and related formal materials. It is most useful when the output needs a fixed document structure, formal agency tone, placeholders for missing facts, Markdown delivery, or optional .docx export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated official, policy, legal, private, or public-facing documents may be incomplete, inaccurate, or unsuitable for formal use without review. <br>
Mitigation: Review generated documents before official use and verify facts, dates, sources, legal references, private information, and policy-sensitive content with an authorized reviewer. <br>
Risk: The optional font download script can retrieve third-party font assets. <br>
Mitigation: Run font download or installation scripts only after accepting the source and licensing of the fonts, or use approved local fonts instead. <br>
Risk: Saved drafts or exported Word files may contain sensitive document content. <br>
Mitigation: Specify an appropriate output path for sensitive documents and handle generated files according to the user's confidentiality and retention requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaohui-yang/official-document-drafting) <br>
- [Project homepage](https://github.com/zhaohui-yang/official-document-drafting) <br>
- [Document types reference](artifact/references/document-types.md) <br>
- [Layout rules reference](artifact/references/layout-rules.md) <br>
- [Style rules reference](artifact/references/style-rules.md) <br>
- [Font usage reference](artifact/references/font-usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown drafts by default, with optional Word .docx files and shell commands for validation, font setup, or export when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholders for missing facts and requires human review before official, legal, sensitive, private, or public-facing use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
