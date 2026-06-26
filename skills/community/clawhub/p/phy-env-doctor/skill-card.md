## Description: <br>
Scans codebases to discover environment variables, generate a documented .env.example, compare against current .env files, and flag secret-handling risks across Node.js, Python, Go, Ruby, and shell scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit a local codebase for environment variable usage, missing or undocumented settings, and secret-handling issues before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans local project files and may surface sensitive environment-variable names, secret-like strings, or configuration details in its report. <br>
Mitigation: Run it only in the intended repository and treat the resulting report and generated files as sensitive project material. <br>
Risk: Generated .env.example content and suggested cleanup commands may not fully match project-specific deployment requirements. <br>
Mitigation: Review generated files and proposed commands before applying them or committing changes. <br>


## Reference(s): <br>
- [Phy Env Doctor on ClawHub](https://clawhub.ai/PHY041/phy-env-doctor) <br>
- [Canlah AI](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and generated .env.example content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include issue tables, inferred environment-variable descriptions, generated .env.example content, and suggested cleanup commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
