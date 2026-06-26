## Description: <br>
Hermes runtime traffic monitoring baseline for opt-in proxy inspection, egress detection, and attestation-aware traffic posture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill as a specification baseline for building opt-in Hermes traffic monitoring that detects exfiltration and injection signals, writes redacted local findings, and exports monitor posture for attestation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Future proxy or HTTPS inspection behavior could observe sensitive Hermes traffic if configured too broadly. <br>
Mitigation: Keep monitoring scoped to the intended Hermes process and require explicit operator approval for any CA trust changes. <br>
Risk: Threat logs or attestation-linked outputs could expose secrets if findings are not redacted. <br>
Mitigation: Protect local logs and redact snippets before persistence or attestation-linked summaries. <br>
Risk: Standalone downloads could be tampered with before installation. <br>
Mitigation: Verify signed release assets and checksums before trusting standalone artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/hermes-traffic-guardian) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Specification-only baseline; no active proxy runtime is shipped in this version.] <br>

## Skill Version(s): <br>
0.0.1-beta2 (source: server release evidence, frontmatter, skill.json, changelog released 2026-05-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
