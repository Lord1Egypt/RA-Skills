## Description:

Guides agents auditing Go code for denial of service and resource exhaustion risks involving goroutines, channels, HTTP handling, resource allocation, parsers, and panic recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhy0](https://clawhub.ai/user/yhy0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to guide Go denial-of-service audits, identify resource-exhaustion patterns, and produce review notes or search commands for follow-up validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation is primarily Chinese, which can make review harder for users who need English or bilingual guidance.

Mitigation: Use it only in workflows where reviewers can accurately read the guidance or translate it before relying on findings.

Risk: The skill provides heuristic audit guidance and grep patterns that can produce false positives or miss context-specific issues.

Mitigation: Validate suspected vulnerabilities with manual code review, tests, and project-specific threat modeling before reporting or remediation.

## Reference(s):

- [Go DoS/Resource Exhaustion Real-World Cases](references/cases.md)
- [ClawHub skill page](https://clawhub.ai/yhy0/skills/go-vuln-dos)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese-language audit guidance; no executable code is included in the skill artifact.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
