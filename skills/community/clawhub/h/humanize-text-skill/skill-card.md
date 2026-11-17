## Description:

Audits and rewrites Chinese or English content to remove AI tone, preserve protected facts, and pull the result toward a target human voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fendouai](https://clawhub.ai/user/fendouai)

### License/Terms of Use:

MIT

## Use Case:

Writers, editors, and developers use this skill in agent runtimes to detect AI-shaped prose, rewrite drafts, or make focused in-file edits for docs, status updates, public writing, and issue replies while preserving protected spans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Development logs or local state files may be present in an unfiltered repository checkout.

Mitigation: Install from the filtered ClawHub package, or verify that .omx development logs and local state files are excluded before deployment.

Risk: Legal, compliance, technical, quoted, or externally sourced text can lose important meaning if rewritten too aggressively.

Mitigation: Use detect mode first for higher-risk material, preserve protected spans, and review suggested changes before use.

Risk: Voice samples may contain writing style that the user is not authorized to adapt.

Mitigation: Use only voice samples the user is authorized to provide, and apply them as observable style guidance rather than as factual or identity content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fendouai/skills/humanize-text-skill)
- [Project homepage](https://github.com/fendouai/humanize-text-skill)
- [Lynote.ai](https://lynote.ai)
- [Skill architecture](references/skill-architecture.md)
- [Protected spans](references/protected-spans.md)
- [Voice contract](references/voice-contract.md)
- [Detector engine](detector/README.md)
- [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)
- [shuorenhua](https://github.com/MrGeDiao/shuorenhua)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Plain text or Markdown containing diagnostics, rewritten prose, edit guidance, or code-preserving changes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports detect-only, rewrite, and edit-in-place modes; protects spans such as numbers, commands, paths, versions, names, logs, and quotes.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter, package.json, and changelog report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
