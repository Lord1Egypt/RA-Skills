## Description: <br>
Converts Markdown text into Feishu Post rich text JSON for message and bot workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KillingJacky](https://clawhub.ai/user/KillingJacky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation authors use this skill to convert Markdown content into Feishu Post JSON for rich-text messages, bots, and notification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted messages may mention users or everyone if the input includes Feishu at-mention tags. <br>
Mitigation: Review generated JSON before sending it through a Feishu bot or API, especially content containing at-mentions. <br>
Risk: Image elements require Feishu image keys rather than ordinary image URLs. <br>
Mitigation: Upload images to Feishu first and provide valid image_key values before using generated image blocks. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Feishu Post JSON, pretty-printed or compact] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default locale key is zh_cn; compact mode produces single-line JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
