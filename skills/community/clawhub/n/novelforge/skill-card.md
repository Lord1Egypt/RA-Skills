## Description:

NovelForge helps agents run a structured novel-writing workflow with story inception, outlines, chapter blueprints, context compilation, drafting, review, settlement, Markdown wiki memory, and custom narrative-engine distillation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

MIT

## Use Case:

Authors and agent users use NovelForge to plan, draft, review, and settle short fiction, novellas, and serialized novels through a recoverable file-based workflow. Developers can also use it to package or distill custom narrative engines for project-specific writing methods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file tools are under-scoped and can modify, read, or delete outside the intended project boundary.

Mitigation: Install only in a dedicated, trusted novel workspace and avoid untrusted projects or engine folders until project-root path confinement, symlink rejection, and hash-checked chapter patch restrictions are enforced.

Risk: Persistent .novelforge project state and Chinese-first interaction may surprise users expecting stateless or English-only behavior.

Mitigation: Review project state before reuse and confirm language expectations for the target writing project.

## Reference(s):

- [NovelForge README](README.md)
- [Executable workflow and gates](novelforge.md)
- [Story genesis and capacity assessment](references/story-genesis.md)
- [Engine contract and activation rules](references/engine-contract.md)
- [Narrative engine distillation](references/engine-distillation.md)
- [Project profile specification](references/project-profile-spec.md)
- [Story memory and Context Ticket](references/story-memory.md)
- [Chapter state machine](references/state-machine.md)
- [Quality checklist](references/quality-checklist.md)
- [Settlement specification](references/settlement-spec.md)
- [ClawHub skill page](https://clawhub.ai/fize/skills/novelforge)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Simplified Chinese Markdown with JSON, JSONL, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-based novel project artifacts, review reports, state records, and narrative-engine guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md openclaw metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
