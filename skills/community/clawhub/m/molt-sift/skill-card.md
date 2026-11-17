## Description:

Data validation and signal extraction service for agents that sifts raw outputs such as JSON, text, and data streams to extract quality signals, validate against schemas, and score reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noizceera](https://clawhub.ai/user/noizceera)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Molt Sift to validate JSON, text, or stream outputs against schemas and domain rules, extract high-confidence signals, and return scored cleaned data. The skill also supports bounty validation workflows that claim jobs, submit validation results, and initiate Solana USDC payment records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports unattended bounty and payment workflows without enough controls.

Mitigation: Use local testing or mock bounty workflows until authentication, payout limits, rate limits, and hardened payment integrations are added.

Risk: The API server can listen on a public interface and process bounty/payment requests.

Mitigation: Bind the API to localhost or a protected network and place it behind access control before handling real jobs or funds.

Risk: Auto-claim mode may process jobs and initiate payment records without operator review.

Mitigation: Disable cron or unattended auto-claim mode for real funds until wallet isolation, job review, and payment approval checks are in place.

## Reference(s):

- [Molt Sift validation rules](references/rules.md)
- [Molt Sift ClawHub page](https://clawhub.ai/noizceera/skills/molt-sift)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI examples, Python examples, JSON result structures, and API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation results include status, score, cleaned data, issues, metadata, and optional payment status fields.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
