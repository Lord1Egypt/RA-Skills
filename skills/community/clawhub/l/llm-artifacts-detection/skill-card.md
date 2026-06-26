## Description: <br>
Detects common LLM coding agent artifacts in codebases, including test quality issues, dead code, over-abstraction, and verbose LLM style patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill during code review or cleanup to identify AI-generated code quality issues and produce evidence-bound findings with file and line anchors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review findings may be inaccurate or misleading if an agent infers issues without reading the relevant code. <br>
Mitigation: Require every finding to include a freshly verified FILE:LINE anchor, a plain-language defect title, and deduplication by root cause. <br>
Risk: The skill asks an agent to inspect repository contents, which may expose sensitive code to the reviewing agent or its runtime. <br>
Mitigation: Use it only in environments approved for the target codebase and review findings before acting on them. <br>


## Reference(s): <br>
- [LLM Artifacts Detection release page](https://clawhub.ai/anderskev/llm-artifacts-detection) <br>
- [Abstraction Criteria](references/abstraction-criteria.md) <br>
- [Dead Code Criteria](references/dead-code-criteria.md) <br>
- [Style Criteria](references/style-criteria.md) <br>
- [Test Quality Criteria](references/tests-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown findings with FILE:LINE anchors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to be anchored to freshly read source buffers and deduplicated by file, line, and root cause.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
