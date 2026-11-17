## Description:

Reviews, analyzes, and polishes Chinese classical poetry across forms such as regulated verse, ci, qu, and old-style poetry, with attention to meter, rhyme, parallelism, imagery, diction, and structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilovecode2018](https://clawhub.ai/user/ilovecode2018)

### License/Terms of Use:

MIT-0

## Use Case:

External users, writers, and poetry reviewers use this skill to critique Chinese classical poems, answer metrical questions, and produce revised or polished versions with explanatory notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Playwright checker can submit poem text to sou-yun.cn during online metrical validation.

Mitigation: Use the bundled local references or manual review for unpublished or private poems, and run the online checker only when sharing poem text with the external service is acceptable.

Risk: The optional checker requires an unpinned Playwright installation.

Mitigation: Install dependencies in an isolated environment and pin Playwright versions before running the checker.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/ilovecode2018/skills/poetry-master)
- [Common ci pattern database](references/cipu_database.md)
- [Ci Lin Zheng Yun rhyme reference](references/cilin_zhengyun.md)
- [Classical poetry metrical rules](references/ge_lu_rules.md)
- [Sou-yun regulated verse checker](https://sou-yun.cn/AnalyzePoem.aspx)
- [Sou-yun ci pattern checker](https://sou-yun.cn/AnalyzeCi.aspx)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown critique with optional inline shell commands for metrical checking]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include annotated metrical analysis, revision suggestions, polished poem drafts, and notes on the checker or reference used.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
