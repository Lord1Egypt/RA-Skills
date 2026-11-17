## Description:

ict audits Claw Skill folders for code style, security vulnerabilities, documentation completeness, and code-documentation consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vimvem](https://clawhub.ai/user/vimvem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use ict to audit individual or batches of Claw Skills, score trust signals, compare versions, and produce findings in human-readable or JSON form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports can expose detected secrets when scanning repositories that contain real credentials.

Mitigation: Run scans only where generated reports are protected, redact sensitive findings before sharing, and avoid using real credential repositories for casual testing.

Risk: The skill makes an outbound update check to api.clawhub.ai.

Mitigation: Install and run it only in environments where outbound access to that service is acceptable.

Risk: Static scanner exclusions and pattern logic can miss malicious files or produce incomplete assurance.

Mitigation: Use ict as one review signal and keep manual review or additional security scanning in the approval process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vimvem/skills/ict)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Plain text reports or JSON audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit trust scores, issue summaries, batch scan summaries, comparison results, and trend records.]

## Skill Version(s):

4.0.8 (source: server release metadata, README.md, and SKILL.md Basic Info; SKILL.md frontmatter lists 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
