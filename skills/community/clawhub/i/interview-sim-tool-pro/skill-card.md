## Description:

A recruiting interview simulation skill for managing enterprise question banks, custom interviewer personas, resume-driven questions, scorecard aggregation, and hiring funnel analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and interview program owners use this skill to configure role-specific question banks and interviewer personas, generate resume-specific interview prompts, aggregate scorecards across sessions, and analyze hiring funnel outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resumes, scorecards, and funnel reports may contain sensitive recruiting records.

Mitigation: Use the skill only in an authorized workspace, review files before saving or exporting them, and avoid unnecessary retention of candidate data.

Risk: Command execution may be unsafe if arbitrary shell commands are accepted during diagnostics or local analysis.

Mitigation: Limit shell execution to clearly understood diagnostics or local analysis steps and review command intent before running it.

Risk: Interview scoring and funnel analysis may affect hiring decisions if treated as final judgment.

Mitigation: Use outputs as decision support and keep human review in the recruiting workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/interview-sim-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON examples, text reports, and optional Python snippets or shell diagnostics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured scorecards, funnel summaries, interviewer calibration guidance, and local file or export instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
