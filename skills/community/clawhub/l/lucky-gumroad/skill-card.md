## Description:

Gumroad store automation for product creation, uploads, profile editing, and data pulls using a pre-authenticated Chrome profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and agent users use this skill to automate Gumroad seller workflows such as creating product listings, uploading files, editing profile details, and pulling sales or customer data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a persistent logged-in Gumroad seller browser profile with broad store-management authority.

Mitigation: Require explicit approval before accessing sales or customer data, publishing products, uploading files, or changing profile settings.

Risk: The Chrome profile functions like a credential because it contains an authenticated seller session.

Mitigation: Protect access to the Chrome profile, avoid clearing or exposing it, and restrict use to agents authorized for the qcautonomous/RayChod seller account.

Risk: The browser launch guidance includes insecure handling such as remote debugging, --no-sandbox, and a fixed temporary DOM dump path.

Mitigation: Disable or restrict remote debugging, avoid --no-sandbox where possible, and replace fixed /tmp dumps with secure temporary files that are deleted after use.

## Reference(s):

- [Lucky Gumroad Automation on ClawHub](https://clawhub.ai/rmbell09-lang/skills/lucky-gumroad)
- [Gumroad dashboard](https://gumroad.com/dashboard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing authenticated Chrome profile for the target Gumroad seller account.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
