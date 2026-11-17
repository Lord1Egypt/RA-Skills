## Description:

An information retrieval assistant for GaoKao regional score lines, designed to help candidates query admission cut-off scores, admission batches, and corresponding rankings across different regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhl-det](https://clawhub.ai/user/jhl-det)

### License/Terms of Use:

MIT-0

## Use Case:

External users and education-focused agents use this skill to answer Chinese GaoKao score-line questions by province, year, student category, and admission batch. It helps candidates retrieve and summarize regional cut-off scores and rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query details are sent to Tencent's GaoKao data endpoint when the bundled lookup script runs.

Mitigation: Disclose the external data request before deployment where policy requires it, and avoid sending unnecessary sensitive personal information in lookup prompts.

Risk: Admission score-line data may be incomplete, unavailable, or stale relative to official admissions notices.

Mitigation: Use retrieved results as informational guidance and verify high-impact admissions decisions against official provincial examination authority publications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jhl-det/skills/province-score-line)
- [Tencent GaoKao score data endpoint](https://gaokao.search.qq.com/skills_data)
- [GaoKao score reference page](https://m.gaokao.cn/proscore?fromcoop=sougou)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise natural-language answer with retrieved score-line data and optional command-backed query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses province, year, student category, and admission batch filters when present; asks for a province when the user query does not identify one.]

## Skill Version(s):

0.1.2 (source: server release evidence, released 2026-05-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
