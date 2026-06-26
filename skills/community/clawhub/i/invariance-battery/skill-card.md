## Description: <br>
Runtime assertion guidance for continuously checking AI agent invariants, detecting drift, enforcing safety constraints, and reporting falsification results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design invariant checks for autonomous agents, audit drift from design intent, and plan falsification reporting for safety-critical behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: If the instructional action-blocking pattern is adapted into automation, overly broad or stale invariants could halt legitimate agent actions. <br>
Mitigation: Test invariants before enforcement, document expected failures, and provide a clear human review or override path. <br>
Risk: If the audit-trail concept is implemented, logs may capture sensitive agent state, prompts, actions, or decisions. <br>
Mitigation: Review log storage, access controls, retention, and redaction before recording runtime checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/invariance-battery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No commands are executed; the skill provides concepts and example patterns for invariant definitions, runtime checks, drift detection, and falsification reporting.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
