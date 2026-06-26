## Description: <br>
Picoclaw runtime traffic monitoring baseline for lightweight AI gateway proxy inspection, egress detection, and posture integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this scaffold to define opt-in Picoclaw traffic monitoring for gateway HTTP/HTTPS inspection, outbound exfiltration detection, inbound injection detection, redacted local findings, and posture export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Future traffic inspection code could expose sensitive request or response content if it captures too much data or persists raw snippets. <br>
Mitigation: Keep monitoring opt-in, process-scoped, byte-bounded, and redact snippets before logs, summaries, or profile outputs. <br>
Risk: HTTPS inspection could broaden trust or affect unrelated applications if certificate authority handling is automated or global. <br>
Mitigation: Require explicit per-process trust configuration and do not install a system-wide CA or change global proxy settings automatically. <br>
Risk: Users may assume this release provides active runtime protection. <br>
Mitigation: Treat this version as a disclosed scaffold/specification and review any future implementation before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/picoclaw-traffic-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/davida-ps) <br>
- [Project homepage](https://clawsec.prompt.security) <br>
- [Specification](artifact/SPEC.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas and bash verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Specification scaffold only; no active runtime proxy implementation in this release.] <br>

## Skill Version(s): <br>
0.0.1-beta2 (source: server release metadata, SKILL.md frontmatter, CHANGELOG, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
