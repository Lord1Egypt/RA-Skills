## Description: <br>
Provides local food, lodging, attraction, hot spring, shopping, nightlife, and parking recommendations using multi-round web search that prioritizes official and local sources while excluding major commercial review platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pythonmango](https://clawhub.ai/user/pythonmango) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to request local recommendations for restaurants, snacks, hotels, attractions, hot springs, shopping, nightlife, coffee, and parking. The skill gathers and formats recommendations with location details, pricing or fees, hours, supporting reasons, caveats, and source notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ClawHub security summary reports unsafe shell execution from user-controlled search text in the shell-based search fallback. <br>
Mitigation: Install only if the publisher is trusted, configure EXA and the preferred search path to avoid the fallback, and patch or remove shell=True before using untrusted location or type text. <br>
Risk: Feishu output can send recommendation cards through configured app credentials. <br>
Mitigation: Use least-privilege Feishu credentials and enable Feishu output only for intended chats or users. <br>
Risk: Recommendation details such as hours, prices, parking fees, and business status may change after search results are collected. <br>
Mitigation: Ask users to confirm important details with the venue or official source before travel or purchase decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/pythonmango/local-guide) <br>
- [Publisher profile](https://clawhub.ai/user/pythonmango) <br>
- [EXA search engine](https://exa.ai) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown recommendations with optional Feishu card JSON and shell command invocation for card delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EXA_API_KEY for search; optional FEISHU_APP_ID and FEISHU_APP_SECRET enable Feishu card output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
