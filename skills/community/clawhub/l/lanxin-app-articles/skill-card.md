## Description: <br>
Formats Lanxin official image-and-text article card requests as clean appArticles JSON with the required article fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamdacai](https://clawhub.ai/user/iamdacai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or external users preparing Lanxin article-card messages use this skill to produce raw appArticles JSON for image-and-text article cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad article or image-text triggers may activate JSON-only output when the user did not intend to create a Lanxin article card. <br>
Mitigation: Confirm the user wants a Lanxin appArticles payload before relying on the generated JSON. <br>
Risk: Generated titles, URLs, image links, or recipients may be incorrect or unsuitable for the intended message. <br>
Mitigation: Review all generated fields and recipient context before sending or using the payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iamdacai/lanxin-app-articles) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/iamdacai) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces only raw appArticles JSON, without Markdown fences or explanatory text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
