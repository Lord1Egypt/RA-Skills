## Description: <br>
Install Chinese/CJK fonts on Linux hosts using distro packages and fontconfig verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[totongf](https://clawhub.ai/user/totongf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and verify Chinese/CJK fonts on Linux hosts, containers, desktops, headless browser environments, screenshot pipelines, PDF renderers, and document export workflows where Chinese text may otherwise render as missing glyphs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled workflow can install system packages and refresh font caches, which may require administrator privileges and change the host environment. <br>
Mitigation: Run the dry-run or verify-only mode first, and use administrator privileges only when system-level font installation is intended. <br>
Risk: Unsupported Linux package managers are not handled by the script. <br>
Mitigation: Use the documented manual font installation fallback when dnf, yum, or apt-get is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/totongf/install-chinese-fonts) <br>
- [Publisher profile](https://clawhub.ai/user/totongf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and bundled shell script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose package-manager commands that install system fonts and refresh fontconfig caches.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
