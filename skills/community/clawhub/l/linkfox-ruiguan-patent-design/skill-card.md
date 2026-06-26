## Description: <br>
Guides agents through Ruiguan design patent infringement detection for product images, helping e-commerce sellers and IP professionals identify design patent, similarity, and TRO risks before listing products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce sellers, IP professionals, and agents use this skill to check whether a product image may resemble existing design patents across supported regions. It produces patent-risk summaries with similarity scores, TRO history, radar analysis, relevant patent images, and a reminder to consult an IP attorney. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product images, titles, descriptions, and patent-search context may be sent to external LinkFox/Ruiguan services. <br>
Mitigation: Use a dedicated LinkFox API key and avoid submitting confidential or pre-release product data unless the user is comfortable sharing it with those services. <br>
Risk: Feedback reporting may send feedback or conversation context to a separate LinkFox endpoint. <br>
Mitigation: Report feedback only when the user explicitly consents, and avoid including sensitive conversation details. <br>
Risk: Patent-risk results may be incomplete, outdated, or unsuitable as legal advice. <br>
Mitigation: Present results faithfully, keep the attorney-review reminder, and have a qualified IP professional review high-risk findings before business or legal action. <br>


## Reference(s): <br>
- [Ruiguan Design Patent Detection API Reference](references/api.md) <br>
- [ClawHub Release Page](https://clawhub.ai/linkfox-ai/linkfox-ruiguan-patent-design) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with JSON API request and response examples, plus optional shell command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LINKFOXAGENT_API_KEY and product image URLs to query external LinkFox/Ruiguan services; high-risk patents are expanded in detail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
