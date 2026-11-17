## Description:

Search TikTok. Use when the user says things like "find TikTok videos about home workouts", "what is trending on TikTok for this keyword" or "show the top videos and their view counts". Runs through looot, billed per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search TikTok videos by keyword and return captions, authors, engagement counts, and links. It is intended for users who want a sorted snapshot of video results for a stated search date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A search run is billed per call and provider prices can differ.

Mitigation: Inspect and tell the user the endpoint price before running, and run only after the user approves the charge.

## Reference(s):

- [TikTok Search skill page](https://clawhub.ai/walidboulanouar/skills/looot-tiktok-search)
- [looot skill setup instructions](https://looot.ai/skill.md)
- [TikTok Search information](https://looot.ai/agent-skills/tiktok-search)

## Skill Output:

**Output Type(s):** [Text, Structured data]

**Output Format:** [Markdown list of video captions, authors, views, likes, and links, with the keyword and search date]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are sorted by views; provider, sort, region, and paging options can affect the returned results.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
