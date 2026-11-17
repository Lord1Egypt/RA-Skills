## Description:

SaMD (Software as a Medical Device) skill — IMDRF N12 risk classification (I-IV), IEC 62304 software lifecycle (A/B/C), FDA level of concern (Major/Moderate/Minor), MDR Rule 11, cybersecurity (MDCG 2019-16, FDA guidance, SBOM) checklists with official references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

External medical-device software teams and regulatory professionals use this skill to assess SaMD classification and organize software lifecycle, cybersecurity, and usability documentation against relevant regulatory frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regulatory guidance and classifications may change or depend on product-specific facts.

Mitigation: Use the skill as a documentation aid and check current official sources before making regulatory decisions.

Risk: The package's bundled security audit, scores, and ownership fingerprint are inconsistent and are not reliable assurance for this release.

Mitigation: Do not rely on those bundled assurances when assessing this release.

Risk: Running the optional checker overwrites security_results.json in the selected directory.

Mitigation: Run it only in a disposable copy if a fresh local report is needed.

## Reference(s):

- [SaMD Knowledge Base](references/SaMD知识库.md)
- [Publisher homepage](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/medical-device-samd)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Checklists, Markdown]

**Output Format:** [Markdown guidance with classification assessments, compliance checklists, and official reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
