## Description: <br>
一键配置电商直播环境（频道、商品、优惠券） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terryso](https://clawhub.ai/user/terryso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and livestream operators use this skill to configure a PolyV e-commerce livestream setup, including account checks, channel setup, sample products, and coupons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask for a long-lived PolyV AppSecret in chat. <br>
Mitigation: Do not paste AppSecret values into chat; configure credentials through a safer local method when available and rotate any secret that has already been shared. <br>
Risk: The setup commands can create or modify PolyV account resources. <br>
Mitigation: Use least-privilege or test credentials, run the setup only in the intended PolyV account, and review the created channel, product, and coupon afterward. <br>
Risk: The workflow runs an external PolyV CLI through npx. <br>
Mitigation: Install only when you trust the PolyV CLI source and intend to create PolyV resources in that account. <br>


## Reference(s): <br>
- [PolyV Console](https://console.polyv.net/) <br>
- [ClawHub skill page](https://clawhub.ai/terryso/polyv-e-commerce-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request PolyV AppID and AppSecret when local authentication is not configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
