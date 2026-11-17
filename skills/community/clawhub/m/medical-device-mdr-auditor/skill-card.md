## Description:

Audit medical device technical files against EU MDR 2017/745 regulations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a local preliminary checklist against medical device technical-file folders for EU MDR 2017/745 document presence and basic completeness. Results should support review preparation, not replace qualified regulatory judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MDR audit results can be misleading because the skill mostly checks filenames and may be used outside its stated medical-device purpose.

Mitigation: Use it only as a preliminary local checklist, keep tasks within the documented medical-device workflow, and have a qualified MDR reviewer verify the underlying documents manually.

Risk: The skill reads local technical-file folders and can write report files to a requested output path.

Mitigation: Run it on copies of selected folders and choose an output path that will not overwrite important files.

Risk: Unnecessary or unpinned dependencies can increase installation and maintenance risk.

Mitigation: Remove or pin unnecessary dependencies before installing the skill in a controlled environment.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/medical-device-mdr-auditor)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON compliance reports with console text summaries and Markdown-style agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local technical-file directories and write report files when an output path is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
