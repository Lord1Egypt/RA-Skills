## Description: <br>
Developer skill for running Hummingbot and Gateway from source, building wheel and Docker images, and testing against Hummingbot API running from source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengtality](https://clawhub.ai/user/fengtality) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to set up, build, verify, and run a local Hummingbot, Gateway, and Hummingbot API development stack from source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs powerful local install, build, and service scripts that can change developer environments and start Docker-backed services. <br>
Mitigation: Review the bundled shell scripts before execution and run them only on an isolated local development machine. <br>
Risk: Generated local defaults include insecure credentials and passphrases such as admin/admin and a default Gateway passphrase. <br>
Mitigation: Replace default credentials and passphrases before exposing any service, and do not use real trading, exchange, wallet, or production credentials with the defaults. <br>
Risk: The API and Gateway are intended for local development and may be unsafe if exposed beyond localhost. <br>
Mitigation: Avoid port forwarding the API or Gateway and keep the services restricted to local development access. <br>
Risk: The install workflow can overwrite or modify a Hummingbot API .env file. <br>
Mitigation: Back up any existing hummingbot-api .env before running install_all.sh. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local dependency installation, Docker builds, service startup, and smoke testing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
