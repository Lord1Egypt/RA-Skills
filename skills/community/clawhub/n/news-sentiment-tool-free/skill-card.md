## Description: <br>
舆情情绪分析免费版 helps individual investors scan announcements, finance news, research reports, and social media for one stock, score sentiment from -10 to +10, and produce a sentiment summary with key events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External individual investors use this skill to monitor recent sentiment around a single stock and receive a sentiment score, event list, and lightweight decision-support summary. It is intended as a reference aid and does not replace investment advice or review of primary sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes a local Python-based workflow that may contact external finance, news, and social-media sources for stock symbols supplied by the user. <br>
Mitigation: Install only when network-backed data collection is acceptable, and review any supplied script before running it. <br>
Risk: The referenced execution script is not present in the artifact, so later-added code could introduce behavior not covered by this evidence package. <br>
Mitigation: Review and scan any script supplied later, especially before adding paid data-source API keys. <br>
Risk: Sentiment outputs can be incomplete, delayed, or misleading if sources are noisy, unavailable, or manipulated. <br>
Mitigation: Treat results as reference material and compare them with authoritative disclosures and human financial judgment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/news-sentiment-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and text report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include a sentiment thermometer, scored key events, source labels, confidence values, sentiment statistics, and reference-only action suggestions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
