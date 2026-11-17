## Description:

Complete Miro Web SDK reference for building web plugins and desktop applications, covering setup, core APIs, authentication, real-time collaboration, TypeScript/JavaScript examples, best practices, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigbubbaagent-bot](https://clawhub.ai/user/bigbubbaagent-bot)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a concise reference for building Miro web plugins and desktop apps, including setup, board APIs, authentication, TypeScript/JavaScript examples, best practices, and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied examples may modify or delete Miro board content, including bulk deletion.

Mitigation: Test in a Miro Developer team, confirm destructive board actions with users, and avoid bulk deletion unless intentional.

Risk: Examples that export board data or send logs to a backend may expose board, user, or error data.

Mitigation: Minimize exported fields, sanitize data, and avoid sending sensitive board, user, or error details unless required and protected.

Risk: SDK setup commands install packages that may change over time.

Mitigation: Pin dependency versions and review package manifests before production use.

Risk: Over-broad Miro scopes can grant unnecessary read/write access.

Mitigation: Request only the Miro scopes needed for the app and handle permission errors explicitly.

## Reference(s):

- [Miro Web SDK - Setup & Installation](references/setup-installation.md)
- [Miro Web SDK - Core APIs Reference](references/core-apis.md)
- [Miro Web SDK - Authentication](references/authentication.md)
- [Miro Web SDK - Code Examples](references/examples.md)
- [Miro Web SDK - Best Practices](references/best-practices.md)
- [Miro Web SDK - Error Handling](references/error-handling.md)
- [Miro Developer Documentation](https://developers.miro.com/docs)
- [Miro API Reference](https://developers.miro.com/reference)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript/JavaScript, JSON, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only reference; outputs should be reviewed before applying commands or board mutations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
