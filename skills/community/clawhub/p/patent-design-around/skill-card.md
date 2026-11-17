## Description:

Analyzes a patent’s independent claims, proposes design-around options, and searches for patents covering alternatives; results are preliminary and not legal advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

R&D teams and product engineers use the skill to review a target patent’s independent claims, explore possible feature removals, replacements, or changes, and check alternatives against patent search results. Treat the suggestions as preliminary and have qualified patent counsel review them before implementation.

### Deployment Geography for Use:

Global; patent data coverage includes China, the United States, Europe, Japan, South Korea, and WIPO.

## Known Risks and Mitigations:

Risk: Patent search terms may contain confidential information.

Mitigation: Use only public or approved non-confidential search terms.

Risk: API credentials could be exposed if destinations or redirects are not appropriately restricted.

Mitigation: Prefer an environment-based, limited-use API key and ask the publisher to clarify credential destinations and redirect handling before installation.

Risk: Cache handling and retries may create file-safety or unexpected billing concerns.

Mitigation: Ask the publisher to contain cache paths and clarify retry billing before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ip930/skills/patent-design-around)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Search workflow](references/search-workflow.md)
- [Query syntax](references/query-syntax.md)
- [API reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Files]

**Output Format:** [Excel-compatible UTF-8 CSV design-around table with patent search findings and accompanying guidance]

**Output Parameters:** [One target patent with one or more proposed alternatives]

**Other Properties Related to Output:** [Preliminary suggestions only; not legal advice and not a guarantee of non-infringement.]

## Skill Version(s):

1.0.2 (source: frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
