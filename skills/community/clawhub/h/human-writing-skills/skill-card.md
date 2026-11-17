## Description:

Provides multilingual tools and guidance for natural rewriting, genre-aware drafting, and long-form continuity and editorial review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whh110112](https://clawhub.ai/user/whh110112)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and developers use the skill to revise supplied drafts, create or continue genre-aware prose, and review long-form voice, continuity, and rewrite fidelity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious with medium confidence, citing potentially unsafe code execution and fixer behavior it considers risky for a writing and editing skill.

Mitigation: Review the package verifier behavior and inspect proposed text changes before using the fixer.

Risk: Manuscript data could be sent to a hosted provider, depending on the workflow configuration.

Mitigation: Review the provider configuration and data flow before submitting manuscript material.

Risk: The scan was partial and covered 97.4% of components, leaving some evidence incomplete.

Mitigation: Review the remaining components before relying on the scan as a complete assessment.

## Reference(s):

- [Long-Form Consistency Guide](artifact/docs/long-form-consistency.md)
- [Pattern Linter Guide](artifact/docs/pattern-linter.md)
- [Editing Tools and Rewrite Fidelity](artifact/docs/editing-tools.md)
- [Multilingual Quality Evaluation](artifact/docs/evaluation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance, JSON, Files]

**Output Format:** [Revised prose, Markdown prompts and audit reports, and structured JSON reports or ledgers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the supplied draft, context, selected modules, and host model.]

## Skill Version(s):

0.17.2 (source: server release evidence, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
