## Description: <br>
Run LLM Signal GEO analyst workflows from OpenClaw to fetch deterministic GEO action plans, check site health status, and execute or review hosted or self-hosted agent workflows with approval-safe guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImMythz](https://clawhub.ai/user/ImMythz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators use this skill to request LLM Signal GEO action plans, review prioritized recommendations, run status checks, and separate automatically safe actions from changes that require human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends an API key and site data to a configurable LLM Signal endpoint. <br>
Mitigation: Install only if the configured endpoint is trusted, prefer the official HTTPS base URL unless intentionally self-hosting, and use a scoped or revocable API key. <br>
Risk: Provider-labeled auto_safe actions may be automatically executed. <br>
Mitigation: Review auto_safe actions before allowing automatic execution and keep manual or assist actions behind explicit human approval. <br>
Risk: Persisted plan calls can store run history and outcomes remotely. <br>
Mitigation: Avoid sending sensitive operational or business data unless remote plan history storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ImMythz/llm-signal-geo-analyst) <br>
- [LLM Signal agent documentation](https://www.llmsignal.app/docs/agents) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with action details, command or diff scaffolds, and approval indicators] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LLMSIGNAL_BASE_URL, LLMSIGNAL_SITE_ID, LLMSIGNAL_API_KEY, and curl-compatible shell access; API access is limited to Growth and Pro plans.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
