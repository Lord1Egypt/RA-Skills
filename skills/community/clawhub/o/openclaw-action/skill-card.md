## Description:

GitHub Action for automated security scanning of agent workspaces that detects exposed secrets, prompt or shell injection, and data exfiltration patterns in PRs and commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this GitHub Action in CI to scan agent skill repositories for secrets, injection patterns, and potential exfiltration behavior before changes are merged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The action fetches and runs mutable remote scanner code while making inaccurate trust claims.

Mitigation: Prefer a version that vendors the scanner code or pins each downloaded scanner to immutable commits with verified hashes.

Risk: Downloaded scanner code runs in CI against repository contents.

Mitigation: Run it in an isolated CI job with read-only repository permissions, no unrelated secrets, and the narrowest workspace path practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atlaspa/skills/openclaw-action)
- [OpenClaw Security Suite](https://github.com/AtlasPA/openclaw-security)
- [openclaw-sentry](https://github.com/AtlasPA/openclaw-sentry)
- [openclaw-bastion](https://github.com/AtlasPA/openclaw-bastion)
- [openclaw-egress](https://github.com/AtlasPA/openclaw-egress)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands, Configuration]

**Output Format:** [GitHub Actions annotations, Markdown job summary, and action outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports findings-count and has-critical outputs; may fail the workflow when fail-on-findings is enabled and critical or high severity findings are present.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
