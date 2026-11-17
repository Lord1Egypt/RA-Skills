## Description:

Compiles raw wiki entries into structured knowledge points by grouping entries by topic and using LLM distillation to save refined Markdown outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sora-mury](https://clawhub.ai/user/sora-mury)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to turn Phase 1 wiki entries into concise, tagged knowledge points for a Karpathy-style LLM knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill allows broad local file access through wiki and output paths.

Mitigation: Run it in a workspace without sensitive files and keep path or filename parameters under trusted control.

Risk: LLM-generated knowledge points may preserve incorrect or untrusted content from source wiki entries.

Mitigation: Use trusted wiki inputs and review generated knowledge points before relying on them.

Risk: Bundled cross-project tests dynamically load sibling skill directories.

Mitigation: Do not run the bundled cross-project tests unless those sibling skill directories are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sora-mury/skills/karpathy-compile)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Markdown knowledge-point documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated knowledge-point files from trusted wiki inputs; LLM distillation depends on a local Ollama-compatible endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
