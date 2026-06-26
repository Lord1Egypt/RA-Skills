## Description: <br>
Install Go compiler on Linux for Go project compilation and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solidexu](https://clawhub.ai/user/solidexu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install a Linux Go toolchain, configure PATH, GOPATH, and GOROOT, and run common development commands for testing, building, and dependency management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer guidance adds persistent shell configuration to ~/.bashrc or ~/.profile, which can conflict with an existing Go installation. <br>
Mitigation: Review the PATH, GOPATH, and GOROOT additions before appending them, and adjust or remove older Go configuration first. <br>
Risk: The example commands download a specific Go archive and assume the selected CPU architecture and version are appropriate. <br>
Mitigation: Confirm the system architecture, download from the official Go site, prefer the current patched Go release, and verify the published checksum when possible. <br>


## Reference(s): <br>
- [Go Downloads](https://go.dev/dl/) <br>
- [ClawHub Skill Page](https://clawhub.ai/solidexu/go-install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Linux-focused installation guidance for amd64 and arm64 systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
