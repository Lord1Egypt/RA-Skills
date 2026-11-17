## Description:

Construct explicitly unsigned J/D/T/V event drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schchit](https://clawhub.ai/user/schchit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create unsigned draft Judge, Delegate, Terminate, and Verify events for JEP-style workflows while keeping authority, signing, and verification outside the draft-construction step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsigned draft events could be mistaken for signed, verified, or action-executing records.

Mitigation: Treat draft=true and signature_valid=false as authoritative, and sign or verify only complete events with the configured security helpers.

Risk: Exposing the FastAPI service beyond loopback can increase authentication and traffic-control risk.

Mitigation: Bind locally by default; for remote use, add trusted TLS termination, request-rate limits, read-time limits, and proxy controls.

Risk: Bearer tokens and trusted key configuration can become sensitive operational secrets.

Mitigation: Generate high-entropy tokens, store only token digests in JEP_CLIENTS, protect environment configuration, and keep private keys outside the artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/schchit/skills/jep-primitive-skills)
- [README.md](artifact/README.md)
- [SECURITY.md](artifact/SECURITY.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [JSON, code, shell commands, configuration, guidance]

**Output Format:** [JSON API responses and Python dataclass results with canonical JSON strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are draft-only with draft=true and signature_valid=false; signing and verification require separate configured security helpers.]

## Skill Version(s):

2.0.0 (source: frontmatter, release evidence, manifest, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
