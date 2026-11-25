## Description:

Batch-computes CDC 2000 growth z-scores and percentiles for child-measurement CSV files.

This skill is for research and development only.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and educators use GrowthZ to process child-measurement files for cohorts or surveys and calculate CDC growth-chart results in batches. It reports calculations and data-quality notes without diagnosis or clinical interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guide uses an unpinned GitHub source that could run code during installation; ClawScan reports this as suspicious with medium confidence and does not establish malicious intent.

Mitigation: Review the source and install from a specific audited revision or verified package in an isolated environment without sensitive files or credentials.

Risk: GrowthZ provides arithmetic results only; incorrect or out-of-range measurements and the CDC reference population may be misunderstood as clinical assessment.

Mitigation: Verify inputs and outputs, heed data-quality flags and notes, and do not use the results as diagnosis or clinical advice.

## Reference(s):

- [GrowthZ on ClawHub](https://clawhub.ai/raktikoo/skills/growthz)
- [GrowthZ source repository and installation source](https://github.com/RakTikoo/growthz)

## Skill Output:

**Output Type(s):** [Files, Analysis]

**Output Format:** [CSV with input columns, computed z-scores and percentiles, data-quality flags, and notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves input columns; row-level data issues are recorded without stopping processing.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
