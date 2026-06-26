## Description: <br>
Queries published MaxKB agents for LLM selection, then routes a question to the chosen agent and returns the answer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuruibin](https://clawhub.ai/user/liuruibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let a host LLM discover published MaxKB agents, choose the best match for a user question, and return that agent's response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User questions and selected prompts are sent to the configured MaxKB agent service. <br>
Mitigation: Use only a trusted, approved MaxKB deployment and avoid sending secrets, regulated data, or private customer content unless that deployment is approved for the data. <br>
Risk: The skill relies on MaxKB credentials or login details stored in the local environment. <br>
Mitigation: Protect the .env file and prefer a dedicated least-privilege account or scoped token over broad admin credentials. <br>
Risk: An untrusted or misconfigured MaxKB endpoint could expose credentials or return unreliable answers. <br>
Mitigation: Configure a trusted HTTPS MaxKB endpoint and review the deployment configuration before use. <br>


## Reference(s): <br>
- [ClawHub MaxKB skill page](https://clawhub.ai/liuruibin/maxkb) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls] <br>
**Output Format:** [JSON strings containing published agent metadata or the selected agent answer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured MaxKB endpoint and credentials; user questions are sent to the configured MaxKB instance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
