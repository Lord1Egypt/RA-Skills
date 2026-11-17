## Description:

Human Like Memory is an intelligent context-management skill that stores, retrieves, summarizes, and injects relevant memories using vector search and HOT/WARM/COLD memory tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanghailong1221](https://clawhub.ai/user/tanghailong1221)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preserve useful conversation context, search prior memories, compress stored context, and inject only the most relevant memories into future agent responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically remember conversation details in local plaintext memory and inject selected memories into later prompts.

Mitigation: Avoid storing secrets or sensitive personal, medical, financial, address, or business data; review memory files regularly and disable autoRemember or injection defaults when inappropriate.

Risk: Vector search depends on external ML packages and model downloads.

Mitigation: Use pinned dependencies and verified official model sources before enabling vector search in a production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanghailong1221/skills/human-like-memory-cn)
- [@xenova/transformers](https://github.com/xenova/transformers.js)
- [BAAI bge-m3 model card](https://huggingface.co/BAAI/bge-m3)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown and plain text responses with optional JSON memory exports and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inject selected local memories into prompts and may export stored memories as JSON.]

## Skill Version(s):

1.2.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
