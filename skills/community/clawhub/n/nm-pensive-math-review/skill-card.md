## Description: <br>
Verifies math-heavy code for algorithmic correctness and numerical stability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review mathematical, scientific, ML, and numerical code for algorithmic correctness, derivation quality, numerical stability, and test evidence before accepting changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested pytest, benchmark, or notebook commands may execute code from the local project. <br>
Mitigation: Review commands before execution and run them in an appropriate project sandbox or trusted checkout. <br>
Risk: Mathematical review findings can be incomplete or overly confident if requirements, derivations, tolerances, or reference implementations are missing. <br>
Mitigation: Require cited evidence, explicit assumptions, documented tolerances, and human review for safety-critical, financial, ML fairness, or scientific claims. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-math-review) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [Configured homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>
- [Requirements mapping module](modules/requirements-mapping.md) <br>
- [Derivation verification module](modules/derivation-verification.md) <br>
- [Numerical stability module](modules/numerical-stability.md) <br>
- [Testing strategies module](modules/testing-strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with tables, issue entries, recommendations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local pytest, benchmark, and notebook execution commands for reviewer approval.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
