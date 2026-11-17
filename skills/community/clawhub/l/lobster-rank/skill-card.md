## Description:

Scans locally installed OpenClaw skills, submits structural metadata to the Lobster ranking server for scoring, and helps the user confirm leaderboard upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bifang988](https://clawhub.ai/user/bifang988)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to evaluate their locally installed skill set, review the returned score, and optionally publish the result to the Lobster leaderboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send installed skill names, descriptions, structural metadata, heuristic signals, and log-availability status to the Lobster ranking service.

Mitigation: Run with --dry-run first, review the generated payload, and submit only when the user is comfortable sharing that metadata.

Risk: The API endpoint is configurable through --api-url or LOBSTER_API_URL, which could redirect submitted metadata and API-key-authenticated requests to an untrusted service.

Mitigation: Use the default endpoint unless the alternative endpoint is fully trusted.

Risk: Authentication uses a Lobster API key from a command-line flag, OPENCLAW_API_KEY, or local OpenClaw configuration.

Mitigation: Use a revocable API key and avoid exposing it in shared shell history, logs, or screenshots.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bifang988/skills/lobster-rank)
- [Publisher profile](https://clawhub.ai/user/bifang988)
- [Lobster Rank leaderboard](https://lobster-rank.wondercv.com)
- [Lobster Rank account page](https://lobster-rank.wondercv.com/me)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and terminal output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print JSON payloads in dry-run mode and score results returned by the ranking service.]

## Skill Version(s):

3.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
