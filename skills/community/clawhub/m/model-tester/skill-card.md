## Description: <br>
Test agents or models against predefined test cases to validate model routing, performance, and output quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nandorocker](https://clawhub.ai/user/nandorocker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run repeatable model and agent tests, compare requested versus actual model routing, and capture structured results for debugging fallback chains or output quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes OpenClaw agents or models under the user's current account. <br>
Mitigation: Run it only when those account-level model calls are expected and authorized. <br>
Risk: The skill briefly reads OpenClaw logs to extract model-routing and token-usage fields. <br>
Mitigation: Run it when unrelated sensitive OpenClaw activity is not active, and review custom test cases before use. <br>


## Reference(s): <br>
- [Predefined test cases](references/test-cases.json) <br>
- [ClawHub release page](https://clawhub.ai/nandorocker/model-tester) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON results with a short human-readable terminal summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally write the JSON result to a file when --out is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
