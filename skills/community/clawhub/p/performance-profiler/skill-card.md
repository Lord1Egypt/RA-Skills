## Description: <br>
Analyzes code performance to identify bottlenecks, redundant calculations, synchronous blocking operations, and memory-leak risks, then provides optimization recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HonestQiao](https://clawhub.ai/user/HonestQiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to review code for common performance issues and receive concise optimization guidance before changing implementation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as 'performance' or '优化建议' may invoke the skill during unrelated requests. <br>
Mitigation: Narrow trigger configuration before broad deployment so invocation is limited to explicit code performance review tasks. <br>
Risk: Performance findings are heuristic and may be incomplete or unsuitable for a specific codebase. <br>
Mitigation: Treat recommendations as review guidance and validate them with maintainers, tests, and benchmarks before implementation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HonestQiao/performance-profiler) <br>
- [Publisher Profile](https://clawhub.ai/user/HonestQiao) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Markdown or JSON-style findings with issue type, location when available, recommendation, complexity, and score.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and should be reviewed before code changes are applied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
