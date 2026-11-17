## Description:

Heartflow Minimal2 is a cognitive-engine skill for agent self-state analysis, memory-backed reasoning, decision routing, emotional and psychological analysis, and self-correction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users can use this skill to route prompts through HeartFlow's cognitive pipeline for reasoning, emotion and psychology analysis, memory search, self-healing checks, and decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can store conversation content in local files, including plaintext storage when memory is enabled without appropriate controls.

Mitigation: Review before use with private data, credentials, source code, or business information; disable memory or configure approved storage, encryption, and retention controls before deployment.

Risk: Broad dispatchable routes can expose memory and write behavior if untrusted callers can invoke HeartFlow dispatch functions.

Mitigation: Restrict dispatch access to trusted callers, constrain allowed routes, and isolate the runtime from sensitive files and credentials.

Risk: Artifact documentation discloses optional code execution, environment access, and filesystem write capabilities.

Mitigation: Keep code execution disabled unless explicitly required, run with least privilege, and require human approval for filesystem or environment-sensitive operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/heartflow-v6)
- [npm package @yun520-1/heartflow](https://www.npmjs.com/package/@yun520-1/heartflow)
- [GitHub repository linked by artifact](https://github.com/yun520-1/mark-heartflow-skill.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Natural-language analysis, Markdown guidance, shell commands, and structured tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may incorporate persisted local memory when memory is enabled.]

## Skill Version(s):

6.0.0 (source: release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
