## Description:

Hotspot Writer helps agents fetch public trending topics from major Chinese social platforms, draft platform-specific social content, and archive trends and generated drafts locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujw0214](https://clawhub.ai/user/liujw0214)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to monitor public trending topics, select trends aligned with their content focus, and draft social posts, short-video scripts, public-account articles, and microblog updates for human review before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact public trend platforms to fetch current topics.

Mitigation: Specify the platforms, topics, and monitoring scope needed for the task, especially for one-off writing requests.

Risk: Trend snapshots and generated drafts may be saved into a local hotspot archive.

Mitigation: Set the desired archive location and retention expectations, or ask the agent to skip archiving when persistence is not needed.

Risk: Generated trend-based copy can be inaccurate, stale, or unsuitable for publication without review.

Mitigation: Review fetched trends and all generated drafts before publishing, consistent with the skill workflow's approval step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujw0214/skills/hotspot-writer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with example shell-style prompts and YAML configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save fetched trends and generated drafts to a local hotspot archive when archiving is enabled.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
