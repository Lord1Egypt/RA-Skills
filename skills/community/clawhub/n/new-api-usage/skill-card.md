## Description: <br>
Query usage statistics and quota from a user-specified new-api endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang48](https://clawhub.ai/user/wang48) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to check quota, balance, token consumption, model-level usage, and recent usage records for a trusted new-api deployment with explicit endpoint and API-key inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends an API key to a user-specified new-api server. <br>
Mitigation: Use only trusted HTTPS base URLs, verify the endpoint before running commands, and prefer limited or revocable API keys. <br>
Risk: API keys passed as command-line arguments or query parameters may be exposed through shell history, process listings, server logs, or proxy logs. <br>
Mitigation: Avoid shared systems for sensitive checks, rotate exposed keys, and review local shell and server logging practices before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wang48/new-api-usage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script prints quota and usage summaries, model aggregates, or raw JSON depending on the selected command-line flags.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
