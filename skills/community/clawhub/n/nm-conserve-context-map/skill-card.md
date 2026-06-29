## Description: <br>
Generates a compressed project context map to help agents understand an unfamiliar codebase before deeper file reads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill at the start of a session or before implementation work to scan a repository, identify structure, entry points, dependencies, routes, environment variables, hot files, and likely token savings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner runs over the current repository and may produce local context files. <br>
Mitigation: Install only in trusted codebases, review generated context before relying on it, and use --no-wiki or avoid --output when local files should not be created. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-context-map) <br>
- [Conserve plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON project context map with optional local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .codesight/ wiki files or a user-specified output file when those options are used.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
