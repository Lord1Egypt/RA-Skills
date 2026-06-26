## Description: <br>
Monitor helps agents guide Texas residential electricity users through address completion, candidate confirmation, ESIID and usage lookup, plan recommendations, self-service routing, and daily or weekly savings monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catkennel](https://clawhub.ai/user/catkennel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Texas residential electricity shoppers use this skill through an agent to confirm a service address, compare available plan options, route to a live Personalized Energy address page, and set a daily or weekly monitoring preference. <br>

### Deployment Geography for Use: <br>
United States - Texas electricity service addresses <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on external Personalized Energy and PowerLego services for Texas address, usage, and plan lookup. <br>
Mitigation: Use it only when sharing a Texas service address with those services is acceptable for the deployment. <br>
Risk: Provider API access is required for live lookup behavior. <br>
Mitigation: Configure the provider API token intentionally and keep credential handling outside user-facing conversations. <br>
Risk: Daily or weekly monitoring may imply alerts, retention, or opt-out expectations that are not provided by the skill alone. <br>
Mitigation: Treat monitoring as a recommendation unless the host separately provides opt-in, alert delivery, retention, and opt-out controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/catkennel/monitor-openclaw) <br>
- [Personalized Energy Texas electricity rates](https://www.personalized.energy/electricity-rates/texas) <br>
- [Address Completeness](artifact/references/address-completeness.md) <br>
- [Intent Routing](artifact/references/intent-routing.md) <br>
- [OpenClaw Execution Guide](artifact/references/openclaw-execution.md) <br>
- [Response Strategy](artifact/references/response-strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown guidance with address candidates, plan summaries, monitoring recommendations, and destination links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumer-facing responses should avoid internal implementation details and end with one concrete next step.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
