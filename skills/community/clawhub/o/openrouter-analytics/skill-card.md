## Description:

Review OpenRouter usage, spend, analytics, per-key reporting, and request-level troubleshooting data via the OpenRouter API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8)

### License/Terms of Use:


## Use Case:

Developers and teams operating OpenRouter use this skill to monitor spending, usage trends, credit balances, per-key consumption, and detailed generation incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper automatically reads ~/.openclaw/.env and the current directory's .env, which can load broad OpenRouter credentials in unintended workspaces.

Mitigation: Run it from a controlled directory with least-privilege OpenRouter keys and review which environment files are present before execution.

Risk: Analytics, CSV, report, and raw JSON outputs can contain sensitive account, key usage, request, token, cost, and latency data.

Mitigation: Treat generated reports and CSV or JSON output as sensitive account data, and avoid --raw unless the full API response is needed.

## Reference(s):

- [OpenRouter Usage & Troubleshooting Endpoints](references/endpoints.md)
- [OpenRouter API](https://openrouter.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands; helper commands can emit JSON, CSV, or Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive account, key usage, request ID, token, cost, and latency data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
