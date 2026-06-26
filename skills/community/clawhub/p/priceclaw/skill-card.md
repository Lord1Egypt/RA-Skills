## Description: <br>
Use when you need the price of a product or service, or have observed a price worth recording. Searches crowdsourced price data, submits new price observations, and votes on existing entries in PriceClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roundtoo](https://clawhub.ai/user/roundtoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use PriceClaw to find current prices, corroborate observed prices, and contribute new public price records with place, category, source, and observation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use and store a PriceClaw API key after authentication. <br>
Mitigation: Review the OAuth URL before approving it and save the API key only when the user explicitly wants future sessions to use PriceClaw without re-authenticating. <br>
Risk: Submitted prices, votes, and place edits affect crowdsourced public price records. <br>
Mitigation: Verify the place, product, price, source type, and observation date before writing, and avoid submitting private or sensitive information in notes or custom fields. <br>
Risk: Authenticated API requests are rate limited. <br>
Mitigation: Back off on 429 responses, honor Retry-After, and slow requests when rate-limit headers show few remaining calls. <br>


## Reference(s): <br>
- [PriceClaw Homepage](https://priceclaw.io) <br>
- [PriceClaw API Docs](https://priceclaw.io/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/roundtoo/priceclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration guidance] <br>
**Output Format:** [Markdown guidance with HTTP examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return price records, OAuth approval URLs, API key setup guidance, and submitted-price or vote confirmations.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
