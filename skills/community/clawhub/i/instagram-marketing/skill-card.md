## Description:

Generates Instagram marketing content from product URLs, including image suggestions, captions, hashtags, and format-specific posting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[insight68](https://clawhub.ai/user/insight68)

### License/Terms of Use:


## Use Case:

External marketers, creators, and commerce teams use this skill to turn public product URLs into ready-to-adapt Instagram feed, carousel, story, reel, caption, hashtag, and posting-strategy content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can make outbound web requests to user-supplied URLs without URL validation or redirect/IP-range protections.

Mitigation: Use ordinary public product URLs only, avoid internal or private URLs, and run the skill in a network-restricted sandbox until validation and redirect/IP-range protections are added.

## Reference(s):

- [Instagram Hashtag Strategy](references/HASHTAG_STRATEGY.md)
- [Instagram Content Package Output Template](templates/OUTPUT_TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown content package with optional JSON product extraction output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product overview, image or video brief, caption, hashtag strategy, posting strategy, engagement preparation, success metrics, and repurposing ideas.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
