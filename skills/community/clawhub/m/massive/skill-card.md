## Description:

Bash CLI wrapper and OpenClaw skill for Massive's public REST API, supporting agent workflows that query market-data endpoints, use OpenClaw-style secret references, avoid secret leakage in logs, and integrate Massive responses into downstream pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw or Codex-style agents use this skill to query Massive REST market-data endpoints through a Bash CLI. It is intended for workflows that need JSON API responses, credential handling through secret references, pagination support, and safe command guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published package is missing the main scripts/massive executable.

Mitigation: Install or use the skill only when the package includes scripts/massive from a trusted source; regenerate the bundle if it is omitted.

Risk: Credential settings can expose the Massive API key if secret references or logs are handled carelessly.

Mitigation: Keep MASSIVE_API_KEY_REF and MASSIVE_API_KEY under trusted control, prefer secret references where supported, and avoid logging resolved secrets or raw secret-ref payloads.

Risk: Exec-style secret references can run commands to resolve credentials.

Mitigation: Use exec secret references only in runtimes that enforce provider sandboxing and policy controls.

Risk: A custom MASSIVE_BASE_URL can redirect requests and credentials away from the default Massive API origin.

Mitigation: Set MASSIVE_BASE_URL only when the alternate HTTPS service is intended to receive the API credential.

## Reference(s):

- [Massive REST Usage Notes](references/massive-api.md)
- [OpenClaw Secrets Integration](references/openclaw-secrets.md)
- [Security Requirements](references/security.md)
- [Bundle Manifest](BUNDLE_MANIFEST.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands; runtime CLI responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, jq, and a Massive API credential supplied through MASSIVE_API_KEY_REF or MASSIVE_API_KEY.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
