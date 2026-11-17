## Description:

Generates random 12-16 character passwords with configurable length and character sets including uppercase letters, lowercase letters, numbers, and symbols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for new random passwords, password generator settings, or batch password output for user-directed workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill requests broad computer access and includes unrelated security, audit, and password-storage claims.

Mitigation: Constrain use to explicit password-generation requests and avoid granting read, write, or exec authority unless a specific user-directed export workflow requires it.

Risk: The artifact describes threat-intelligence, CVE, compliance-audit, and password-storage features that are outside the core password-generation use case.

Mitigation: Treat the skill as a password generator only, and remove or disregard unrelated audit, threat-intelligence, and storage claims during review.

Risk: Generated passwords are sensitive secrets that can be exposed through logs, files, or shared conversation history.

Mitigation: Return passwords only to the requesting user, avoid logging or persistent storage by default, and require explicit user approval before exporting password lists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/password-generator-free)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Plain text or JSON, depending on the agent response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated password strings, character-set settings, or batch password lists when explicitly requested by the user]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
