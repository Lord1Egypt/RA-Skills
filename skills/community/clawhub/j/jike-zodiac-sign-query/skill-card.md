## Description: <br>
Queries Jike API for zodiac sign characteristics, ruling house, polarity, ruling planet, lucky color, lucky number, date range, and gender-specific traits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to look up zodiac sign information for traditional culture, everyday reference, or compatibility-related questions. It runs a Python helper that returns readable Chinese text by default or raw JSON when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Zodiac lookup terms and the Jike AppKey are sent to Jike's API. <br>
Mitigation: Install only when that data sharing is acceptable and prefer a dedicated AppKey for this skill. <br>
Risk: Passing the AppKey with --key may expose it through shell history. <br>
Mitigation: Provide the key through JIKE_ZODIAC_SIGN_QUERY_KEY or JIKE_APPKEY instead of command-line arguments. <br>
Risk: The optional JIKE_API_BASE_URL override can redirect requests and credentials to another endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless intentionally using a trusted compatible endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-zodiac-sign-query) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [Jike zodiac sign API endpoint](https://api.jikeapi.cn/v1/zodiac_sign) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese text or JSON from a command-line Python helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Jike AppKey provided through JIKE_ZODIAC_SIGN_QUERY_KEY or JIKE_APPKEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
