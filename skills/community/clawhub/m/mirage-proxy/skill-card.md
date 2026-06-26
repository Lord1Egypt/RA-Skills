## Description: <br>
Install and configure mirage-proxy as a transparent PII/secrets filter for OpenClaw LLM API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chandika](https://clawhub.ai/user/chandika) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install mirage-proxy, route OpenClaw model providers through a local privacy proxy, and configure direct-provider fallback routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and starts a persistent local proxy that can intercept provider-authenticated model traffic. <br>
Mitigation: Install only when the mirage-proxy project is trusted, keep direct-provider fallbacks configured, and remove the proxy plus related provider configuration when it is no longer needed. <br>
Risk: The setup script can fall back to an unpinned source build if the downloaded binary does not run. <br>
Mitigation: Prefer verified release binaries and avoid the source-build fallback unless the repository and build path have been reviewed. <br>
Risk: The proxy log may reveal sensitive redaction metadata. <br>
Mitigation: Monitor, protect, rotate, or delete the log according to local data-handling requirements. <br>


## Reference(s): <br>
- [Mirage Proxy ClawHub release](https://clawhub.ai/chandika/mirage-proxy) <br>
- [mirage-proxy project link from artifact](https://github.com/chandika/mirage-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and JSON5 configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install, uninstall, provider configuration, persistence, verification, and fallback guidance.] <br>

## Skill Version(s): <br>
0.5.17 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
