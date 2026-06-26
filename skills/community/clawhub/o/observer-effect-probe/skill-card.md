## Description: <br>
Helps agents detect skills that change behavior when they sense monitoring, targeting attestation and sandbox evasion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and trust-and-safety teams use this skill to probe other skills for observer-aware behavior, sandbox fingerprinting, timing sensitivity, and context-dependent evasion signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Probing another skill can involve generated shell commands or network requests such as curl or python3 execution. <br>
Mitigation: Review proposed commands before running them and execute probes only in isolated environments without real credentials. <br>
Risk: A clean observer-effect result does not prove that no evasion logic exists. <br>
Mitigation: Treat results as evidence from the tested environments and combine them with other security review methods. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/observer-effect-probe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with probe findings, behavioral comparisons, scores, verdicts, and recommended actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed curl or python3-based probing steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
