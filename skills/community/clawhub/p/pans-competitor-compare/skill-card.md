## Description:

Compares static GPU instance pricing and specifications across AWS, GCP, Azure, Volcengine, and Alibaba Cloud with filters for GPU model, provider, region, and output format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sales engineers, and cloud cost analysts use this skill to compare GPU cloud instance options and export pricing or specification data for vendor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static pricing data may be stale or differ from current provider quotes.

Mitigation: Verify current cloud-provider pricing before using the comparison for purchasing or budgeting decisions.

Risk: The tool can write an output file when a user supplies --output.

Mitigation: Choose an intended output path and review generated JSON or CSV files before reuse.

## Reference(s):

- [GPU Pricing Reference Data](references/gpu_pricing.md)

## Skill Output:

**Output Type(s):** [text, json, csv, files, shell commands]

**Output Format:** [Plain text tables, JSON arrays, or CSV, with optional file export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static pricing data last updated April 2026; results can be filtered by GPU model, provider, region, and output mode.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
