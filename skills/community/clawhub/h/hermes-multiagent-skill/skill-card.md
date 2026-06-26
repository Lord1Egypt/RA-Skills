## Description: <br>
Provides a local Python message router for coordinating multiple agents through topic subscriptions, task dispatch, completion events, and optional sessions_spawn lifecycle integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[briefness](https://clawhub.ai/user/briefness) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to coordinate local multi-agent workflows with sparse topic subscriptions instead of broad message broadcasts. It is suited for routing task, completion, and system-event payloads between cooperating agents in a single process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent payloads may contain secrets or sensitive content and are delivered to subscribed callbacks while also remaining in in-memory pending task records or the bounded message pool during the process lifetime. <br>
Mitigation: Avoid routing secrets unless every subscribed handler is trusted, sanitize payloads before publishing, and tune pending task TTL and message pool size for the deployment. <br>
Risk: The sessions_spawn integration depends on an external API and lifecycle coordination outside this skill. <br>
Mitigation: Use the core HermesRouter or HermesAgent APIs when sessions_spawn is unavailable, and call on_agent_exit during lifecycle cleanup to remove subscriptions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/briefness/hermes-multiagent-skill) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown documentation and Python API usage patterns that produce local message callbacks, task identifiers, and routing statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python 3.8+ standard-library components and does not create databases; sessions_spawn integration requires the external sessions_spawn API to be available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
