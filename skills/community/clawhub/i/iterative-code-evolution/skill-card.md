## Description: <br>
Systematically improve code through structured analysis-mutation-evaluation loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronjmars](https://clawhub.ai/user/aaronjmars) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to improve code through structured analyze, plan, mutate, verify, score, and archive cycles. It is intended for optimization, persistent debugging, and disciplined design evolution after initial attempts have not been sufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for development workspaces where an agent may edit files, run tests or code, and maintain an .evolution/ history. <br>
Mitigation: Install it only in trusted workspaces, keep normal sandboxing and approval controls active for sensitive repositories, and review generated changes before accepting them. <br>
Risk: Iterative mutations can introduce regressions or misleading guidance if changes are accepted without verification. <br>
Mitigation: Use the skill's verify and score phases, compare each variant against its parent, and preserve failure notes in the evolution log. <br>


## Reference(s): <br>
- [ALMA research framework](https://yimingxiong.me/alma) <br>
- [ClawHub skill page](https://clawhub.ai/aaronjmars/iterative-code-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code, shell commands, and JSON logging structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local .evolution/ history when applied in a development workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
