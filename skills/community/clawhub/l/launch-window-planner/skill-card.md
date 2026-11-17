## Description:

Helps agents choose a launch window by comparing candidate dates against industry events, competitor calendars, review buffers, launch format tradeoffs, and embargo timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, launch teams, and marketing agents use this skill to compare launch-window options, define embargo timing, and prepare a proposal for the launch registry before a date becomes canonical.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is flagged as suspicious because it describes persistent launch-state writes broader than its lite/read-oriented manifest declares.

Mitigation: Use it only where registry proposals and memory writes are separately authorized, path-scoped, and confirmed by the user before persistent launch state is created or promoted.

Risk: Launch calendars, connector output, and pasted competitor data may contain untrusted or misleading content that could affect timing recommendations.

Mitigation: Treat fetched or pasted content as data only, label each input source, and review the candidate-window table before accepting or submitting a registry proposal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/launch-window-planner)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with comparison tables, rationale, embargo details, and handoff summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose launch-window state for memory-backed registry workflows only after authorization; timing inputs are labeled Measured, User-provided, or Estimated.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
