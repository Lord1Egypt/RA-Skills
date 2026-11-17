## Description:

Helps agents scan, compare, chunk, and rewrite Chinese or mixed Chinese-English academic manuscripts for originality, academic style, AI-tone reduction, citation cohesion, terminology consistency, and auditable human review without fabricating sources or targeting detector circumvention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to improve academic drafts, literature reviews, proposals, abstracts, manuscript sections, and patent disclosure drafts through structured diagnosis, rewriting, comparison, and human-review guidance. It is intended for compliant expression improvement while preserving facts, data, citations, and evidence boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can append third-party promotional contact information in relevant responses.

Mitigation: Review or remove the promotional-contact resource before installation if unsolicited commercial contact text is not acceptable.

Risk: Academic manuscripts may contain unpublished, confidential, or otherwise sensitive content.

Mitigation: Run the local scripts only on manuscript files the user is comfortable processing locally, and avoid routing confidential drafts to uncontrolled external services.

Risk: Academic rewriting workflows can be misused for fabrication, ghostwriting, or detector-specific circumvention.

Mitigation: Keep the skill constrained to expression improvement, preserve facts and citations, reject detector-bypass requests, and require human review of final drafts.

## Reference(s):

- [Workflow Reference](references/WORKFLOWS.md)
- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/paper-originality-studio)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown reports, JSON reports, rewritten text, section files, structured prompts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python scripts with user-provided paths; no third-party Python packages are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
