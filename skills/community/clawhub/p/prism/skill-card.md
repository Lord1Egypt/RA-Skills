## Description: <br>
Use PRISM when reviewing architecture decisions, security-sensitive changes, major refactors, long-lived decisions, open source releases, or when structured adversarial analysis is needed to reduce groupthink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremyknows](https://clawhub.ai/user/jeremyknows) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use Prism to run structured multi-agent code and architecture reviews with specialist reviewers, evidence requirements, synthesis, and local review history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Multiple configured agents may read relevant project files and save local review summaries. <br>
Mitigation: Install Prism only in repositories where this access pattern is acceptable, use explicit review targets, and avoid archiving secrets. <br>
Risk: Local review summaries can accumulate in analysis/prism/archive/. <br>
Mitigation: Periodically clean analysis/prism/archive/ and apply the documented retention policy when archives grow. <br>
Risk: A local sub-agent completion helper may be used during review completion. <br>
Mitigation: Ensure the local helper is trusted before using Prism in sensitive repositories. <br>


## Reference(s): <br>
- [PRISM Evidence Rules](references/evidence-rules.md) <br>
- [PRISM Orchestration Reference](references/orchestration.md) <br>
- [PRISM Archive Retention Policy](references/archive-retention-policy.md) <br>
- [Example PRISM v2 Review](references/example-review.md) <br>
- [Prism on ClawHub](https://clawhub.ai/jeremyknows/prism) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review synthesis with cited findings, verdicts, and inline shell commands or file path changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local review summaries under analysis/prism/archive/ for future review context.] <br>

## Skill Version(s): <br>
2.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
