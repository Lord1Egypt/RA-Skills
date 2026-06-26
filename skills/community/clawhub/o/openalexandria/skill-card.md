## Description: <br>
Query and submit artifacts to the OpenAlexandria federated knowledge protocol (reference node by default). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[havneco](https://clawhub.ai/user/havneco) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use OpenAlexandria to query a federated knowledge node for cached research entries and, when authorized, submit JSON research bundles for later reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to upload research bundles to an external federated service without clear privacy review or user confirmation. <br>
Mitigation: Use query-only behavior by default, inspect and minimize any JSON bundle before submission, confirm the destination node, and avoid uploading secrets or confidential, customer, proprietary, or regulated content. <br>


## Reference(s): <br>
- [OpenAlexandria skill page](https://clawhub.ai/havneco/openalexandria) <br>
- [OpenAlexandria publisher profile](https://clawhub.ai/user/havneco) <br>
- [OpenAlexandria reference node](https://openalexandria.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses python3 and optional OPENALEXANDRIA_BASE_URL and OPENALEXANDRIA_API_KEY environment variables.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
