## Description: <br>
LMeterX Web Load Test analyzes a webpage URL, pre-checks discovered APIs, and creates LMeterX load-testing tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckyyc](https://clawhub.ai/user/luckyyc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn a website URL into LMeterX load-test tasks, including page analysis, API connectivity checks, and report links for created tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create remote load-test tasks for arbitrary websites with weak consent, credential, and transport-safety controls. <br>
Mitigation: Use only on systems you own or are explicitly authorized to test; require manual confirmation of the target URL, concurrency, duration, spawn rate, and authorization before execution. <br>
Risk: The bundled workflow uses a default LMeterX token and may send target URLs and discovered API details to the LMeterX service. <br>
Mitigation: Replace the default token with a user-scoped credential, avoid private or secret-bearing URLs, and confirm that sharing target details with the LMeterX service is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luckyyc/lmeterx-web-loadtest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary of discovered APIs, pre-check results, created task IDs, and LMeterX report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a target webpage URL and can use optional concurrency, duration, and spawn-rate parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
