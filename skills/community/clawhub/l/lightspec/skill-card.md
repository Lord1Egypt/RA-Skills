## Description: <br>
AI-native spec-driven development tool. Create, manage, and apply specifications with your agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcoleongdev](https://clawhub.ai/user/marcoleongdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use LightSpec to set up and run spec-driven development workflows with an agent, including creating, validating, reviewing, and applying feature specs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing LightSpec uses a global third-party npm CLI. <br>
Mitigation: Install only when the user trusts the LightSpec npm package and verify installation with lightspec --version. <br>
Risk: LightSpec commands can modify project files, including AGENTS.md and generated specification files. <br>
Mitigation: Confirm before running file-changing commands such as lightspec init and lightspec apply, then review the resulting changes. <br>


## Reference(s): <br>
- [LightSpec on ClawHub](https://clawhub.ai/marcoleongdev/lightspec) <br>
- [LightSpec repository](https://github.com/augmenter-dev/lightspec) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may involve file-changing LightSpec commands such as init and apply; user confirmation is recommended before modifying a project.] <br>

## Skill Version(s): <br>
0.6.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
