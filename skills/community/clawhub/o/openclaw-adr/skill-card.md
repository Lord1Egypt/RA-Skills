## Description: <br>
Architecture Decision Records (ADR) management. Creates, updates, and tracks architectural decisions with templates and linting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to create, list, update, and lint Architecture Decision Records in a repository using a MADR-style Markdown format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Create and update commands write Markdown files under docs/adr for the selected repository root. <br>
Mitigation: Run the skill from the intended repository root and use --root carefully before allowing file writes. <br>
Risk: The documentation mentions index and configuration behavior that is not implemented in this artifact version. <br>
Mitigation: Use the implemented create, list, update, and lint commands, and verify generated ADR indexes or configuration behavior manually. <br>
Risk: Generated ADR files contain placeholder decision content. <br>
Mitigation: Review and complete the generated ADR before treating it as an accepted architectural decision. <br>


## Reference(s): <br>
- [MADR](https://adr.github.io/madr/) <br>
- [OpenClaw ADR on ClawHub](https://clawhub.ai/michealxie001/openclaw-adr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown ADR files and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local files under docs/adr in the selected project root.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
