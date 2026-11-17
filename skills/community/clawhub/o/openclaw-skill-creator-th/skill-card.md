## Description:

Create new skills, modify and improve existing skills, and measure skill performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nattsukun](https://clawhub.ai/user/nattsukun)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to draft, revise, evaluate, benchmark, and package agent skills through an iterative review workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run authenticated agent processes and bundled review tools with under-scoped security risks.

Mitigation: Use it only in an isolated workspace with non-sensitive skills and evaluation prompts.

Risk: Evaluation and description-optimization scripts may use configured Claude CLI credentials and send skill or eval content to external Claude services.

Mitigation: Avoid real secrets, proprietary code, and untrusted eval sets unless the CLI and environment are sandboxed.

Risk: Review tooling may affect existing local services or packaged skill contents.

Mitigation: Prefer static review output, avoid killing existing services, and inspect packaged skill directories for symlinks before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nattsukun/skills/openclaw-skill-creator-th)
- [schemas.md](artifact/references/schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, JSON schemas, generated reports, and packaged skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create evaluation workspaces, benchmark artifacts, HTML review pages, and packaged skill archives when directed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
