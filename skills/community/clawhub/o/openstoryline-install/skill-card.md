## Description: <br>
Installs, configures, verifies, and starts FireRed-OpenStoryline from source on macOS, Linux, or WSL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anlittledy](https://clawhub.ai/user/Anlittledy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to set up or repair a local FireRed-OpenStoryline checkout, including prerequisites, Python environment setup, resource downloads, config.toml API key settings, and MCP and web service startup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing dependencies and running download.sh executes upstream project setup behavior. <br>
Mitigation: Install only when the upstream FireRed-OpenStoryline project is trusted, and review requirements.txt and download.sh before running them. <br>
Risk: Setup may require package-manager or sudo commands for missing system dependencies. <br>
Mitigation: Require explicit approval before running privileged or package-manager commands. <br>
Risk: API keys written to config.toml can be exposed if committed, shared, or logged. <br>
Mitigation: Treat config.toml credentials as secrets and avoid committing, sharing, or logging them. <br>
Risk: Starting MCP or web services on externally reachable interfaces can expose local services unintentionally. <br>
Mitigation: Keep services bound to 127.0.0.1 unless external access is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Anlittledy/openstoryline-install) <br>
- [Publisher profile](https://clawhub.ai/user/Anlittledy) <br>
- [FireRed-OpenStoryline repository](https://github.com/FireRedTeam/FireRed-OpenStoryline.git) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local prerequisite checks, install commands, configuration updates, and service startup instructions.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
