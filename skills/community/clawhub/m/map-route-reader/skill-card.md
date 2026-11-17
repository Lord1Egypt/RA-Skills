## Description:

Reads real Amap or Baidu Maps route results and turns them into route guidance a user can follow for transit, taxi, walking, or route-comparison questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyunting555](https://clawhub.ai/user/wuyunting555)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer point-to-point route questions with concrete map-derived steps, station names, transfer points, walking segments, and side-by-side comparisons when an alternate route is proposed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Route queries and map results may expose sensitive origin, destination, or travel-pattern information, especially when Browser Relay is used.

Mitigation: Use Browser Relay only on a dedicated Amap or Baidu route tab and select exactly that tab so the agent sees only the intended route details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuyunting555/skills/map-route-reader)
- [Amap route query endpoint](https://ditu.amap.com/dir)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown route summaries with structured steps, route comparisons, and uncertainty notes when extraction fails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include origin, destination, travel mode, estimated duration, transfers, station names, exits, walking distances, and comparison criteria.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
