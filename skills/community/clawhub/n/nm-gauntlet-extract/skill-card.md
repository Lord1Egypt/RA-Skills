## Description:

Builds the gauntlet knowledge base from AST extraction and AI enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to initialize or refresh codebase knowledge for challenges. It guides AST extraction, natural-language enrichment, cross-referencing, and saving the result as a knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because three referenced local paths could not be resolved.

Mitigation: Check the unresolved references and review their contents before installing or running the skill.

## Reference(s):

- [Gauntlet project page](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [JSON knowledge base with natural-language details and cross-references; Markdown usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The knowledge base is saved as .gauntlet/knowledge.json and may include entries merged from annotations.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata; artifact frontmatter lists 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
