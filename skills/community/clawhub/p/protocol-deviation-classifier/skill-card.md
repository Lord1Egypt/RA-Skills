## Description:

Classifies clinical trial protocol deviations as major, minor, or critical and provides advisory risk rationale, regulatory references, and recommended actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ewankeynes](https://clawhub.ai/user/ewankeynes)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical quality, compliance, and trial operations teams use this skill to classify protocol deviation events and generate advisory JSON or text reports for review. Outputs should support, not replace, clinical QA and regulatory decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical compliance outputs may understate serious deviations when risk-factor inputs are missing or malformed.

Mitigation: Treat results as advisory and require clinical QA review before using classifications in quality, reporting, or regulatory workflows.

Risk: The dependency installation step is unnecessary and unpinned.

Mitigation: Avoid running the pip install step until the dependency list is fixed or removed, and review dependencies before installation.

Risk: Downstream processes that expect only major or minor labels may mishandle critical classifications.

Mitigation: Require consuming workflows to explicitly handle critical, major, and minor outputs before automation is enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ewankeynes/skills/protocol-deviation-classifier)
- [Artifact skill documentation](artifact/SKILL.md)
- [Classifier implementation](artifact/scripts/main.py)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [JSON classification results, summary reports, CLI table text, and Python API objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence scores, rationale, risk factors, regulatory basis entries, and recommended actions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
