## Description:

Perform web searches and generate summarized answers with citations using the Kagi API and FastGPT for higher-quality results or rate-limit fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelasper](https://clawhub.ai/user/michaelasper)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Kagi Search API queries or FastGPT prompts for web research, ranked results, and summarized answers with citations when Kagi credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search and FastGPT queries are sent to Kagi using a user-supplied API token.

Mitigation: Do not include secrets or highly sensitive personal data in queries, and use Kagi credentials only in environments where this data sharing is acceptable.

Risk: Unexpected redirects could expose valuable API credentials if the client is not hardened.

Mitigation: Review and harden redirect handling before using the skill with valuable API credentials.

## Reference(s):

- [Kagi API quick reference](references/kagi-api.md)
- [Kagi API documentation](https://help.kagi.com/kagi/api/)
- [Kagi ClawHub skill page](https://clawhub.ai/michaelasper/skills/kagi)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration guidance]

**Output Format:** [Readable terminal text or JSON returned from Kagi API wrappers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied Kagi API token in KAGI_API_TOKEN or KAGI_API_KEY.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
