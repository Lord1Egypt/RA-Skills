## Description: <br>
Query TikTok data through MaxHub APIs for video details, user profiles, search, trends, comments, live streams, ads analytics, creator tools, shop/ecommerce, and crypto or signing utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, ecommerce operators, marketers, and data analysts use this skill to collect and analyze TikTok public data and MaxHub-supported account or creator analytics. Agents can use it to plan validated API calls, summarize returned data, and guide configuration with the required MaxHub API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evidence security summary says the skill mixes a claimed read-only scope with sensitive session-cookie, signing, device-registration, and at least one write-capable endpoint. <br>
Mitigation: Review before installing, keep automated use to public read-only lookups where possible, and require explicit human approval before invoking write, cookie, device-registration, or signing endpoints. <br>
Risk: The skill requires a MaxHub API key and may handle sensitive TikTok cookies or login-related inputs. <br>
Mitigation: Use a separate MaxHub API key and test TikTok accounts, rotate credentials regularly, and avoid exposing API keys, cookies, tokens, usernames, or passwords in prompts, logs, or client storage. <br>
Risk: Creator/account analytics and crypto or tool endpoints can involve consent-sensitive or platform-risk workflows. <br>
Mitigation: Use those endpoints only with clear user consent and a documented purpose; do not use signing or encryption utilities to bypass platform controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-tiktok) <br>
- [MaxHub API Console](https://www.aconfig.cn) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Endpoint Whitelist](artifact/references/endpoints_whitelist.yaml) <br>
- [Parameter Mappings](artifact/references/param-mappings.md) <br>
- [Tools and Crypto Reference](artifact/references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API response interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; API requests are sent to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
