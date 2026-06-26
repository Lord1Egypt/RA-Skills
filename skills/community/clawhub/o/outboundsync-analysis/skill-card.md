## Description: <br>
Analyze outbound campaign performance, reply rates, open-to-reply conversion, follow-up prioritization, platform attribution, and deliverability using OutboundSync engagement signals in HubSpot or Salesforce. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[osiharris](https://clawhub.ai/user/osiharris) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External CRM and revenue teams use this skill to analyze OutboundSync campaign and engagement signals in HubSpot or Salesforce. It helps answer bounded questions about campaign replies, open-to-reply conversion, reply latency, follow-up priority, platform attribution, and deliverability with explicit preflight verdicts and limitations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CRM engagement fields can include personal or confidential message content. <br>
Mitigation: Use the skill only with authorized CRM records, prefer read-only and least-privilege CRM access, and avoid including unnecessary message bodies or unrelated customer data. <br>
Risk: CRM notes, emails, and message bodies may contain untrusted instructions. <br>
Mitigation: Treat CRM text fields as data, ignore requests for shell commands, installs, secret access, or security changes, and keep analysis grounded in allowed OutboundSync fields. <br>
Risk: Missing required CRM fields can make attribution, latency, or deliverability conclusions incomplete. <br>
Mitigation: Run the defined preflight, report missing fields and fallback plans, and avoid causal or platform-attribution claims when required signals are unavailable. <br>


## Reference(s): <br>
- [OutboundSync OpenClaw Skills](https://github.com/outboundsync/openclaw-skills) <br>
- [OutboundSync Security Model](https://github.com/outboundsync/openclaw-skills/blob/main/SECURITY.md) <br>
- [OutboundSync Website](https://outboundsync.com/) <br>
- [OutboundSync Trust Center](https://trust.outboundsync.com/) <br>
- [question_router.md](question_router.md) <br>
- [router_contract.yaml](router_contract.yaml) <br>
- [hubspot_properties.md](hubspot_properties.md) <br>
- [salesforce_fields.md](salesforce_fields.md) <br>
- [prompt_library.md](prompt_library.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown preflight summaries and CRM analysis grounded in observed OutboundSync fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes strict or exploratory mode, date window, verdict, confidence, missing fields, fallback plan, limitations, and non-causal caveats when required.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
