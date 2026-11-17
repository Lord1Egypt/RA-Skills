## Description:

Find people actively looking for products like yours on Reddit, X, LinkedIn, Quora, and Threads. Free mode uses web_search; paid mode uses the HotMention API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexandr-belogubov](https://clawhub.ai/user/alexandr-belogubov)

### License/Terms of Use:


## Use Case:

External users and go-to-market teams use this skill to find social posts that show buying intent for a product, score relevance, identify competitors, and draft replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product keywords and lead-search terms may be sent to web search or to HotMention when the optional API key is configured.

Mitigation: Use paid API mode only when sharing those terms with HotMention is acceptable, and treat automated monitoring such as cron as a separate setup choice.

## Reference(s):

- [HotMention](https://hotmention.com)
- [HotMention API Documentation](https://hotmention.com/docs/api)
- [ClawHub Skill Page](https://clawhub.ai/alexandr-belogubov/skills/hotmention)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown with scored mention summaries, verdicts, competitor notes, draft replies, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use normal web search in free mode or the optional HotMention API when HOTMENTION_API_KEY is configured.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
