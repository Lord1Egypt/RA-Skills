## Description:

臻选顾问 helps users query the 共健臻选 supplement catalog and receive product recommendations using catalog data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxbabby](https://clawhub.ai/user/foxbabby)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask about 共健臻选 supplement products, including categories, prices, claimed effects, inventory, and recommendations for common wellness needs. The skill steers purchases to the 共健臻选 WeChat mini-program.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can present supplement recommendations and health-related product claims as catalog guidance.

Mitigation: Review responses for medical neutrality and make clear that product suggestions are not a substitute for professional health advice.

Risk: The product catalog data is mutable and retrieved remotely, so prices, inventory, and claims can change outside the skill file.

Mitigation: Confirm remote catalog contents before deployment and periodically review product claims, prices, inventory, and availability.

Risk: The skill promotes a single WeChat mini-program as the purchase channel.

Mitigation: Disclose the commercial channel clearly and avoid presenting recommendations as neutral marketplace comparisons.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foxbabby/skills/gongjian-catalog)
- [Remote product catalog data](https://raw.githubusercontent.com/foxbabby/gongjian-catalog/master/products.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown product cards and recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include product names, prices, claimed effects, inventory counts, and the WeChat mini-program purchase channel.]

## Skill Version(s):

1.20260419.1133 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
