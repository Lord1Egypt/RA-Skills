## Description:

Generate 3D animation scripts and lay explanations for drug mechanisms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, medical educators, and scientific-content creators use this skill to draft mechanism-of-action animation storyboards, voiceover scripts, key visual concepts, and plain-language explanations for drug mechanisms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite arbitrary writable files when an output path is supplied.

Mitigation: Run it only in a sandbox or disposable workspace and avoid passing important existing file paths to --output.

Risk: Drug mechanism explanations may be incomplete or clinically misleading if used as-is for healthcare audiences.

Mitigation: Treat outputs as draft educational copy and require qualified clinical or pharmacology review before sharing with patients, investors, or healthcare audiences.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [MoA Explainer on ClawHub](https://clawhub.ai/aipoch-ai/skills/moa-explainer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown with structured sections; generated text may also be saved to a file when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires drug name, mechanism of action, and molecular target for script generation; lay explanations use drug name and mechanism.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
