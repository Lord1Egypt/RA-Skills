## Description: <br>
Systematic debug and root cause investigation framework that guides agents through investigation, analysis, hypothesis, verification, and root-cause fixes for bugs, abnormal behavior, and service errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate software bugs and service failures before proposing fixes. It emphasizes evidence collection, reproducible hypotheses, regression tests, and a structured debug report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging workflows may inspect repository contents, logs, stack traces, git history, and test output that contain sensitive information. <br>
Mitigation: Use it only in repositories the agent is allowed to inspect, and review logs, traces, history, and test output for secrets before sharing them externally. <br>
Risk: A proposed fix can address symptoms instead of the verified root cause or introduce regressions. <br>
Mitigation: Require reproduction evidence, a confirmed root-cause hypothesis, a regression test, and test-suite output before treating the fix as complete. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown guidance with inline shell commands, code references, and structured debug reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include root-cause hypotheses, verification evidence, regression test recommendations, status labels, and requests for user input when investigation scope is high.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
