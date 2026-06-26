## Description: <br>
Helps agents design, apply, and evaluate context compression strategies for long-running sessions, large codebases, and token-efficient continuation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lidekahdjdhdhsjjs-lang](https://clawhub.ai/user/lidekahdjdhdhsjjs-lang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to choose context compression strategies, design structured summaries, and evaluate whether compressed context preserves artifacts, decisions, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summaries can preserve sensitive information from long-running sessions. <br>
Mitigation: Avoid placing secrets or regulated data in compressed summaries, and review summary contents before sharing them outside the trusted workspace. <br>
Risk: External judge evaluation can expose compacted context to another provider or data flow. <br>
Mitigation: Use external judges only when the provider and data handling path are approved for the data being evaluated. <br>
Risk: The bundled evaluator uses stubbed judge calls, simplified token estimation, and pattern-based ground-truth extraction. <br>
Mitigation: Treat the evaluator as a local evaluation scaffold and replace stubs, tokenization, and extraction logic before relying on it for production-quality measurements. <br>


## Reference(s): <br>
- [Context Compression Evaluation Framework](references/evaluation-framework.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lidekahdjdhdhsjjs-lang/hz-context-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with optional Python evaluation code and JSON-style evaluation structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured summary sections, probe questions, scoring rubrics, and context-compression implementation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
