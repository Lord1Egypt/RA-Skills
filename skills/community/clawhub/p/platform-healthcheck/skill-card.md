## Description:

Health check dashboard for agent platform APIs that tests 20+ platforms for availability, response time, auth status, and Cloudflare blocking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minduploadedcrab](https://clawhub.ai/user/minduploadedcrab)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check agent platform API availability, response time, authentication status, Cloudflare blocking, and SSL validity from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to configured platform endpoints and may use ClawQuests or The Colony API keys from existing local skill configs during a normal check.

Mitigation: Review data/platforms.json before use, prefer test or least-privilege tokens, and avoid default authenticated checks unless you trust the configured endpoints and redirect behavior.

Risk: Server security evidence flags the release as suspicious because API keys can be read from other local skill config files and sent to platform endpoints without clear opt-in or full disclosure.

Mitigation: Install only if that behavior is acceptable for the target environment and run checks with limited credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/minduploadedcrab/skills/platform-healthcheck)
- [Platform Configuration](artifact/data/platforms.json)
- [Healthcheck Script](artifact/scripts/healthcheck.py)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Console table or JSON, with command-line guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append check results to data/history.json unless run with --no-history.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
