## Description:

Pull personal data (emails, issues) and propose outbound actions (drafts, replies) through the PersonalDataHub access control gateway. Data is filtered, redacted, and shaped by the owner's policy before reaching the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haojian](https://clawhub.ai/user/haojian)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to retrieve authorized personal data from services such as Gmail and GitHub through PersonalDataHub, then propose outbound email actions for owner review and approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access personal data sources and propose outbound email actions.

Mitigation: Use it only with a trusted PersonalDataHub instance, confirm owner-defined access policies before granting source access, and keep owner approval required for outbound actions.

Risk: The install path and packaged build require review before use.

Mitigation: Avoid the unpinned npx setup path and verify packaged dist files match the reviewed source before deployment.

Risk: Logs or configuration paths may expose API keys or sensitive personal-data context.

Mitigation: Restrict log access and treat configuration files and purpose strings as sensitive operational data.

## Reference(s):

- [PersonalDataHub project homepage](https://github.com/AISmithLab/PersonalDataHub)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and formatted JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls require a purpose string; outbound actions are staged for owner approval before execution.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
