## Description:

Runtime prompt injection detection for AI agents. Checks tool outputs for hidden instructions before your agent acts on them. 98% detection rate on agent attacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dmilstein-match](https://clawhub.ai/user/dmilstein-match)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check untrusted tool outputs for prompt injection before an agent follows instructions from those outputs. It is intended for workflows that handle web, email, file, API, or database content from external sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured guard endpoint may receive broad agent context, retrieved content, and an LLM API key.

Mitigation: Use only a trusted MLAYER_GUARD_URL, provide a dedicated revocable guard credential, and apply redaction, endpoint restrictions, and retention controls before sending sensitive content.

Risk: If the guard service is unavailable, acting on untrusted external content could bypass the intended prompt-injection check.

Mitigation: Warn the user and avoid acting on the external content until explicit confirmation is obtained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dmilstein-match/skills/mlayer-guard)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown instructions with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guard-result handling guidance for blocked, abstain, and safe responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
