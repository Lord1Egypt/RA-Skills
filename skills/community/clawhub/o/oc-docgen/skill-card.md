## Description: <br>
Generates documentation from code, including API docs, README updates, architecture diagrams, and documentation sync checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate and refresh project documentation from source code, including API references, README sections, diagrams, and sync reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation or README updates can modify repository files. <br>
Mitigation: Run the skill on a branch or test copy first and review generated diffs before committing. <br>
Risk: The CI example can push generated documentation changes if copied into automation. <br>
Mitigation: Use the push workflow only when intentional, with limited credentials and normal code review controls. <br>
Risk: Generated documentation can be incomplete or misleading if source parsing misses behavior. <br>
Mitigation: Review generated docs against the source code before publishing or relying on them. <br>


## Reference(s): <br>
- [OpenClaw Doc Generator on ClawHub](https://clawhub.ai/michealxie001/oc-docgen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, generated documentation files, Mermaid or DOT diagram text, configuration examples, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated docs or README updates to the target repository when invoked with output or update options.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
