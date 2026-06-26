## Description: <br>
Expose Mac Homebrew tools like brew, gh, and other /opt/homebrew/bin CLIs on a Linux OpenClaw gateway by installing explicit same-LAN SSH wrappers with optional Wake-on-LAN and OpenClaw config auto-discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to expose selected Mac Homebrew CLIs on a Linux OpenClaw gateway through explicit SSH-backed wrappers. It is intended for trusted same-LAN or VLAN setups where the Mac owns the real Homebrew binaries and the Linux gateway owns stable wrapper paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [Skill Readiness](references/skill-readiness.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces wrapper installation and verification guidance for explicitly selected Homebrew tools; users should choose trusted SSH hosts, keys, and tool mappings.] <br>

## Skill Version(s): <br>
0.6.1 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
