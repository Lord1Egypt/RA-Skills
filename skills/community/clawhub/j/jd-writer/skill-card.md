## Description:

Jd Writer helps create and improve recruiting job descriptions, including responsibilities, requirements, company introductions, benefits, salary references, and inclusivity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams, HR users, and hiring managers use this skill to draft job descriptions, generate role requirements and benefits language, compare salary ranges, optimize existing postings, and check for exclusionary wording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package has inconsistent entry points, which may confuse users about which job-description workflow is intended.

Mitigation: Clarify the supported entry point before use and prefer the documented JD workflow for recruiting use cases.

Risk: One included script records user inputs in local history, which can expose confidential hiring plans, company names, or draft JD text.

Mitigation: Disable or disclose local history logging before entering sensitive recruiting information.

Risk: Generated job descriptions, salary guidance, and inclusivity checks can be incomplete or inaccurate for a specific role, location, or legal context.

Mitigation: Have qualified recruiting, compensation, and legal reviewers check generated content before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/jd-writer)
- [JD-Writer usage tips and best practices](tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated job-description text, role requirements, benefits language, salary benchmark guidance, optimization notes, and inclusivity findings.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
