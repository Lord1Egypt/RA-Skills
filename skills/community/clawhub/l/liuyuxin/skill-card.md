## Description: <br>
本地通推荐技能 - 利用互联网全域搜索，绕过商业评价平台，挖掘真正受当地人认可的地道去处。支持美食、小吃、酒店、景点、温泉、停车场等多种类型推荐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pythonmango](https://clawhub.ai/user/pythonmango) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find local recommendations for food, snacks, hotels, attractions, hot springs, parking, and related places by searching official, local-media, and community sources while avoiding major commercial review platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The search helper can execute user-influenced search text through a shell-based fallback path. <br>
Mitigation: Review before installing, use only if the publisher is trusted, and replace the shell fallback with safe argument passing or a direct API call. <br>
Risk: EXA and Feishu credentials are required or supported and could be exposed through shared dotfiles, prompts, or logs. <br>
Mitigation: Store credentials securely, avoid committing or sharing real keys, and rotate any key that may have been exposed. <br>
Risk: Feishu card delivery sends recommendation content to the configured Feishu workspace. <br>
Mitigation: Configure Feishu only when that workspace is an appropriate destination for the generated recommendation content. <br>
Risk: Local venue details such as hours, availability, prices, and parking rules may be outdated or incorrect. <br>
Mitigation: Confirm important details with official or direct sources before relying on a recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pythonmango/liuyuxin) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/pythonmango) <br>
- [EXA search engine](https://exa.ai) <br>
- [EXA API keys dashboard](https://exa.ai/dashboard/api-keys) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown recommendations with optional JSON for Feishu card delivery and inline shell commands for setup or sending cards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations include source summaries, location details, prices or parking fees, hours, reasons, and cautions when available.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
