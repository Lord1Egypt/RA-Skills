## Description:

Checks draft answers against supplied documents for mismatched figures, arithmetic errors, and claims about the wrong entity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javihaus](https://clawhub.ai/user/javihaus)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use GroundLens before sending document-based answers with figures, dates, amounts, or names. It checks a draft against the supplied sources and identifies contradictions or claims needing review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker reads the local source files and draft answers supplied to it.

Mitigation: Install the groundlens command only if permitted and provide only the files needed for verification.

Risk: A PASS can miss incorrect free-text statements without figures; REVIEW leaves claims unconfirmed.

Mitigation: Treat it as a checking aid, not a complete truth validator; disclose unconfirmed claims and review important answers against the sources.

## Reference(s):

- [GroundLens on ClawHub](https://clawhub.ai/javihaus/skills/groundlens)
- [GroundLens homepage](https://groundlens.dev)
- [GroundLens code and documentation](https://github.com/groundlens-dev/groundlens)
- [GroundLens benchmark](https://github.com/groundlens-dev/groundlens/blob/main/BENCHMARK.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with a shell command and verification-result guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides handling of PASS, FAIL, and REVIEW decisions; PASS does not establish that the full answer is true.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
