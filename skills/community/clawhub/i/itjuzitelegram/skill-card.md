## Description:

Queries ITjuzi venture-capital bulletin events for today's updates, recent financing activity, keyword-filtered event streams, and sector news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyentq-alt](https://clawhub.ai/user/skyentq-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve and summarize ITjuzi venture-capital bulletin updates, including today's investment news and member-only filters when a valid ITjuzi Skill Token is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store an ITjuzi Skill Token under the user's home directory and show a token prefix.

Mitigation: Prefer the ITJUZI_SKILL_TOKEN environment variable, avoid --show-token in logged sessions, and remove the saved token when it is no longer needed.

Risk: The script contacts the external ITjuzi API with query parameters such as date scope, keyword, event type, page, and limit.

Mitigation: Use the skill only in environments where calls to ITjuzi are allowed and avoid sending sensitive keywords.

Risk: Free-user responses may include subscription messaging required by the artifact behavior.

Mitigation: Review generated responses for appropriateness before using them in user-facing or regulated workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skyentq-alt/skills/itjuzitelegram)
- [ITjuzi Telegraph API](https://www.itjuzi.com/api/telegraph/get_list)
- [ITjuzi Membership Page](https://www.itjuzi.com/order)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain-text summaries with inline shell commands and JSON-derived results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include subscription guidance for free users and token-management instructions for members.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog list 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
