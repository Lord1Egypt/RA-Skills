## Description:

Mingxi Analyzer provides a Chinese-language structured analysis workflow for system diagnosis, contradiction analysis, game-scenario reasoning, policy interpretation, content evaluation, confidence labeling, and judgment review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[122201](https://clawhub.ai/user/122201)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to guide complex analysis tasks through explicit routing, evidence collection, framework selection, confidence labeling, failure conditions, and follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The judgment tracker can persist local analysis records and import previous records from /tmp/judgment_tracker.

Mitigation: Review or clear existing tracker data before use, avoid recording secrets or sensitive business details, and restrict access to the local tracker database.

Risk: The release evidence marks the security verdict as suspicious because local record handling lacks clear user control and permission hardening.

Mitigation: Use the analysis workflow without the tracker when persistence is not needed, or inspect the tracker script and storage path before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/122201/skills/mingxi-analyzer)
- [TCR task routing](references/00-tcr.md)
- [Core principles](references/00-core-principles.md)
- [OCGS system diagnosis](references/01-ocgs.md)
- [Five-layer reasoning](references/02-five-layer.md)
- [Contradiction analysis](references/03-contradiction.md)
- [Policy signal interpretation](references/04-policy-signal.md)
- [Six-prism content evaluation](references/05-six-prism.md)
- [Credibility levels](references/06-credibility.md)
- [Safety gates](references/07-safety-gates.md)
- [Judgment tracker](references/08-judgment-tracker.md)
- [Review template](references/09-review-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis templates and structured prose, with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include confidence labels, failure conditions, review dates, and judgment-tracker records.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
