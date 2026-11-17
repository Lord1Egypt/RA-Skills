## Description:

Novel Master v2 helps agents plan, write, and revise publication-grade Chinese long-form fiction with structured workflows for worldbuilding, character design, outlining, chapter drafting, foreshadowing, and consistency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbroot](https://clawhub.ai/user/bbroot)

### License/Terms of Use:

MIT

## Use Case:

External writers, editors, and developers use this skill to guide Chinese novel projects from concept through outline, chapter drafting, continuity tracking, and quality review. Long-form workflows can use local helper scripts for character state, compressed plot memory, foreshadowing, and auditing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted project or character names can cause helper scripts to read or write outside the intended novel workspace.

Mitigation: Use simple trusted project and character names without slashes or .., and do not let untrusted text choose those identifiers until path validation and workspace containment are added.

Risk: The workflow keeps local novel state under ~/.qclaw.

Mitigation: Install and run it only when that local state location is acceptable for the project, and review generated state before relying on it.

## Reference(s):

- [Skill Instructions](SKILL.md)
- [README](README.md)
- [English README](README_EN.md)
- [Process per Character](references/process-per-character.md)
- [Node Compressed Graph](references/node-compressed-graph.md)
- [Quantum Auditor](references/quantum-auditor.md)
- [Cognitive Bias](references/cognitive-bias.md)
- [Plot Structure](references/plot-structure.md)
- [Character Design](references/character-design.md)
- [Scene Writing](references/scene-writing.md)
- [Foreshadowing](references/foreshadowing.md)
- [Style Guide](references/style-guide.md)
- [Banned Words](references/banned-words.md)
- [Classic Writing Books](references/classic-writing-books.md)
- [Genres](references/genres.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with optional JSON snippets, code blocks, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local novel project state under ~/.qclaw when helper scripts are used.]

## Skill Version(s):

2.0.0 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
