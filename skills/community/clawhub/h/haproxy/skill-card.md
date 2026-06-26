## Description: <br>
HAProxy load balancer reference. Frontend binds with ACL routing, backend server pools with health checks, balance algorithms (roundrobin/leastconn/source), SSL termination with SNI, stick-table rate limiting, and stats/Prometheus monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to retrieve HAProxy reference snippets for frontend routing, backend pools, health checks, SSL termination, stick-table rate limiting, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied HAProxy examples can expose administrative features, weak example passwords, relaxed TLS verification, reload commands, or runtime socket commands if applied directly to production systems. <br>
Mitigation: Review and adapt examples before use, especially stats admin settings, credentials, TLS verification choices, reload procedures, and runtime socket commands that can affect live traffic. <br>


## Reference(s): <br>
- [Haproxy on ClawHub](https://clawhub.ai/ckchzh/haproxy) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reference text with HAProxy configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script prints reference material only; it does not apply configuration changes itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
