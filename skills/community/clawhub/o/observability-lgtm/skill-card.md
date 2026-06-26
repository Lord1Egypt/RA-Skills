## Description: <br>
Set up a full local LGTM observability stack (Loki + Grafana + Tempo + Prometheus + Alloy) for FastAPI apps with one Docker Compose file, one Python import, and unified dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add local logs, metrics, traces, and Grafana dashboards to FastAPI applications with Docker Compose and a Python instrumentation helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Grafana setup grants unauthenticated admin access and may be unsafe on shared, remote, or production-like machines. <br>
Mitigation: Install only on a trusted local development machine; bind exposed ports to localhost and enable Grafana authentication or reduce anonymous access to Viewer before using it beyond local development. <br>
Risk: Logs and traces may contain secrets or personal data. <br>
Mitigation: Review telemetry contents before collection, avoid logging sensitive data, and treat stored local observability data according to the application's data handling requirements. <br>
Risk: Trace export can leave the machine if OTLP_ENDPOINT is configured to an external collector. <br>
Mitigation: Keep OTLP_ENDPOINT unset for local Tempo, or explicitly verify it points only to the intended collector before running instrumented applications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/observability-lgtm) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Local stack definition](artifact/assets/docker-compose.yml) <br>
- [FastAPI instrumentation helper](artifact/assets/lib/observability.py) <br>
- [Grafana dashboard](artifact/assets/config/grafana/dashboards/fastapi-overview.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and Python code blocks plus configuration file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker, Docker Compose, Python 3.10+, and a FastAPI application to instrument.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
