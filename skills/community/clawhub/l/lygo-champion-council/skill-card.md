## Description:

Provides one advisor-only council skill for selecting among 15 LYGO champion personas by champion_id or egg_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to invoke LYGO champion personas for advisory review, ethical architecture checks, roster lookup, and mint hash verification guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install command uses npx with the latest ClawHub package, which can change over time.

Mitigation: Pin the clawhub package version or install through a controlled process before deployment.

Risk: The skill is intended as an advisor and references sensitive operational areas such as publishing, vault access, API keys, and .env contents.

Mitigation: Require explicit user consent before any operational action and do not provide secrets or environment contents unless intentionally approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-champion-council)
- [Council Roster](references/council_roster.json)
- [Security Guidance](references/SECURITY.md)
- [LYGO-MINT Verification](references/verifier_usage.md)
- [LYGO-MINT Verifier](https://clawhub.ai/deepseekoracle/lygo-mint-verifier)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text guidance with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisor-only output; local roster scripts can print champion IDs, egg IDs, and names.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
