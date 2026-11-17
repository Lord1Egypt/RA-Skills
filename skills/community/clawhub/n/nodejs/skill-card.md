## Description:

Builds, debugs, and hardens Node.js servers, CLIs, and npm packages across async behavior, modules, streams, memory, and process lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when writing, reviewing, debugging, and operating Node.js services, CLIs, libraries, npm packages, and runtime-side TypeScript. It helps diagnose hangs, leaks, module issues, dependency failures, HTTP timeout problems, flaky tests, container behavior, profiling, and graceful shutdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Debugging workflows may produce environment dumps or diagnostic reports that contain secrets or sensitive runtime details.

Mitigation: Redact secrets before sharing diagnostic artifacts and keep any generated reports access-controlled.

Risk: The skill may read and maintain scoped preference or memory files under ~/Clawic/data/nodejs/.

Mitigation: Review local preference and memory files before installation or use on production systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/nodejs)
- [Clawic NodeJS Skill](https://clawic.com/skills/nodejs)
- [NodeJS Skill Definition](artifact/SKILL.md)
- [Setup](artifact/setup.md)
- [Async](artifact/async.md)
- [Commands](artifact/commands.md)
- [Debugging](artifact/debug.md)
- [Security](artifact/security.md)
- [Production](artifact/production.md)
- [Runtime](artifact/runtime.md)
- [Testing](artifact/testing.md)
- [TypeScript On Node](artifact/typescript.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic commands, configuration guidance, code snippets, and review checklists tailored to Node.js projects.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
