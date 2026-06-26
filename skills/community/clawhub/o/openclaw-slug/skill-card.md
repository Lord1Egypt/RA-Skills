## Description: <br>
Connects to the WHOOP Developer Platform through official OAuth, stores and refreshes tokens, fetches WHOOP v2 health and activity data, and renders daily or weekly summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinchengcool](https://clawhub.ai/user/gavinchengcool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and developers use this skill to authorize WHOOP access, fetch recovery, sleep, strain, workout, profile, and body measurement data, and produce concise summaries for chat or scheduled reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes unrelated trusted-partner healthcare API operations alongside WHOOP metric functionality. <br>
Mitigation: Review before installing and remove those partner endpoints or split them into a separate, tightly scoped partner-only skill. <br>
Risk: WHOOP credentials, client secrets, token files, and generated health summaries may expose sensitive personal data. <br>
Mitigation: Use the minimum WHOOP read scopes, keep secrets and token files private, and confirm before sending summaries to public or shared channels. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gavinchengcool/openclaw-slug) <br>
- [WHOOP API Quick Reference](references/whoop_api.md) <br>
- [Normalized Output Schema](references/output_schemas.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [WHOOP OpenAPI Specification](references/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or plain text summaries, JSON data files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Channel-aware rendering presets for generic, Discord, Slack, WhatsApp, and Telegram output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
