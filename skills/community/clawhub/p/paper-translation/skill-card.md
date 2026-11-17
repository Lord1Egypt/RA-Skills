## Description:

ArXiv 论文精读级中文翻译，同步到 IMA 知识库和腾讯文档，并提供翻译校验流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fandywang87](https://clawhub.ai/user/fandywang87)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce complete Chinese translations of public ArXiv papers, preserve paper structure and formulas, add clearly marked translator notes, validate the Markdown, and prepare IMA and Tencent Docs versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent uploads to Tencent Docs and IMA can expose translated content outside the local agent session.

Mitigation: Add an explicit user confirmation step before upload and use the workflow only for public ArXiv papers or documents approved for those platforms.

Risk: The workflow uses a broad trigger surface for paper translation tasks.

Mitigation: Confirm the target paper, destination platforms, and upload intent before fetching, translating, or publishing content.

Risk: The temporary file pattern `/tmp/args.json` can collide with other processes or leave upload payloads on disk.

Mitigation: Use a unique restricted temporary file for each run and delete it immediately after the platform call completes.

## Reference(s):

- [平台兼容性与踩坑经验](references/platform-compat.md)
- [翻译迭代历史（MixFormer 案例）](references/iteration-history.md)
- [ClawHub skill page](https://clawhub.ai/fandywang87/skills/paper-translation)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces IMA and Tencent Docs oriented Markdown versions and a validation checklist.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
