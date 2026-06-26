## Description: <br>
Generate isolated dev, test, and production environments for uvicorn/FastAPI Python web projects with Vue or React frontend support, including separate configs, startup scripts, data directories, Playwright integration, and setup documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rm-huang](https://clawhub.ai/user/rm-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scaffold isolated dev, test, and production workflows for FastAPI/uvicorn projects with optional Vue or React frontends. It is intended for projects that need separate ports, configuration files, data directories, startup scripts, and Playwright E2E test setup so parallel development and testing do not conflict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated environment files include placeholder secrets that are not suitable for production. <br>
Mitigation: Replace every placeholder secret, especially production JWT secrets, before real production use. <br>
Risk: The setup modifies a target project by creating local configuration, scripts, data directories, and documentation. <br>
Mitigation: Run the skill only on the intended repository and inspect generated .env and shell scripts before execution. <br>
Risk: Generated frontend scripts may run npm install when node_modules is missing. <br>
Mitigation: Review frontend package files before allowing generated scripts to install dependencies. <br>


## Reference(s): <br>
- [Configuration Options Reference](references/config-options.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/rm-huang/multi-env-isolator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with generated Python, shell, environment, and Playwright configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces files in the target repository, including .env files, startup scripts, data directories, docs, and optional frontend test configuration.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
