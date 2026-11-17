## Description:

Lieutenant scans messages, agent cards, and agent-to-agent communications for prompt injection, jailbreaks, data exfiltration, and other malicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jd-delatorre](https://clawhub.ai/user/jd-delatorre)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use Lieutenant to scan untrusted prompts, agent cards, and A2A communications before an agent processes them. It supports local checks, JSON reporting, and optional API-assisted or semantic analysis when credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote agent verification can fetch arbitrary URLs.

Mitigation: Run remote verification in an isolated environment and verify only trusted or intentionally tested URLs.

Risk: API mode can send scanned text or agent cards to external services.

Mitigation: Avoid API mode for confidential prompts, agent cards, credentials, or internal metadata unless the configured endpoint and data handling are trusted.

Risk: Unpinned repository or package installation can change behavior over time.

Mitigation: Pin repository or package versions before installation or deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jd-delatorre/skills/lieutenant)
- [TrustAgents](https://trustagents.dev)
- [TrustAgents API Docs](https://trustagents.dev/docs)
- [TrustLayer GitHub Repository](https://github.com/jd-delatorre/trustlayer)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and Python examples; CLI commands can emit human-readable text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional semantic and API modes require OPENAI_API_KEY or TRUSTAGENTS_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
