## Description:

中国法律法规检索（得理科技） helps legal professionals, general users, and agents retrieve Chinese legal provisions, find related regulations, check validity status, and compare regulatory differences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolalam](https://clawhub.ai/user/coolalam)

### License/Terms of Use:

MIT-0

## Use Case:

External users, legal professionals, and agents use this skill to retrieve Chinese laws and regulations through Delilegal, summarize retrieved provisions, check legal validity status, and compare related provisions. It is a retrieval aid and should not be treated as legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API script disables TLS certificate verification while sending the configured API key and legal queries.

Mitigation: Review or fix TLS behavior before installation, remove disabled certificate checks, and rotate any key used with this version.

Risk: Retrieved legal content may be stale or incomplete for important decisions.

Mitigation: Treat outputs as retrieval aids and verify important legal conclusions against current official legal texts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolalam/skills/legal-retrieval)
- [Common regulation abbreviation mappings](references/regulation-mapping.md)
- [Legal retrieval examples](references/search-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown legal retrieval results with optional tables, quoted provisions, summaries, and shell command invocations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes validity-status labels and a reminder to verify important legal conclusions against current official texts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
