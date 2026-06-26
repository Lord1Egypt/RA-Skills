## Description: <br>
Scans MCP server configuration files for OWASP MCP Top 10 risks using mcpsec and reports findings by severity without modifying config files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit MCP configuration files for prompt injection, hardcoded secrets, missing authentication, insecure transport, excessive permissions, and related OWASP MCP Top 10 issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automated binary install path can place a downloaded external binary into a system PATH location without enforcing the advertised checksum verification. <br>
Mitigation: Prefer the documented pinned SHA256 verification, Homebrew from a trusted source, or building mcpsec from source before installing or running it. <br>
Risk: The scanner reads local MCP configuration files that may contain API keys or tokens. <br>
Mitigation: Run it only on MCP configs you intend to audit, and use a container, VM, or reviewed source build when handling sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pfrederiksen/mcpsec) <br>
- [mcpsec scanner](https://github.com/pfrederiksen/mcpsec) <br>
- [mcpsec v1.0.0 checksums](https://github.com/pfrederiksen/mcpsec/releases/download/v1.0.0/checksums.txt) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; runtime scan output is text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May exit non-zero when findings meet the configured fail-on threshold.] <br>

## Skill Version(s): <br>
1.0.4 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
