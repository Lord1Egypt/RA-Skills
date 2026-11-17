## Description:

Assess the current PHI Readiness Stage (PRS) of a workload, repository, system, or environment; determine HIPAA applicability and role; identify evidence gaps; and recommend next actions using official HHS/OCR and NIST sources with conservative evidence caps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickzren](https://clawhub.ai/user/nickzren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, compliance reviewers, and product teams use this skill to assess a workload's PHI readiness stage, identify evidence gaps, and prioritize next actions without overstating legal status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assessment evidence may include PHI or confidential compliance records.

Mitigation: Use redacted screenshots, evidence pointers, and approved internal storage instead of pasting raw PHI or confidential records into chat.

Risk: PRS findings could be mistaken for a legal determination or compliance certification.

Mitigation: Keep conclusions scoped to the workload and use the skill's required caveats against saying HIPAA compliant, HIPAA certified, or HIPAA secure.

Risk: Stale, indirect, or repo-only evidence can overstate readiness.

Mitigation: Apply the evidence freshness rules and conservative stage caps, and record missing approval or live operational evidence as blockers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickzren/skills/phi-readiness-stages)
- [Project homepage](https://github.com/nickzren/phi-readiness-stages)
- [PHI Readiness Stages README](README.md)
- [PRS assessment workflow](skills/phi-readiness-review/SKILL.md)
- [Assessment evidence handling](framework/assessment-evidence-handling.md)
- [Stage rubric](framework/stage-rubric.md)
- [Output contract](framework/output-contract.md)
- [Official source registry](references/source-registry.md)
- [HHS HIPAA Security Rule overview](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [45 CFR Part 164 regulation text](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164)
- [NIST SP 800-66 Rev. 2](https://csrc.nist.gov/pubs/sp/800/66/r2/final)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown assessment report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scoped summary, applicability and role analysis, evidence review, source verification, PRS stage assignment, domain findings, recommended actions, caveats, and regulatory boundary notes.]

## Skill Version(s):

1.1.0 (source: frontmatter, changelog, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
