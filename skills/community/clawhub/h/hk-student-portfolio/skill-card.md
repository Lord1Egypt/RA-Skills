## Description:

Generates bilingual Hong Kong secondary-school application portfolio Word documents from structured student data, with templates for traditional local schools, direct-subsidy or private schools, and international schools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchenyao-tech](https://clawhub.ai/user/wuchenyao-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Parents, education consultants, and agents use this skill to turn Hong Kong secondary-school application data into a polished bilingual portfolio document. It is intended for local document generation and school-application preparation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can collect sensitive child and family data, including identity numbers, birth dates, addresses, contact details, guardian information, grades, and recommendations.

Mitigation: Redact fields that are not required by the target school, avoid entering exact identifiers unless necessary, store generated Word or PDF files in access-controlled locations, and delete drafts when no longer needed.

Risk: Generated application content may overstate achievements or include inaccurate school-application claims if the input data is incomplete or embellished.

Mitigation: Review the portfolio with the applicant and guardian, verify awards and rankings against source records, and keep the included declaration accurate before submission.

Risk: The skill depends on local Python execution and document-generation dependencies.

Mitigation: Install dependencies in an isolated environment with pinned versions and review files before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchenyao-tech/skills/hk-student-portfolio)
- [Miss Kirby Portfolio guide](https://www.misskirby.com/portfoliomaking)
- [Big Bang Academy secondary intake portfolio guide](https://www.bigbangacademyhk.com/blog-zh/secondary-intake-portfolio)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON data structures, Python commands, and generated Word .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses python-docx locally; generated documents may be converted to PDF outside the skill.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter, artifact/_meta.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
