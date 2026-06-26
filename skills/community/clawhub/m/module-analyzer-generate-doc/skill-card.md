## Description: <br>
Java/Maven single-module deep documentation generator that creates L3 file-level and L2 module-level business logic documentation with parallel subagent processing, context compression, checkpoint resume, and retry support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[endcy](https://clawhub.ai/user/endcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze a single Java/Maven module and generate source-derived L3 file documentation plus an L2 module overview. The generated documentation explains business responsibilities, flows, dependencies, configuration, and skip decisions in human-facing prose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Java module source files and creates documentation, logs, and checkpoint files in the project. <br>
Mitigation: Run it on a controlled branch and review generated files before committing or sharing them. <br>
Risk: Server security evidence flags inconsistent guidance about shell fallbacks and security-restricted file access. <br>
Mitigation: Follow platform file access restrictions, require confirmation before migrations, overwrites, or cleanup, and do not run the package.json PowerShell generate script unless the missing helper script is supplied and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/endcy/module-analyzer-generate-doc) <br>
- [L2 module documentation template](references/l2-module-template.md) <br>
- [L3 file documentation template](references/l3-file-template.md) <br>
- [Task execution guide](references/task-execution-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation and execution guidance with command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces source-derived L3 file docs, an L2 module overview, progress logs, and checkpoint state under .ai-doc when run.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
