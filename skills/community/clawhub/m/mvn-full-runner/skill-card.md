## Description: <br>
Run Maven commands with full argument passthrough, optionally specifying the working directory through a Node.js wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyongm](https://clawhub.ai/user/yuanyongm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent run Maven goals, plugins, profiles, and flags in a selected project directory while preserving Maven's normal command behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maven goals, plugins, profiles, and -D options can run build logic with the same effects as a direct mvn command. <br>
Mitigation: Review requested Maven arguments before execution, especially for sensitive or untrusted projects. <br>
Risk: The optional --dir argument changes the project directory where Maven runs. <br>
Mitigation: Confirm the target directory is the intended project before running the wrapper. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyongm/mvn-full-runner) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and Maven console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Maven in PATH; forwards all non-wrapper arguments directly to mvn.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
