## Description: <br>
Provides scripts and guidance for testing OpenClaw skills across trigger behavior, functional outputs, and comparison metrics. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[cry779](https://clawhub.ai/user/cry779) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers can use this as a scaffold for checking whether OpenClaw skills trigger in expected situations, return expected output shapes, and report comparison metrics. Treat the generated reports as examples until the scripts are connected to real target skill execution and measured results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated pass/fail reports and comparison metrics may be simulated or hard-coded rather than based on real target skill execution. <br>
Mitigation: Use the skill as a scaffold only until scripts execute real skills, propagate actual exit codes, and build reports from collected test results. <br>
Risk: Teams may over-trust the reports for CI, quality, security, or deployment decisions. <br>
Mitigation: Require independent review and real validation data before using results as release or deployment gates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cry779/openclaw-skill-tester) <br>
- [Publisher profile](https://clawhub.ai/user/cry779) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON or Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and bash; package metadata lists pytest and requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
