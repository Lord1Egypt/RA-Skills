## Description:

Claw Mbti generates a playful MBTI-style personality report for an agent by analyzing recent natural-language interactions with the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyang0807](https://clawhub.ai/user/xiaoyang0807)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to ask for an informal personality-style report based on recent interactions. The skill outputs a formatted MBTI-style profile, evidence table, and guidance for zero or insufficient interaction history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes recent conversations and memory to infer personality traits, which can expose private behavioral summaries.

Mitigation: Use only when users are comfortable with this analysis, and review generated reports before sharing them.

Risk: Generated reports may include install or update promotion with a GitHub command.

Mitigation: Do not copy or run install/update commands from reports unless the repository and version have been reviewed and trusted.

Risk: MBTI-style labels can be misleading if treated as factual or clinical assessment.

Mitigation: Present outputs as playful, informal impressions and avoid using them for decisions about people.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoyang0807/skills/lobster-mbti)
- [Project homepage](https://github.com/xiaoyang0807/claw-mbti)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include share prompts, install/update guidance, and a no-result response when interaction history is unavailable.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
