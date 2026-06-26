## Description: <br>
Queries multiple threat intelligence services to enrich IPs, domains, URLs, and hashes with reputation, DNS, scanning, malware, and infrastructure context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nirhalfon](https://clawhub.ai/user/nirhalfon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, incident responders, and threat hunters use this skill to enrich IOCs across public and API-key threat intelligence services, compare service results, and produce triage outputs for investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or confidential IOCs may be sent to external threat intelligence providers, including public URLscan submissions. <br>
Mitigation: Query only indicators approved for external sharing; avoid `--services all`, bulk mode, and URLscan for confidential, internal, or customer indicators unless organizational policy permits it. <br>
Risk: API keys can be saved in the skill-local configuration file, and results may be cached locally. <br>
Mitigation: Prefer environment variables, restrict local file access, and clear saved configuration or cache data after sensitive investigations. <br>
Risk: Bulk enrichment and all-service queries can disclose many indicators at once and consume provider quotas or paid-service capacity. <br>
Mitigation: Limit service selection and batch size, review provider terms and rate limits, and use free triage services before broader enrichment when appropriate. <br>


## Reference(s): <br>
- [API Keys Setup Guide](references/api-keys.md) <br>
- [Service Documentation](references/services.md) <br>
- [Rate Limits Reference](references/rate-limits.md) <br>
- [Tutorial](TUTORIAL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI table, JSON, or Markdown threat intelligence results, with optional JSON or Markdown report files for bulk runs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on selected external services, configured API keys, provider rate limits, and local response caching.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
