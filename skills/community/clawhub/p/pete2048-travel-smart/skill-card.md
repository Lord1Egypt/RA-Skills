## Description:

TravelSmart helps drivers compare highway exits, hotels, and taxi pickup points using Amap location data and weighted scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pete2048](https://clawhub.ai/user/pete2048)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to get ranked self-driving travel recommendations for highway exit stops, overnight lodging, and parking-to-taxi pickup points. It can run as a CLI, local web service, or Feishu-integrated assistant when required credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Feishu notification relay can be called without authentication.

Mitigation: Remove the relay unless needed, or protect it with a signed secret or equivalent authorization and require an explicit FEISHU_CHAT_ID.

Risk: The skill sends travel locations, destinations, addresses, and optional natural-language prompts to third-party services.

Mitigation: Run the service only on a trusted local interface, restrict CORS, and notify users before sending location or prompt data to Amap, MiniMax, or Feishu.

Risk: Untrusted map or API fields may be rendered into the web demo.

Mitigation: Escape or sanitize all external fields before inserting them into the page.

## Reference(s):

- [README](README.md)
- [TravelSmart API Reference](references/api-reference.md)
- [TravelSmart PRD](references/PRD.md)
- [Scoring Algorithm](references/scoring-algorithm.md)
- [Amap Web API](https://lbs.amap.com/)
- [Amap Key Console](https://console.amap.com/dev/key/app)
- [MiniMax Platform](https://platform.minimaxi.com)
- [Feishu Open API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown-formatted recommendation text and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns top-ranked travel options with scores, distances, addresses, and recommendation rationale when upstream map data is available.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
