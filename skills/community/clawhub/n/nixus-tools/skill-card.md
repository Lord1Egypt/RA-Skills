## Description: <br>
Free agentic tools API at nixus.pro. No API key needed. Magic 8-Ball, Roast Machine, Confessional, Last Words, Deadpool predictions. Fun interactive tools any agent can call via simple HTTP. 30 req/min rate limit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to call free entertainment-oriented HTTP tools for Magic 8-Ball answers, roasts, confessional text, last-words prompts, and technology deadpool predictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted to the examples is sent to nixus.pro. <br>
Mitigation: Use only non-sensitive text and avoid passwords, tokens, private prompts, personal details, internal business information, or regulated data. <br>
Risk: The tool depends on unauthenticated remote HTTP endpoints and may be unavailable or rate limited. <br>
Mitigation: Design agent workflows to handle request failures and the documented 30 requests per minute per IP rate limit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cassh100k/nixus-tools) <br>
- [Nixus tools discovery endpoint](https://nixus.pro/api/tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and HTTP API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls remote nixus.pro endpoints with a documented 30 requests per minute per IP rate limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
