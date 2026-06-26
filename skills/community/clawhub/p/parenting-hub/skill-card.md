## Description: <br>
Parenting Hub provides read-only, source-linked parenting guidance from the public Mom AI Agent evidence intelligence API with explicit scope, urgency, source, and coverage boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jupitlunar](https://clawhub.ai/user/jupitlunar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve source-linked parenting answers, safety boundaries, urgency guidance, and next reading paths from Mom AI Agent's public KB and insight API surfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled crawler playbook could lead an agent with matching local project access to run scraping or ingestion workflows despite the normal skill posture being read-only. <br>
Mitigation: Remove the crawler playbook reference before deployment or restrict the agent environment so it cannot execute those operational scraping and ingestion steps. <br>
Risk: Parenting and postpartum answers may be mistaken for individualized medical advice if evidence scope, urgency, or coverage boundaries are omitted. <br>
Mitigation: Keep answers constrained to returned public API evidence, preserve urgent escalation language for high-risk scenarios, and avoid diagnosis, treatment selection, or clearance language. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jupitlunar/parenting-hub) <br>
- [Mom AI Agent public KB API](https://www.momaiagent.com/api/kb) <br>
- [API Reference](references/api.md) <br>
- [Architecture Boundary](references/architecture.md) <br>
- [High-Risk Examples](references/high-risk-examples.md) <br>
- [Current-Site Deep Search Playbook](references/current-site-deep-search-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise Markdown-style parenting guidance with source, scope, urgency, and read-next sections when supported by the API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public API retrieval; no private user data, account actions, or write operations are part of the normal skill workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
