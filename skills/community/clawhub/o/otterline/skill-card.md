## Description: <br>
Otterline provides free sample NBA and NHL moneyline pick predictions from Otterline's AI consensus model, with confidence tiers and no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChrisLyonsHFX](https://clawhub.ai/user/ChrisLyonsHFX) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External sports fans and agent users use this skill to fetch and present current free sample NBA and NHL betting-pick predictions, grouped by confidence tier. It is intended for entertainment-oriented pick discovery with responsible-betting disclaimers, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Otterline/Supabase endpoints to fetch free sports-betting pick samples. <br>
Mitigation: Install only if external requests to those disclosed services are acceptable for the user's environment. <br>
Risk: Sports-betting picks may be mistaken for financial advice or guaranteed outcomes. <br>
Mitigation: Present picks as entertainment only, include the responsible-betting disclaimer, and avoid language that guarantees results. <br>
Risk: Betting-related prompts can expose personal preferences or sensitive information. <br>
Mitigation: Do not share personal, financial, or sensitive information when asking for betting-related guidance. <br>
Risk: Free sample responses include a premium upsell. <br>
Mitigation: Keep the upsell transparent and attribute it to Otterline rather than presenting it as neutral advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChrisLyonsHFX/otterline) <br>
- [Otterline website](https://otterline.club) <br>
- [Otterline premium picks](https://otterline.club/premium) <br>
- [Free NBA picks endpoint](https://gvwawacjgghesljfzbph.supabase.co/functions/v1/free-nba-picks) <br>
- [Free NHL picks endpoint](https://gvwawacjgghesljfzbph.supabase.co/functions/v1/free-nhl-picks) <br>
- [Otterline on X](https://twitter.com/TheOtterline) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown or plain text summaries of fetched JSON pick data, including tiered picks, sample notices, upgrade links, credit, and responsible-betting disclaimers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches fresh NBA and NHL sample-pick data from disclosed public endpoints; optional date parameters use YYYY-MM-DD.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and artifact/claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
