## Description: <br>
Probe and verify whether an OpenAI-compatible baseURL is a real single-model endpoint or a multi-model aggregation pool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit OpenAI-compatible model providers, compare endpoint behavior, and decide whether a provider should be treated as a primary route, fallback route, or avoided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses user-supplied API credentials to probe model providers. <br>
Mitigation: Use scoped or temporary API keys where possible and verify the target base URL before probing. <br>
Risk: Terminal output may include response previews or provider error messages. <br>
Mitigation: Avoid sharing raw probe output publicly and redact sensitive provider details before distribution. <br>
Risk: Public API behavior alone cannot prove official upstream model provenance. <br>
Mitigation: Treat final judgments as confidence-based routing guidance and confirm high-stakes provider claims through contractual or vendor documentation. <br>


## Reference(s): <br>
- [Provider Probe Checklist](references/provider-probe-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional JSON probe results and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider URLs, model IDs, endpoint compatibility findings, latency summaries, and confidence judgments.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
