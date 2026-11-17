## Description:

SCI journal selection assistant for meta-analysis and systematic review papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenhan9739](https://clawhub.ai/user/wenhan9739)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and academic authors use this skill to choose SCI journals for meta-analysis or systematic review manuscripts. It compares scope fit, JCR and CAS quartiles, impact factor, acceptance-rate estimates, review speed, APC, desk-rejection risk, and pre-submission compliance needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Journal metrics, indexing status, APCs, acceptance-rate estimates, and submission requirements may change after the packaged data is published.

Mitigation: Verify current journal data and requirements on publisher, indexing, or journal-listing sites before using the recommendations for submission decisions.

Risk: The skill provides decision support for academic submissions and should not be treated as authoritative publishing advice.

Mitigation: Use the report as a structured starting point and confirm final choices against institutional requirements, journal policies, and manuscript-specific constraints.

Risk: Evidence security guidance notes that packaged reference paths appear inconsistent with the skill instructions.

Mitigation: Confirm the available artifact files are loaded before relying on local journal metrics or qualitative database entries.

## Reference(s):

- [Skill definition](artifact/SKILL.md)
- [Meta-analysis friendly SCI journal database](artifact/journal_database.md)
- [Verified JCR and CAS journal data](artifact/jcr_verified_data.csv)
- [PROSPERO](https://www.crd.york.ac.uk/prospero/)
- [Clarivate Master Journal List](https://mjl.clarivate.com/)
- [Directory of Open Access Journals](https://doaj.org/)
- [Think. Check. Submit.](https://thinkchecksubmit.org/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables, checklists, decision guidance, and follow-up recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tiered Reach/Target/Safety journal recommendations, compliance checks, desk-rejection risk notes, cost and timeline estimates, and cover-letter guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
