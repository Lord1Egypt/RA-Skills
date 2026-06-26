## Description: <br>
Implements HTTP request retries with exponential backoff and a configurable circuit breaker to reduce transient failures and prevent cascading errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qwe123sddfsdfs](https://clawhub.ai/user/qwe123sddfsdfs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to add retry handling, exponential backoff, timeouts, circuit breaker state management, and failure statistics to JavaScript HTTP clients that call unreliable services or third-party APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retries can repeat requests that change data, especially POST, PUT, PATCH, delete, payment, account-change, or publishing operations. <br>
Mitigation: Use idempotency keys where possible, restrict retries to safe or explicitly idempotent operations, and avoid sending sensitive data to untrusted endpoints. <br>
Risk: Aggressive retry settings can add latency or increase load on an already degraded dependency. <br>
Mitigation: Tune retry counts, delays, jitter, timeouts, and circuit breaker thresholds for the service, and monitor failure rate, retry rate, and circuit state before production rollout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qwe123sddfsdfs/http-retry-circuit-breaker) <br>
- [README](artifact/README.md) <br>
- [Skill usage guide](artifact/SKILL.md) <br>
- [Performance guide](artifact/PERFORMANCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes configurable retry counts, backoff delays, timeout values, retryable status codes, circuit breaker thresholds, event hooks, and runtime statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, manifest.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
