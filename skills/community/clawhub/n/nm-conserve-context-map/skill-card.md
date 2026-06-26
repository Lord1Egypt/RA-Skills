## Description: <br>
Generates a compressed project context map to avoid expensive Read/Grep calls for session startup or feature work in an unfamiliar codebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to build a compact project overview before making changes in an unfamiliar repository. It helps identify structure, dependencies, entry points, routes, environment variable references, models, middleware, and high-blast-radius files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may activate repository-wide scanning on vague requests. <br>
Mitigation: Use the skill deliberately when broad project context scanning is appropriate. <br>
Risk: The generated context map may expose project structure, route names, schema names, and environment variable names from the local repository. <br>
Mitigation: Review the generated map before sharing it outside the intended workspace or team. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-conserve-context-map) <br>
- [Conserve plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Files] <br>
**Output Format:** [Markdown project context map, optional JSON output, and optional .codesight Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is capped by --max-tokens, with section-specific and blast-radius modes available.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
