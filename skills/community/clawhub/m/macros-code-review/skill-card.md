## Description: <br>
Reviews Rust macro code for hygiene issues, fragment misuse, compile-time impact, and procedural macro patterns when reviewing macro_rules! definitions, procedural macros, derive macros, or attribute macros. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to structure Rust macro code reviews for declarative macros, procedural macros, derive macros, and attribute macros. It guides checks for hygiene, fragment matching, span handling, error reporting, compile-time cost, and edition-specific generated code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to inspect Rust project files during macro review. <br>
Mitigation: Use it only in repositories where agent access to relevant source code is acceptable. <br>
Risk: The pre-report gate references a separate review-verification-protocol skill. <br>
Mitigation: Install or otherwise provide that referenced skill before relying on the final verification gate. <br>


## Reference(s): <br>
- [Declarative Macros](artifact/references/declarative-macros.md) <br>
- [Procedural Macros](artifact/references/procedural-macros.md) <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/macros-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text review findings with file-line citations and severity labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should include [FILE:LINE], severity, and a concise description; no findings are emitted until the verification gates pass.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
