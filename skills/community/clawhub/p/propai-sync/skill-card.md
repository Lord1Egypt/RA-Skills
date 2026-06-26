## Description: <br>
Maintain and operate the PropAI Sync monorepo, including hosted-platform BYOK API validation, Railway deployment checks, scoped tests, build gates, hosted smoke checks, and ClawHub-ready publishing steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalgojha](https://clawhub.ai/user/vishalgojha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill while working in the PropAI Sync monorepo to run quality gates, validate hosted BYOK API behavior, check Railway deployments, and prepare ClawHub skill releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted smoke validation can generate or expose bootstrap API keys during endpoint checks. <br>
Mitigation: Treat bootstrap API keys as sensitive, keep them out of handoff notes, terminal logs, screenshots, and shared CI output, and rotate or revoke test keys after validation. <br>
Risk: Deployment validation can fail or give misleading confidence if non-2xx endpoint responses are ignored. <br>
Mitigation: Treat any non-2xx response as a failing gate and record endpoint outcomes before handoff. <br>


## Reference(s): <br>
- [PropAI Sync ClawHub skill page](https://clawhub.ai/vishalgojha/propai-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, validation steps, and JSON smoke-check output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The hosted smoke script prints a JSON summary of endpoint validation and records gateway logs under a temporary job-log directory.] <br>

## Skill Version(s): <br>
2026.2.28 (source: server release metadata, created 2026-03-05T22:02:00Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
