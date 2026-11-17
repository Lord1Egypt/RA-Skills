## Description:

This skill normalizes testing engineers' written defect reasons against supplied product codebooks, correcting typos, abbreviations, ambiguous or mixed Chinese-English text, and applying segmentation, semantic matching, confidence calibration, and station validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing quality engineers and agent developers use this skill to map noisy test-center failure reason text to product-codebook codes, labels, rationales, and calibrated confidence values. It supports station-scoped validation and UNKNOWN handling when evidence is weak.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manufacturing logs and product codebooks may contain sensitive operational or product information.

Mitigation: Confirm that the data can be processed by the target agent environment before installing or using the skill.

Risk: Incorrect normalization can assign the wrong failure code or label, especially when evidence is weak or ambiguous.

Mitigation: Use the skill's UNKNOWN path for weak matches and review the rationale, confidence, station, fail_code, and test_item signals before relying on outputs operationally.

Risk: Station-scoped codes can be misapplied when the record station does not match the codebook entry.

Mitigation: Reject station-incompatible candidates and only select codes whose station scope matches the record when a station scope is defined.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Structured text with one normalized prediction per segment, including pred_code, pred_label, rationale, confidence, and UNKNOWN when evidence is weak.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Confidence is rounded to 4 decimals and requires user-supplied manufacturing logs and product codebooks.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
