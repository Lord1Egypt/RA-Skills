## Description:

Litho Doc helps agents analyze a software repository and generate C4-style architecture documentation, workflow documentation, module deep dives, boundary interface notes, and conditional database documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sopaco](https://clawhub.ai/user/sopaco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent inspect a codebase and produce readable project documentation, including architecture views, workflow explanations, module deep dives, interface summaries, and database notes when applicable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository contents to produce documentation, which may expose sensitive code or project details to the agent session.

Mitigation: Review the target repository for sensitive material before use and run the skill only in an environment approved for that codebase.

Risk: The skill may create documentation artifacts and temporary .litho-agent research files in the target workspace.

Mitigation: Specify the intended output directory and decide whether temporary research files should be retained for review or deleted after generation.

Risk: Generated architecture explanations and diagrams can be incomplete or misleading if the repository structure is ambiguous or very large.

Mitigation: Review generated documentation against the source code before publishing or using it for engineering decisions.

## Reference(s):

- [Litho Doc ClawHub Release](https://clawhub.ai/sopaco/skills/litho-documents-skill)
- [Phase 1 Preprocessing Guide](references/phase1-preprocessing.md)
- [Phase 2 Research Guide](references/phase2-research.md)
- [Phase 3 Composition Guide](references/phase3-composition.md)
- [Phase 4 Output Guide](references/phase4-output.md)
- [Mermaid Diagram Templates](references/doc-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown documentation files with Mermaid diagrams and a concise execution summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary .litho-agent research files during analysis and can delete or retain them based on user preference.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
