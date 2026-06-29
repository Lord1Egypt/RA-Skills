## Description: <br>
Async Python patterns via asyncio and aiohttp for I/O-bound concurrency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to apply asyncio and aiohttp patterns for I/O-bound Python work, including concurrent requests, rate limiting, timeouts, cancellation, testing, and avoiding blocking calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Python or async-related triggers may activate this skill when a narrower Python skill is intended. <br>
Mitigation: Use narrower trigger configuration or agent routing when multiple Python guidance skills are installed. <br>
Risk: Generated async examples may be applied without adapting timeouts, rate limits, cancellation, or blocking-call checks to the target system. <br>
Mitigation: Review proposed code against the target application's concurrency limits, external service policies, and test coverage before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-parseltongue-python-async) <br>
- [Homepage from ClawDIS metadata](https://github.com/athola/claude-night-market/tree/master/plugins/parseltongue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no direct tool or network execution.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
