## Description: <br>
Assess the current PHI Readiness Stage (PRS) of a workload, repository, system, or environment; determine HIPAA applicability and role; identify evidence gaps; and recommend next actions using official HHS/OCR and NIST sources with conservative evidence caps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickzren](https://clawhub.ai/user/nickzren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, compliance teams, and product teams use this skill to assess a workload's PRS stage, identify PHI-readiness evidence gaps, and recommend next actions without treating PRS as a legal determination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assessment evidence may contain PHI or sensitive operational details. <br>
Mitigation: Use redacted evidence, record pointers, and approved storage paths; avoid placing raw PHI into prompts, tickets, reports, or public documentation. <br>
Risk: HIPAA guidance or enforcement posture may change after the packaged baseline was curated. <br>
Mitigation: Verify official HHS/OCR, eCFR, and NIST sources live before making current regulatory statements and record the access date. <br>
Risk: A PRS assessment can be overstated as legal approval or certification. <br>
Mitigation: Use the skill's required caveats and safe public wording; do not label a workload as HIPAA compliant, HIPAA certified, or HIPAA secure. <br>
Risk: Missing or stale evidence can lead to an unsupported stage assignment. <br>
Mitigation: Apply conservative evidence caps, identify blockers explicitly, and recommend the next evidence artifacts needed for the next stage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickzren/phi-readiness-stages) <br>
- [Project homepage](https://github.com/nickzren/phi-readiness-stages) <br>
- [Official Source Registry](references/source-registry.md) <br>
- [Current Baseline](references/current-baseline.md) <br>
- [Assessment Evidence Handling](framework/assessment-evidence-handling.md) <br>
- [Output Contract](framework/output-contract.md) <br>
- [HIPAA Security Rule Crosswalk](mappings/hipaa-security-rule-crosswalk.md) <br>
- [NIST SP 800-66 Rev. 2 Mapping](mappings/nist-800-66-r2.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown assessment report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scoped evidence review, official-source verification records, PRS stage assignment, blockers, ordered recommendations, caveats, and safe public wording.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
