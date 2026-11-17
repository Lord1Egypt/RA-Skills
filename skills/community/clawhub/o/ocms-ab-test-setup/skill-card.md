## Description:

Helps agents plan, design, implement, and document statistically rigorous A/B tests and experiments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boleyn](https://clawhub.ai/user/boleyn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, marketers, and product teams use this skill to structure A/B test hypotheses, choose metrics, estimate sample size, plan traffic allocation, prepare launch checklists, and document experiment results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad experiment or hypothesis wording may activate the skill when the user does not intend a formal A/B test.

Mitigation: Confirm the user wants experiment planning before applying sample size, metric, or launch guidance.

Risk: Optional local product marketing context can influence recommendations if that context is stale or incomplete.

Mitigation: Review the relevant product context and ask only for missing test-specific details before finalizing recommendations.

Risk: Experiment decisions may be misleading when sample size, primary metric, or stopping rules are not set up front.

Mitigation: Predefine the hypothesis, primary metric, sample size, duration, and guardrail metrics before launching or interpreting a test.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/boleyn/skills/ocms-ab-test-setup)
- [Sample Size Guide](references/sample-size-guide.md)
- [A/B Test Templates Reference](references/test-templates.md)
- [Evan Miller A/B Test Sample Size Calculator](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely Sample Size Calculator](https://www.optimizely.com/sample-size-calculator/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with checklists, tables, formulas, and experiment templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use optional local product marketing context when present; no code execution or credential handling is described in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
