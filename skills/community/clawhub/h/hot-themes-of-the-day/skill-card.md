## Description:

Provides daily A-share market hot theme summaries, related stocks, latest prices, percentage changes, and linkage reasons from the 牛股王 data feed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maomaoxx779-cmd](https://clawhub.ai/user/maomaoxx779-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users following A-share market activity use this skill to ask what themes are active today and to review related stocks and stated linkage reasons. Outputs should be treated as informational market summaries, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment-related output may be time-sensitive or lower-confidence than regulated market data.

Mitigation: Treat outputs as informational only and verify against trusted market data before making financial decisions.

Risk: The skill relies on an unsecured HTTP data feed for market-related output.

Mitigation: Review before installation, prefer an HTTPS source when available, and avoid sending sensitive data through the feed.

Risk: The artifact requires fixed promotional footer text in every response.

Mitigation: Review before installing when neutral formatting, localization flexibility, or non-promotional output is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maomaoxx779-cmd/skills/hot-themes-of-the-day)
- [Publisher profile](https://clawhub.ai/user/maomaoxx779-cmd)
- [Niuguwang HotSpot GetNews API](http://apicore.niuguwang.com/askstock/HotSpot/GetNews)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are intended as informational market summaries and include source and AI-disclaimer footer text described by the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
