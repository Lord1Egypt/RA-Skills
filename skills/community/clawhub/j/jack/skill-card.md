## Description:

Guides an agent through a Chinese-language workflow for collecting jack design parameters and generating CAD production sheet links through jixietools.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect jack CAD parameters one at a time, calculate design outputs, and create or monitor guest production sheets on jixietools.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends jack design parameters to jixietools.com and creates persistent guest production sheet links.

Mitigation: Review the skill before installing, disclose external data sharing to users, and require explicit confirmation before creating a guest production sheet.

Risk: The security evidence flags unsafe shell-style API templates for external HTTP requests.

Mitigation: Prefer a structured HTTP client where possible, or carefully review generated curl commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liv09370/skills/jack)
- [JixieTools API endpoint](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language Markdown with tables, JSON examples, curl commands, and production sheet status or link updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation at each step and may create persistent guest production sheets on jixietools.com.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
