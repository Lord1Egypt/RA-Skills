## Description: <br>
Query and troubleshoot NextDNS via the NextDNS API, especially when NextDNS is used as Technitium DNS upstream. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naamah75](https://clawhub.ai/user/naamah75) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who administer NextDNS profiles use this skill to inspect profile configuration, analyze DNS status, review recent logs, and troubleshoot blocked domains or Technitium upstream behavior before making configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: NextDNS API access can expose sensitive DNS account data and DNS logs that reveal browsing or device activity. <br>
Mitigation: Use specific profiles and time ranges, avoid pasting sensitive domains unless needed, keep API keys out of output, and rotate or revoke the API key when the skill is no longer used. <br>
Risk: Profile edits, denylist or allowlist changes, and log clearing can change DNS behavior or remove useful diagnostic history. <br>
Mitigation: Require explicit user confirmation before writes, deletes, monitoring, or log-clearing actions, and export the current profile before configuration changes. <br>
Risk: The NextDNS API is marked beta and response shapes may change. <br>
Mitigation: Handle API errors and response changes defensively, and verify endpoint behavior against the bundled API summary or upstream documentation before relying on results. <br>


## Reference(s): <br>
- [NextDNS API summary](references/api-summary.md) <br>
- [NextDNS API documentation](https://nextdns.github.io/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NEXTDNS_API_KEY and optional NEXTDNS_PROFILE_ID for authenticated NextDNS API inspection.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
