## Description:

Searches Korean statutes, court cases, and everyday legal information through law.go.kr and data.go.kr APIs for legal questions and statute lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw326](https://clawhub.ai/user/sw326)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search Korean statutes, cases, official interpretations, and everyday legal information, then produce action-first Korean responses with legal bases and practical next steps. It is reference support only and does not replace legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and legal queries may be exposed because the security evidence reports plaintext HTTP use and local credential handling.

Mitigation: Use only non-sensitive queries until the scripts use HTTPS where available and credential files are stored with restrictive permissions.

Risk: User-supplied input may create command-execution injection exposure in the shell and Python handoff.

Mitigation: Pass user input as data rather than embedded Python source, and validate numeric counts and law or case identifiers before execution.

Risk: Legal search results can be outdated, incomplete, or mistaken for legal advice.

Mitigation: Cite current statutes or cases, mark repealed, amended, or future-effective law clearly, and recommend attorney review for sensitive decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sw326/skills/law-search)
- [law.go.kr Open API](https://open.law.go.kr)
- [data.go.kr](https://www.data.go.kr)
- [data.go.kr Case API](https://www.data.go.kr/data/15057123/openapi.do)
- [Artifact Playbook](artifact/playbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown legal-search response with supporting JSON results from shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should cite statutes or cases where available, mark amended or future-effective law clearly, and include a legal-advice disclaimer for sensitive matters.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
