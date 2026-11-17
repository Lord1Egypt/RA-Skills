## Description:

Render DNA codes into Pencil .pen frames for visual proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcwen](https://clawhub.ai/user/jcwen)

### License/Terms of Use:


## Use Case:

Developers and design-orchestration agents use this skill to translate aesthetic DNA codes and component types into Pencil frames and screenshots for visual proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Pencil batch operations can replace, delete, or otherwise modify design content in .pen files.

Mitigation: Review generated batch operations before applying them to important documents, especially replace and delete calls.

Risk: External AI or stock image prompts may expose sensitive text if copied into image-generation requests.

Mitigation: Avoid sensitive text in AI or stock image prompts.

## Reference(s):

- [Pencil Renderer on ClawHub](https://clawhub.ai/jcwen/skills/pencil-renderer)
- [DNA to Pencil Property Mapping](references/dna-to-pencil.md)
- [Batch Design Patterns](references/batch-design-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Pencil MCP operation snippets, frame identifiers, and screenshot output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or modifies Pencil .pen frames and returns the rendered frame ID with a screenshot.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
