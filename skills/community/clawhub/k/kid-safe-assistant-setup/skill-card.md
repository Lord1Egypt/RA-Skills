## Description:

Deploy a locked-down OpenClaw chat assistant for a child: sandboxed tools, safety rules, photo/voice chat, parent progress digest

This skill is ready for commercial/non-commercial use.

## Publisher:

[entguinee-afk](https://clawhub.ai/user/entguinee-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and self-hosting administrators use this playbook to set up a child-focused homework assistant with restricted capabilities, a private chat page, and a parent progress digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Children’s conversations may be retained or accessible to people who do not need raw transcripts.

Mitigation: Set a clear retention and access policy before deployment; restrict transcript access and use the private summary export for parent updates.

Risk: The Docker helper is reported to use an unpinned image with write access to application code.

Mitigation: Review why write access is needed and limit it to the required volume and deployment window; use a trusted, pinned image.

Risk: The security scan was partial and could not resolve three local path-like references.

Mitigation: Resolve and review those references and complete a security review before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/entguinee-afk/skills/kid-safe-assistant-setup)
- [Publisher profile](https://clawhub.ai/user/entguinee-afk)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, Code]

**Output Format:** [Markdown with setup guidance, configuration examples, shell commands, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Step-by-step setup playbook; commands and examples may need adaptation to the host environment.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
