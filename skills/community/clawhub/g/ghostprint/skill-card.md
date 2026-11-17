## Description:

Ghostprint sends behaviorally randomized LLM requests to configured providers on a schedule to make usage profiles less personally identifying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alarawms](https://clawhub.ai/user/alarawms)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to generate scheduled synthetic LLM traffic, inspect run statistics, and configure provider-specific noise behavior for privacy-oriented usage masking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally sends automated synthetic LLM requests from configured accounts.

Mitigation: Install it only when that behavior is desired, review provider policies and expected costs, and keep noise volume proportional to real usage.

Risk: Provider credentials may be reused for both real and synthetic traffic, allowing account-level correlation.

Mitigation: Use separate, low-privilege API keys or accounts dedicated to noise traffic.

Risk: Custom provider base URLs can send credentials and traffic to unintended endpoints.

Mitigation: Avoid custom base_url values unless credentials are endpoint-specific and the endpoint has been reviewed.

Risk: The standalone cron installer creates persistent scheduled execution.

Mitigation: Use --install-cron only when persistent background execution is intended, and inspect or remove the crontab entry manually when no longer needed.

Risk: The documented install path clones from a moving source branch.

Mitigation: Pin installation to a reviewed commit or release before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alarawms/skills/ghostprint)
- [Publisher Profile](https://clawhub.ai/user/alarawms)
- [Anti-Fingerprint Design](ANTI-FINGERPRINT.md)
- [README](README.md)
- [Declared Project Source](https://github.com/alarawms/ghostprint)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, inline shell commands, configuration snippets, and plain-text tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OpenClaw tool output includes immediate noise-run results and run statistics; standalone usage emits command-line status and metadata-only logs.]

## Skill Version(s):

3.0.1 (source: ClawHub release evidence; artifact frontmatter and package metadata report 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
