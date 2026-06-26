## Description: <br>
Probe any URL and check if it's up. Returns the HTTP status code, response latency in milliseconds, and a healthy/not-healthy verdict. Configurable timeout. Useful for checking if an API is available before calling it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Healthprobe to check whether a URL or API endpoint is reachable before calling it, including status code, latency, and a healthy verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local service can be used to contact any caller-supplied URL. <br>
Mitigation: Keep it bound to localhost, avoid probing untrusted URLs, and add URL allowlisting or private-network and metadata-IP blocking before shared, cloud, or internet-facing use. <br>


## Reference(s): <br>
- [Healthprobe Skill Page](https://clawhub.ai/mirni/healthprobe) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON response from a local FastAPI endpoint, with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns healthy, status_code, latency_ms, and error fields; timeout_ms accepts 100 to 30000 milliseconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, created 2026-04-13T08:07:13Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
