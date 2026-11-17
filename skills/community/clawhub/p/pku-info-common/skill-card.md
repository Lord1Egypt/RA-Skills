## Description:

PKU Info Common guides agents working on the info-common shared authentication crate for PKU CLI tools, including IAAA login, OTP, credential resolution, session persistence, cookie storage, and QR rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when maintaining or extending the PKU info-common authentication crate and related PKU CLI tools. It helps with shared IAAA authentication, OTP handling, credential and keyring integration, session persistence, cookie storage, and QR-code login behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and SMS-code values may be exposed if placed in broad shell environments.

Mitigation: Prefer OS keyring or interactive prompts, and scope PKU_PASSWORD or PKU_SMS_CODE to the narrow operation that needs them.

Risk: Guidance may affect session, cookie, and authentication behavior for PKU CLI tools.

Mitigation: Review changes in the intended PKU info-common context before applying them, and do not write passwords to disk.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code identifiers, shell command examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference PKU credential, session, cookie, keyring, and SMS-code handling; avoid exposing passwords or SMS codes in generated commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
