## Description:

Generates reviewable contract drafts from Word templates and structured business facts, including party details, cooperation content, missing-field lists, and validation artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renjicode](https://clawhub.ai/user/renjicode)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn an existing Word contract template and structured business terms into a reviewable draft, missing-items note, run summary, and validation report. It supports business and legal review workflows and should not be treated as final legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare environment or login changes and install helper tooling as part of Word plugin setup.

Mitigation: Install and run it only in an isolated or trusted workspace, and approve package installation or login steps before execution.

Risk: Contract templates, generated drafts, and auxiliary reports may contain sensitive business or legal information.

Mitigation: Review generated .docx, JSON, and Markdown outputs before sharing, and avoid using sensitive data in untrusted workspaces.

Risk: Template paths and output filenames influence file reads and writes performed by the runner.

Mitigation: Use trusted template paths and explicit output locations, and avoid attacker-controlled paths or filenames.

Risk: Generated contract text can be incomplete, inconsistent, or unsuitable for signature without professional review.

Mitigation: Treat outputs as review drafts, keep unresolved fields visible, and require business and legal review before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renjicode/skills/keplerjai-contract-draft)
- [Publisher profile](https://clawhub.ai/user/renjicode)
- [README](README.md)
- [Generic requirements](references/generic-requirements.md)
- [Input contracting rules](references/input-contracting-rules.md)
- [Runtime output contract](references/runtime-output-contract.md)
- [Template analysis](references/template-analysis.md)
- [Word plugin setup](references/word-plugin-setup.md)
- [Iteration notes](references/iteration-notes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON job specs, shell commands, Word .docx drafts, and JSON/Markdown validation artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces editable contract drafts plus missing-items, run-summary, and validation-report files for review.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
