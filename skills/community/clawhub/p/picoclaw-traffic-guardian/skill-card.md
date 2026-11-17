## Description:

Picoclaw runtime traffic monitoring baseline for lightweight AI gateway proxy inspection, egress detection, and posture integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill as a Picoclaw traffic-monitoring scaffold for detecting AI gateway exfiltration and injection signals, writing redacted local findings, and exporting posture for Picoclaw security profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future traffic inspection and optional HTTPS MITM can expose sensitive traffic if implemented or operated too broadly.

Mitigation: Keep monitoring opt-in, scope proxy and CA trust per process, and avoid automatic system-wide proxy or CA changes.

Risk: Traffic findings could persist secrets or sensitive snippets.

Mitigation: Redact snippets before writing local JSONL findings, summaries, or exported posture profiles.

Risk: This release is a beta specification scaffold rather than a working monitor.

Mitigation: Review future implementations carefully before deployment and verify that detect-and-log behavior remains the default.

## Reference(s):

- [ClawSec homepage](https://clawsec.prompt.security)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON schemas, and implementation requirements.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Beta specification scaffold; no active proxy runtime is shipped in the reviewed package.]

## Skill Version(s):

0.0.1-beta2 (source: evidence.json, frontmatter, skill.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
