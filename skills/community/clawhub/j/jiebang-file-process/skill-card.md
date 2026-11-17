## Description:

Processes text for MD5, SHA1, SHA256 hashing, Base64 encoding or decoding, and URL encoding or decoding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiebang-tools](https://clawhub.ai/user/jiebang-tools)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to calculate text or file-content hashes and to encode or decode Base64 and URL text. It is useful for checksum, text transformation, and format-conversion tasks where JSON results are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted content and an environment-based admin key are sent to an external JieBang service.

Mitigation: Do not use the skill with passwords, tokens, private URLs, proprietary files, or regulated data unless the external service and credential handling are approved.

Risk: The advertised operations could be performed locally, but this release depends on a remote service.

Mitigation: Prefer a local-only implementation for sensitive workflows or when external data transfer is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiebang-tools/skills/jiebang-file-process)
- [JieBang service](https://www.jiebang.site)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object containing the processed result and original input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an external JieBang service call and an admin credential; avoid submitting sensitive or regulated content.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
