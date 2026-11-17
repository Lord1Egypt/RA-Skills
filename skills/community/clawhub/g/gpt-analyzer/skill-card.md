## Description:

GPT-specific pattern detection with model fingerprinting and version identification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi)

### License/Terms of Use:


## Use Case:

Developers, reviewers, and content analysts use this skill to estimate whether text shows GPT-like phrasing, structure, and model-specific indicators. It returns heuristic confidence, model-family labels, scores, and recommendations for downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The detector may create false positives or overstate authorship because it relies on GPT-like phrases, structure, and confidence thresholds.

Mitigation: Use the result as a review signal only, corroborate with additional evidence, and avoid making authorship or enforcement decisions from this output alone.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raghulpasupathi/skills/gpt-analyzer)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JavaScript object with JSON-compatible analysis fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a configurable confidence threshold; results are heuristic and should not be treated as proof of authorship.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
