## Description:

Nuwa (女娲) researches a named person, extracts thinking frameworks, mental models, decision heuristics, and expression DNA, and generates a runnable perspective skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alchaincyf](https://clawhub.ai/user/alchaincyf)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use Nuwa to create or update public-figure perspective skills that answer from documented cognitive frameworks rather than repeating quotes. It is useful for thinking advisors, decision reference, and persona-style analysis when generated outputs are reviewed before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated persona skills may speak in first person as public figures with limited disclosure, which can confuse users about attribution or endorsement.

Mitigation: Review generated SKILL.md files before enabling them, especially disclosure text, trigger phrases, and role-play rules.

Risk: The skill creates or updates local skill directories and stores research notes.

Mitigation: Run it only in a workspace where file creation is expected, and review generated files before installation or use.

Risk: The install command in the evidence is not pinned.

Mitigation: Pin or verify the installer source and release version before installation.

## Reference(s):

- [Nuwa README](artifact/README.md)
- [Nuwa Skill Definition](artifact/SKILL.md)
- [Extraction Framework](artifact/references/extraction-framework.md)
- [Skill Template](artifact/references/skill-template.md)
- [Naval Perspective Example](artifact/examples/naval-perspective/SKILL.md)
- [Elon Musk Perspective Example](artifact/examples/elon-musk-perspective/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/alchaincyf/skills/nuwa-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown skill files, research notes, concise text guidance, and occasional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated perspective skills should include source notes, honesty boundaries, and validation results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
