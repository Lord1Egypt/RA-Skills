## Description: <br>
Installs and configures ocmemog, the OpenClaw durable memory plugin and sidecar, using the package path when available and the public repository installer when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simbimbo](https://clawhub.ai/user/simbimbo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install ocmemog, enable the memory-ocmemog plugin, configure the local sidecar endpoint, and validate durable memory behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The source installer path can run changing remote code from the upstream repository. <br>
Mitigation: Prefer the package install path; use the source fallback only when the repository version is pinned or reviewed. <br>
Risk: The skill can alter OpenClaw memory settings. <br>
Mitigation: Review proposed OpenClaw configuration changes before applying them and preserve unrelated plugin configuration. <br>
Risk: The installer can leave a local memory sidecar service running. <br>
Mitigation: Verify the sidecar health endpoint after installation and keep removal or shutdown steps available for the chosen install path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simbimbo/ocmemog-installer) <br>
- [ocmemog GitHub repository](https://github.com/simbimbo/ocmemog.git) <br>
- [ocmemog v0.1.2 GitHub release](https://github.com/simbimbo/ocmemog/releases/tag/v0.1.2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include installation commands, OpenClaw configuration snippets, validation checks, and troubleshooting steps.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
