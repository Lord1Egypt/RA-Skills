## Description: <br>
NanoClaw runtime traffic monitoring baseline for host-side proxy inspection with container-safe MCP and IPC status surfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers and security engineers use this skill as a NanoClaw specification baseline for opt-in host-side traffic monitoring, redacted findings, and container-safe MCP or IPC status surfaces. This release documents the intended architecture and safety contract rather than shipping an active monitor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Future implementations could expose raw traffic, secrets, or CA private key material through logs, containers, or MCP responses. <br>
Mitigation: Keep CA private keys on the host, redact snippets before persistence or MCP responses, and return only bounded findings and status. <br>
Risk: HTTPS inspection and proxying can affect operator trust boundaries if enabled implicitly. <br>
Mitigation: Make monitoring opt-in, require deliberate per-runtime trust configuration, and avoid automatic system CA installation. <br>
Risk: This version is a specification scaffold and may be mistaken for an active traffic monitor. <br>
Mitigation: Verify release artifacts before installation and treat the package as implementation guidance until active monitor code is added and tested. <br>


## Reference(s): <br>
- [NanoClaw Traffic Guardian README](artifact/README.md) <br>
- [NanoClaw Traffic Guardian Specification](artifact/SPEC.md) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/nanoclaw-traffic-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON schema examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Specification scaffold; no active runtime monitoring code is shipped in this version.] <br>

## Skill Version(s): <br>
0.0.1-beta2 (source: frontmatter, skill.json, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
