## Description: <br>
Provides HTTP request retry guidance and C sample code for exponential backoff, timeout control, connection reuse, transient failure handling, and HTTP 429 rate-limit handling. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[gatsby047-oss](https://clawhub.ai/user/gatsby047-oss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers can use this skill as sample C retry logic or educational guidance for designing resilient HTTP clients. It is most useful as a starting point for API clients, microservice calls, web scraping, and other HTTP workflows that need retry behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact is incomplete sample C HTTP retry code and does not perform real HTTP requests as written. <br>
Mitigation: Integrate a real HTTP client library, add tests, and verify timeout and failure handling before using it in deployed software. <br>
Risk: Retrying non-idempotent operations can duplicate payments, transfers, account changes, or other POST/PATCH side effects. <br>
Mitigation: Use idempotency keys, method-aware retry rules, and clear final-failure handling before enabling retries for state-changing requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gatsby047-oss/http-retry-c) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [http_retry.h](artifact/http_retry.h) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with C header code and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes configurable retry attempts, delay bounds, timeout settings, and helper functions; the HTTP execution path is sample code and requires real HTTP integration before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
