## Description: <br>
Verifies math-heavy code for algorithmic correctness and numerical stability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review mathematical, scientific, statistical, numerical, and ML code for correctness, stability, reproducibility, and standards alignment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to run tests, benchmarks, or notebooks from an unfamiliar repository. <br>
Mitigation: Run those commands only in a sandboxed environment after reviewing the tests, benchmark setup, and notebooks. <br>
Risk: Mathematical review output can be incomplete or wrong if source requirements, formulas, or standards are missing. <br>
Mitigation: Require cited evidence, documented assumptions, and human review before relying on the recommendation for safety-critical, financial, or regulatory decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-math-review) <br>
- [Pensive plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review with summary, context, requirements analysis, derivation review, stability analysis, issue entries, and a recommendation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include verification commands and a recommendation of Approve, Approve with actions, or Block.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
