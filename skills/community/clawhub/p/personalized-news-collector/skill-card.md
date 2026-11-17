## Description:

Get current news which matches user's recent interests. It can be triggered when user ask about current news or the events happening around without selecting a specific topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeron90](https://clawhub.ai/user/zeron90)

### License/Terms of Use:


## Use Case:

External users use this skill to have an agent infer recent interests from the conversation or memory, collect current news about those interests, and return a categorized report ranked by apparent popularity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can infer news interests from prior conversation or memory without clear consent.

Mitigation: Ask before using conversation history or memory, then confirm the inferred interests before collecting news.

Risk: The skill can fetch arbitrary web pages without clear source, redirect, or size limits.

Mitigation: Prefer the reviewed source list and restrict outbound fetching to trusted HTTPS news domains with redirect and response-size limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zeron90/skills/personalized-news-collector)
- [News source list](artifact/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown news report with categorized ranked items and optional inline shell commands for collection.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [At least three interests and at least three news items per interest are requested by the artifact.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
