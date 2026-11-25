## Description:

Batch-convert lab-result CSV columns or single values between conventional (US) and SI units, recording the conversion factor or formula and refusing analytes without a verified fixed conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Lab-data analysts use the skill to convert selected lab values or CSV columns between conventional and SI units while retaining the conversion details for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from the repository carries supply-chain risk, and declaring the wrong source unit system can produce incorrect conversions.

Mitigation: Review and pin the repository before installation, install without access to sensitive data or credentials, specify the source and target systems explicitly, and check a known value by hand before relying on results.

Risk: Converted values could be mistaken for clinical interpretation or treated as a medical device output.

Mitigation: Verify converted values against the laboratory's own reporting before clinical use; the skill provides no reference ranges or interpretation.

## Reference(s):

- [Lab Units ClawHub release](https://clawhub.ai/raktikoo/skills/labunits)
- [Lab Units installation repository](https://github.com/RakTikoo/labunits)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [CSV files with converted value and factor columns; plain-text conversion results and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves input columns and records the exact factor or formula used.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
