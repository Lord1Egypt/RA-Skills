## Description:

Automated step-by-step mathematical proof generation and review for user-submitted theorems with iterative refinement until acceptance or retry limit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyu20011021-hub](https://clawhub.ai/user/xiaoyu20011021-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Students, educators, and developers use this skill to generate and critique step-by-step proofs for mathematical statements while preserving requested methods, tools, language, and output constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-selected reference files or folders may expose sensitive local content when included as proof context.

Mitigation: Use only narrow, non-sensitive reference materials and avoid broad directories, credentials, private notes, or project folders with secrets.

Risk: The iterative proof and review loop can add latency or cost, especially with high retry limits.

Mitigation: Set clear retry expectations and stop or lower the retry limit when the proof no longer improves.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoyu20011021-hub/skills/math-proof)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown proof text with LaTeX-compatible mathematical notation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include iterative review feedback, round status, and a final accepted proof or retry-limit failure summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
