## Description:

Executes Karpathy-style knowledge queries by searching M-Flow memory, formatting results as wiki entries, and saving them for later compilation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sora-mury](https://clawhub.ai/user/sora-mury)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn M-Flow memory search results into reusable Markdown wiki entries for later knowledge compilation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists memory-derived content into a wiki that may be reused downstream.

Mitigation: Review saved wiki entries before using them for later compilation or publication.

Risk: Write behavior is under-scoped and may save output outside the intended wiki area if configured carelessly.

Mitigation: Run the skill with workspace write permissions limited to the intended wiki directory.

Risk: Confidential memory content could be copied into persistent Markdown files.

Mitigation: Avoid use with confidential memory until filename containment and Markdown/content sanitization are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sora-mury/skills/karpathy-query-feedback)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown wiki table entries, JSON result objects, and plain-text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes retrieved memory content to a persistent wiki file when query results are found.]

## Skill Version(s):

1.0.0 (source: server release evidence; target metadata matches)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
