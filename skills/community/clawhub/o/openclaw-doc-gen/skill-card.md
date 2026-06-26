## Description: <br>
Generates documentation from code, including API docs, README updates, architecture diagrams, and documentation sync checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate and maintain project documentation from source code, including API references, README tables of contents, architecture diagrams, and documentation freshness checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation or README changes may be inaccurate or may not match the intended project state. <br>
Mitigation: Run on a clean branch, inspect generated README.md and documentation changes before committing, and review the output against the source code. <br>
Risk: The CI example can push documentation changes directly if used without safeguards. <br>
Mitigation: Use branch protections and a restricted workflow token before enabling direct-push automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/openclaw-doc-gen) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, Mermaid or DOT diagram text, README edits, and console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update README.md and docs files in the target project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
