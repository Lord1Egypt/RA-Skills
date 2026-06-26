## Description: <br>
手机号码归属地查询，输入手机号码或手机号前7位，查询归属地省份/城市、区号、邮编、运营商和卡类型。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Chinese mobile number segment information, including province, city, area code, postal code, carrier, and card type. It supports single or batch lookups after the user configures a Juhe API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Phone numbers and the Juhe API key may be transmitted over an unencrypted HTTP request. <br>
Mitigation: Prefer an HTTPS Juhe endpoint if supported, review network behavior before use, and rotate keys that may have crossed untrusted networks. <br>
Risk: Passing the API key with the --key option can expose it through shell history or process listings. <br>
Mitigation: Use the JUHE_MOBILE_KEY environment variable or a protected local .env file instead of command-line key arguments. <br>
Risk: Phone number lookups can disclose personal or sensitive identifiers to an external API provider. <br>
Mitigation: Query only numbers the user is authorized to send to Juhe and keep the default masking behavior when displaying full numbers is unnecessary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/juhemcp/juhe-mobile-locate) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/juhemcp) <br>
- [Juhe Mobile Number Lookup API](https://www.juhe.cn/docs/api/id/11) <br>
- [Juhe Data Platform](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and tabular text output from the lookup script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JUHE_MOBILE_KEY credential; outputs may mask full phone numbers by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
