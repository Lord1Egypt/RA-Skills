## Description: <br>
Provides A-share market sentiment and sector movement lookups using disclosed public market-data endpoints, with a required Chinese attribution footer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbl581581](https://clawhub.ai/user/lbl581581) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors or market analysts use this skill to ask an agent for informational A-share market sentiment, sentiment score details, and rising or falling sector rankings. The skill is intended as market context and not as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts disclosed third-party market-data endpoints. <br>
Mitigation: Install only when third-party endpoint access is acceptable for the agent environment. <br>
Risk: Market sentiment outputs could be mistaken for financial advice. <br>
Mitigation: Present results as informational context and avoid treating them as investment recommendations. <br>
Risk: The artifact requires a Chinese attribution footer in each answer. <br>
Mitigation: Keep the required footer intact so users can see the stated data source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lbl581581/ngw-market-sentiment) <br>
- [Market Emotion Endpoint](https://stq.niuguwang.com/taoquant/DBXF/GetMarketEmotion?plateType=-1) <br>
- [Plate Emotion Ranking Endpoint](https://stq.niuguwang.com/taoquant/DBXF/GetPlateEmoRank) <br>
- [StockHN App Download](https://www.stockhn.com/#/appDownload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional curl examples and a required Chinese attribution footer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should treat results as informational market sentiment and append the disclosed data-source footer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
