## Description:

Compress natural language prompts into I-Lang — AI-native structured instructions. Output is text notation only — review before passing to execution agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsorgcn](https://clawhub.ai/user/adsorgcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to compress natural language prompts into compact I-Lang instruction notation while preserving intended operations for later review or agent handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command-like I-Lang notation may be acted on if passed to an agent or tool that interprets terms such as DEL, WRIT, SYNC, @LOCAL, @DRIVE, or @R2.

Mitigation: Review compressed output before passing it to execution-capable agents, tools, or automation systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adsorgcn/skills/ilang-compress)
- [I-Lang Homepage](https://ilang.ai)
- [I-Lang Specification](https://ilang.ai/spec/)
- [I-Lang Dictionary](https://github.com/ilang-ai/ilang-dict)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [I-Lang text notation followed by a brief Markdown explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only output; command-like notation should be reviewed before use by execution-capable agents or automation.]

## Skill Version(s):

2.3.4 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
