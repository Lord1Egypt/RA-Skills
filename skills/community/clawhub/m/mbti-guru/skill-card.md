## Description:

Mbti Guru provides MBTI-style personality tests in four lengths and generates bilingual personality, career, relationship, and PDF reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[effeceee](https://clawhub.ai/user/effeceee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and channel operators use this skill to run guided MBTI-style questionnaires, resume in-progress tests, view history, and receive bilingual personality analysis reports. Results are intended as informational self-assessment output, not as a basis for major life, hiring, clinical, or other high-stakes decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local session and history storage can expose personality-test progress or results across users on shared or public bot deployments.

Mitigation: Use only in trusted single-tenant deployments until session ownership checks, access isolation, and retention cleanup are reviewed and fixed.

Risk: Personality-test reports may be over-applied to consequential decisions.

Mitigation: Present reports as informational self-assessment guidance and avoid using results for hiring, clinical, legal, or other high-stakes decisions.

Risk: Saved test data can persist locally after completion or interruption.

Mitigation: Document local data paths and establish deletion or retention procedures for data/sessions and data/history before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/effeceee/skills/mbti-guru)
- [Publisher profile](https://clawhub.ai/user/effeceee)
- [SKILL.md](artifact/SKILL.md)
- [CLAWHUB.md](artifact/CLAWHUB.md)
- [Report specification](artifact/docs/report_spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Interactive chat responses, Markdown-style reports, local JSON session/history files, and optional PDF reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores progress and completed result history locally under data/sessions and data/history.]

## Skill Version(s):

1.5.2 (source: server release evidence and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
