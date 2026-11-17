## Description:

Maintains dated per-platform social-platform norm cards covering character limits, visible-fold cutoffs, hashtag norms, format specs, link placement, disclosure mechanics, algorithm notes, and stale-card flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and social-content teams use this skill to build or refresh platform norm cards before drafting, scheduling, or auditing organic social content. It helps agents distinguish official platform documentation from named folklore, date every norm, and flag cards that are past review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed platform-card changes could preserve outdated or misleading norms if accepted without review.

Mitigation: Review card edits, source labels, last-verified dates, and review-by dates before using the norms in downstream social content.

Risk: The skill can propose shared file or memory updates that may affect future agent sessions.

Mitigation: Confirm memory saves and pointer updates only when the reviewed results should be reused later.

## Reference(s):

- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/platform-norm-profiler)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown card updates, staleness reports, rule-snapshot pointer candidates, and concise handoff summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include proposed file or memory updates that should be reviewed before reuse.]

## Skill Version(s):

19.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
