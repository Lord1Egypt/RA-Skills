## Description:

Use when researching a person, publication, brand, blog, creator, work, or other style-bearing target to create a reusable style guide or test whether generated work reflects that target.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahongc](https://clawhub.ai/user/jiahongc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writers use this skill to research style-bearing targets, build reusable runtime style skills, and evaluate generated work against held-out evidence while preserving authorization, attribution, and originality boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be misused to imitate living people too closely or imply endorsement.

Mitigation: For living people without authorization, keep outputs to high-level inspired-by guidance and do not claim authorship, endorsement, impersonation, or reader deception.

Risk: Research may rely on inaccessible, weak, or insufficient public sources.

Mitigation: Record access gaps, source sufficiency, corpus roles, and saturation evidence before generating a runtime skill.

Risk: Generated outputs may copy distinctive phrasing, stories, or source sequences.

Mitigation: Keep excerpts short, generate original material, and run phrase-overlap and held-out evidence checks during evaluation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiahongc/skills/imitation-author)
- [Project homepage](https://github.com/jiahongc/imitation-machine)
- [Research protocol](references/research-protocol.md)
- [Evaluation protocol](references/evaluation-protocol.md)
- [Pressure scenarios](tests/pressure-scenarios.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown files and structured markdown templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one portable runtime skill plus research, output, and evaluation materials for a target style model.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
