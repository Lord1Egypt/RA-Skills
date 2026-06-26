## Description: <br>
Scans e-commerce listing text for possible trademark matches and infringement risk across supported regions using the LinkFox Ruiguan text trademark API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce sellers and listing operators use this skill to check product titles, descriptions, and bullet points for text trademark risk before publishing listings. It helps surface matched trademarks, region coverage, risk scores, blacklist and whitelist entries, and review recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send listing text to LinkFox services and includes feedback reporting to a separate LinkFox endpoint. <br>
Mitigation: Use only listing text that is appropriate to share with LinkFox, avoid secrets or unreleased business-sensitive details, and approve or redact any feedback report before it is sent. <br>


## Reference(s): <br>
- [Ruiguan Text Trademark API Reference](references/api.md) <br>
- [ClawHub Release Page](https://clawhub.ai/linkfox-ai/linkfox-ruiguan-text-trademark) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command examples and tabular trademark-risk analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY for live API calls; productTitle and productText are each limited to 1000 characters, and API results are capped at 500.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
