## Description: <br>
Audits and hardens an OpenClaw installation for common security misconfigurations, including exposed gateway listeners, missing authentication, elevated execution, permissive tool policies, open DM access, plaintext API keys, and insecure file permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billyhetech](https://clawhub.ai/user/billyhetech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review a local OpenClaw setup before first use, after reconfiguration, or when investigating whether the installation is safe. It produces a concise report card and prioritized hardening guidance based on local configuration, process state, listener exposure, authentication, tool policy, channel access, and secret handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local configuration, process state, listeners, permissions, and secret-adjacent files, which may expose sensitive operational details during an audit. <br>
Mitigation: Use it only in a trusted maintenance environment, keep inspection local, and avoid printing full API keys, tokens, or secret values. <br>
Risk: Hardening recommendations can affect authentication, network binding, execution privileges, tool policy, file permissions, or startup commands. <br>
Mitigation: Review each proposed change before applying it, require explicit confirmation, and prefer the smallest safe remediation first. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain-text or Markdown report with status labels, native shell commands, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Secret values should not be printed in full, and configuration, permission, user, or startup-command changes require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
