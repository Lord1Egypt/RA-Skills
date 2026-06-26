## Description: <br>
Make (formerly Integromat) API integration with managed authentication for managing scenarios, organizations, teams, connections, data stores, hooks, and templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to inspect and manage Make resources through Maton-managed authentication, including scenarios, teams, organizations, connections, webhooks, data stores, templates, and incomplete executions. It is intended for interactive API work where the agent proposes or executes calls with explicit confirmation for write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and brokered OAuth connection to access Make resources. <br>
Mitigation: Install only when Maton is trusted to broker the Make account, and keep MATON_API_KEY scoped and protected. <br>
Risk: Write actions can create, update, start, stop, or delete resources in Make. <br>
Mitigation: Before approving a write action, verify the target organization, team, scenario, hook, data store, connection, or template ID and the intended effect. <br>
Risk: Started scenarios and created hooks or data stores may persist after the agent conversation ends. <br>
Mitigation: Track resources created or started during the session and explicitly stop or delete anything that should not continue running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/make-api) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton homepage](https://maton.ai) <br>
- [Make API Documentation](https://developers.make.com/api-documentation) <br>
- [Make API Reference](https://developers.make.com/api-documentation/api-reference) <br>
- [Make Help Center](https://www.make.com/en/help) <br>


## Skill Output: <br>
**Output Type(s):** [api calls, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline HTTP endpoints, shell commands, Python and JavaScript examples, and JSON request or response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and the MATON_API_KEY environment variable; write actions can create, modify, start, stop, or delete persistent Make resources.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
