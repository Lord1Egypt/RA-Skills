## Description:

Local Guide helps agents search for local recommendations such as food, lodging, attractions, hot springs, parking, coffee, shopping, and nightlife while prioritizing official and local-community sources over commercial review platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pythonmango](https://clawhub.ai/user/pythonmango)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce local-place recommendations with addresses, phone numbers, hours, price ranges, reasons for recommendation, and practical cautions. It also supports optional Feishu card delivery when Feishu credentials and recipient context are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell-command paths could allow crafted search or card content to run local commands.

Mitigation: Patch shell execution before deployment by removing shell=True, passing command arguments as arrays, and avoiding shell echo for generated JSON.

Risk: Feishu recipient and reply identifiers may be misdirected if they are not validated.

Mitigation: Validate recipient ID formats and allowed targets before sending cards, and restrict Feishu app permissions to the minimum required scope.

Risk: Long-term plaintext API keys in shell startup files can expose EXA or Feishu credentials.

Mitigation: Store secrets in a managed secret store or short-lived environment injection mechanism instead of persistent shell profiles.

Risk: Local recommendation details such as hours, prices, and business status may become stale.

Mitigation: Tell users to confirm time-sensitive venue details before visiting, especially for phone numbers, hours, parking rates, and closures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pythonmango/skills/liuyuxin)
- [Publisher profile](https://clawhub.ai/user/pythonmango)
- [Exa search](https://exa.ai)
- [Exa API keys dashboard](https://exa.ai/dashboard/api-keys)
- [OpenClaw](https://openclaw.ai)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu send message API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type})
- [Feishu reply message API](https://open.feishu.cn/open-apis/im/v1/messages/{reply_to}/reply)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown recommendations with optional JSON-formatted Feishu card payloads and shell commands for sending cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include source notes, recommendation reasons, cautions, and venue details such as address, phone, hours, navigation address, price, parking rates, spaces, and charging availability when relevant.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact/README.md lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
