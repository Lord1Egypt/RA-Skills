## Description: <br>
Amazon Alexa For Shopping helps agents ask Amazon's storefront Alexa shopping assistant natural-language shopping questions and return answers, product recommendation groups, ASINs, links, and follow-up questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for conversational Amazon shopping research, including product discovery, recommendation comparison, page-anchored questions, and follow-up prompt generation. <br>

### Deployment Geography for Use: <br>
Global, subject to Amazon Alexa shopping availability and LinkFox service access. <br>

## Known Risks and Mitigations: <br>
Risk: Shopping prompts, Amazon page URLs, and feedback text may be sent to LinkFox services. <br>
Mitigation: Use only with user awareness, avoid account credentials, payment details, order IDs, private business information, or sensitive URLs, and strip unnecessary tracking or query parameters. <br>
Risk: The skill requires a LinkFox API key. <br>
Mitigation: Store LINKFOXAGENT_API_KEY as an environment secret, do not paste it into prompts or logs, and rotate it if exposed. <br>
Risk: Alexa-driven recommendations can vary and may not represent all relevant Amazon results. <br>
Mitigation: Present outputs as live shopping guidance and verify product availability, price, and suitability on Amazon before purchase decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-amazon-alexa-for-shopping) <br>
- [Amazon Alexa shopping API reference](references/api.md) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown report by default, or structured JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product groups, ASINs, product links, prices, ratings, screenshots, follow-up questions, status codes, latency, token cost, and task identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
