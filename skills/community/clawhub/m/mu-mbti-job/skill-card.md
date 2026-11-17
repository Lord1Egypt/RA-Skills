## Description:

MBTI人格与职业测评 guides users through 70, 93, or 144 question bilingual MBTI-style personality and career assessments, then produces local scoring results and bilingual PDF reports for personal or team use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT

## Use Case:

Individuals, team leads, and agents use this skill to run local MBTI-style career self-assessments, score answer JSON, and generate bilingual personal or team PDF reports. The results are for self-awareness and career discussion, not hiring, promotion, performance, or clinical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated quiz and report files may include under-disclosed external promotional links.

Mitigation: Review generated HTML and PDF footers before distribution, and avoid clicking footer badges unless leaving the local workflow is acceptable.

Risk: Answer JSON, browser-saved quiz progress, scoring results, and PDF reports can contain sensitive personal assessment data.

Mitigation: Treat generated files as sensitive personal data, clear browser-saved quiz progress on shared machines, and delete local artifacts when they are no longer needed.

Risk: Optional PDF dependencies and browser-based PDF fallback can vary across managed environments.

Mitigation: Pin optional PDF dependencies and validate the selected PDF rendering path before institutional or repeated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muippt/skills/mu-mbti-job)
- [Scoring and output reference](references/scoring-and-output.md)
- [Project landing page](https://muippt.github.io/mu-mbti-job/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON scoring files, generated HTML quiz pages, and PDF reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local answer JSON, result JSON, and bilingual personal or team PDF reports; optional PDF dependencies may affect rendering quality.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
