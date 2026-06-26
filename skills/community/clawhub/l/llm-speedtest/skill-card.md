## Description: <br>
Ping major LLM providers in parallel and compare real API latency. Run with /ping <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chapati23](https://clawhub.ai/user/chapati23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run a quick live latency check across configured LLM providers when comparing response times or investigating whether a provider is slow or unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads LLM API keys from pass shared/ and makes live authenticated requests to configured providers. <br>
Mitigation: Install and run it only if that key source matches your setup, or adapt scripts/ping.sh to use your approved secret manager before execution. <br>
Risk: Running the latency test may create small provider charges. <br>
Mitigation: Use low-quota keys or restrict the script to selected providers when cost exposure must be tightly controlled. <br>
Risk: The skill sends live requests to external provider APIs during each test run. <br>
Mitigation: Review the provider list and run the skill only in environments where outbound API calls to those services are allowed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chapati23/llm-speedtest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown-formatted latency report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are sorted fastest to slowest and labeled with latency status badges.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
