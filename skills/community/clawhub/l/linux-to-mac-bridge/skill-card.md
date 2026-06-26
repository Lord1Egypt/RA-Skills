## Description: <br>
Installs Linux-side wrappers that expose selected Mac-owned and Homebrew-backed tools over SSH for trusted same-LAN gateway setups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure auditable Linux gateway commands that call selected tools on trusted local Mac nodes over SSH. It is intended for wrapper-backed public skills and same-LAN Mac tool ownership mapping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated wrappers run selected trusted Mac tools over SSH and can affect real Mac-side apps, Homebrew packages, GitHub state, messages, notes, reminders, or screenshots depending on the wrapped tool. <br>
Mitigation: Install only for Macs and SSH accounts the user trusts, review the generated tool-to-host map, and use least-privilege SSH credentials. <br>
Risk: Using the bridge with untrusted WAN hosts or arbitrary remote shells expands the exposure beyond the skill's stated local-network design. <br>
Mitigation: Keep deployments to a trusted local network or VLAN, assign one explicit owning Mac per tool, and avoid generic remote shell bridging. <br>
Risk: Sleeping or unreachable Mac nodes can make wrapper-backed workflows unreliable. <br>
Mitigation: Keep Mac nodes awake during agent work or configure Wake-on-LAN metadata and verify wrapper readiness after installation. <br>


## Reference(s): <br>
- [Skill Readiness](artifact/references/skill-readiness.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/matthewxmurphy/linux-to-mac-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated shell wrapper files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create executable wrapper files under the configured Linux target directory.] <br>

## Skill Version(s): <br>
1.2.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
