## Description:

No Prompt turns a user's plain-language task description into a structured I-Lang instruction that can be copied into other AI systems as a starting prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsorgcn](https://clawhub.ai/user/adsorgcn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert natural-language task requests into concise I-Lang prompt instructions for reuse with other AI systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated I-Lang instructions may be interpreted differently across AI systems or models.

Mitigation: Review generated instructions before reuse and test important prompts with the target model.

Risk: A generated instruction for sensitive, financial, legal, or automated work could omit context or produce unsafe downstream behavior.

Mitigation: Treat generated instructions as drafts and apply domain review before using them for sensitive or automated actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adsorgcn/skills/no-prompt)
- [I-Lang homepage](https://ilang.ai)
- [I-Lang dictionary](https://github.com/ilang-ai/ilang-dict)
- [I-Lang research](https://research.ilang.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with a structured I-Lang instruction followed by a brief explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, file access, credentials, installation, persistence, or external service calls are requested by the skill.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
