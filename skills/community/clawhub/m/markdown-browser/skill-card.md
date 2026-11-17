## Description:

Wrapper skill for OpenClaw web_fetch results that post-processes fetched pages with Content-Signal policy decisions, privacy-preserving URL redaction, optional markdown normalization fallback, and a stable output schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill after an OpenClaw web_fetch call to normalize page content, redact sensitive URL components, and surface policy actions for downstream handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The normal npm install path uses plaintext third-party dependency URLs in the lockfile.

Mitigation: Review or regenerate the npm lockfile before installation, prefer an HTTPS trusted registry, exact dependency versions, and npm ci with integrity enforcement.

Risk: External fetched content may require review before use when Content-Signal handling returns needs_review or block_input.

Mitigation: Route downstream agent behavior through the emitted policy_action field and avoid using blocked or unresolved content without review.

## Reference(s):

- [Markdown Browser ClawHub skill page](https://clawhub.ai/2233admin/skills/markdown-browser)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON object with normalized content, format, token estimate, Content-Signal values, policy action, redacted source URL, status code, and fallback flag.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses official web_fetch results as input; HTML input may be converted to Markdown with turndown, and source URLs are redacted before output.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
