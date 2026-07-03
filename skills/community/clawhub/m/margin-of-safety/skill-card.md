## Description: <br>
Helps agents audit uncertain commitments by estimating downside scenarios, choosing a margin of safety, and checking whether the commitment still survives adverse outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and agents use this skill to size buffers for budgets, timelines, investments, runway, capacity, or other commitments where estimates may be wrong. It is intended as structured reasoning support, not a substitute for professional financial, engineering, or legal review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat margin-of-safety outputs as professional financial, engineering, or legal advice for high-stakes commitments. <br>
Mitigation: Use the output as structured reasoning support and have qualified reviewers validate assumptions before committing capital, capacity, timelines, or legal obligations. <br>
Risk: Incorrect point estimates, base rates, or uncertainty bounds can produce misleading buffer recommendations. <br>
Mitigation: Require explicit estimate methods, adverse scenarios, historical base-rate checks, and stress tests before relying on a recommended margin. <br>


## Reference(s): <br>
- [Sources - margin-of-safety](references/sources.md) <br>
- [Graham's 1934 Framework and Buffett's Lifelong Application](examples/grahams-1934-framework-and-buffetts-lifelong-application.md) <br>
- [Berkshire Hathaway Annual Letters to Shareholders](https://www.berkshirehathaway.com/letters/letters.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Analysis] <br>
**Output Format:** [Markdown audit with structured fields for estimates, adverse scenarios, margin choice, discipline check, and stress-test results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask clarifying questions and stop for user input before completing the audit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
