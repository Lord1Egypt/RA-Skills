## Description:

多技能联动编排器，将多个独立Skill串联成"超级技能"自动执行.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-long-2022](https://clawhub.ai/user/jack-long-2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to classify a user's goal, select matching skills, and generate multi-step workflows for content creation, research, media analysis, investment analysis, knowledge management, and skill improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflows can include public publishing steps.

Mitigation: Keep auto-publish disabled by default and require a preview plus explicit confirmation before upload or publish actions.

Risk: Generated workflows can include financial portfolio changes.

Mitigation: Require explicit user confirmation before portfolio updates and treat investment outputs as guidance that needs review.

Risk: Generated workflows can write to a knowledge base or other persistent local files.

Mitigation: Show the planned write target and require approval before updating indexes, wiki files, or other persistent state.

Risk: Fetched web content can influence downstream writing, publishing, or skill-improvement steps.

Mitigation: Treat fetched content as untrusted input and review generated outputs before using them in publishing, installation, or skill changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jack-long-2022/skills/openclaw-skill-compounder)
- [SKILL.md](artifact/SKILL.md)
- [CHAIN.md](artifact/CHAIN.md)
- [REGISTRY.md](artifact/REGISTRY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, structured workflow descriptions, YAML pipeline templates, and generated skill-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ordered skill calls, input mappings, output validation expectations, fallback handling, and optional publish or persistence steps.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
