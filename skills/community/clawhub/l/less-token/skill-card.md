## Description:

Compress verbose summary prompts into structured one-line instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsorgcn](https://clawhub.ai/user/adsorgcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI users use this skill to turn verbose summarization requests into compact I-Lang prompt syntax while preserving the requested summary task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided prompt content to the host AI model for compression and may be used with confidential source text.

Mitigation: Avoid providing confidential content unless the host AI environment is approved for that data.

Risk: Evidence notes a small wording mismatch where one instruction may encourage summarization in addition to compression.

Mitigation: Use the skill as a prompt-compression aid and review the compressed output to ensure it preserves the intended task.

## Reference(s):

- [Less Token on ClawHub](https://clawhub.ai/adsorgcn/skills/less-token)
- [I-Lang homepage](https://ilang.ai)
- [I-Lang benchmark](https://ilang.ai/benchmark/)
- [I-Lang dictionary](https://github.com/ilang-ai/ilang-dict)
- [I-Lang research](https://research.ilang.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown containing compressed I-Lang prompt strings plus a brief explanation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only behavior; no CLI, API key, external dependency, file access, command execution, URL fetching, or external service call is described in the evidence.]

## Skill Version(s):

1.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
