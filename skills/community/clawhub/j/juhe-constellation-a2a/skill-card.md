## Description: <br>
Provides paid horoscope profile and fortune lookups for the twelve zodiac signs across daily, weekly, monthly, and yearly periods using 聚合数据. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and consumer agents use this skill to request zodiac profiles and horoscope readings after confirming a paid Alipay-backed lookup. The skill is suited for entertainment-oriented constellation information, not decisions about health, finance, law, career, or relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may incur a paid Alipay-backed horoscope lookup without noticing the price or order details. <br>
Mitigation: Show the price, order details, privacy notice, and cancellation path before any payment flow begins. <br>
Risk: Plain-HTTP local testing could expose real queries or payment details. <br>
Mitigation: Use HTTPS for production and avoid real queries or payments in any plain-HTTP local test setup. <br>
Risk: Horoscope output could be mistaken for reliable advice for health, finance, legal, career, or relationship decisions. <br>
Mitigation: Present results as entertainment only and keep the no-scientific-basis disclaimer with the generated Markdown output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-constellation-a2a) <br>
- [聚合数据 A2A query endpoint](https://apis.juhe.cn/a2a/query.php) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown horoscope profile and fortune report after payment completion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the requested zodiac sign and period only; output should be based on returned API fields and include an entertainment disclaimer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
