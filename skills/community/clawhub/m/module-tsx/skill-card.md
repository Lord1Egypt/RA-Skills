## Description:

Guides agents in writing browser HTML that runs TypeScript, TSX, or React without a build step using module-tsx.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yieldray](https://clawhub.ai/user/yieldray)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need an agent to create or explain browser pages that execute TypeScript, TSX, or React without a local build pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser pages generated from this skill may rely on third-party CDN-hosted JavaScript.

Mitigation: Pin exact module-tsx and package versions with an explicit import map; consider self-hosting or vendoring dependencies for production, sensitive, offline, or high-assurance pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yieldray/skills/module-tsx)
- [module-tsx on esm.sh](https://esm.sh/module-tsx)
- [module-tsx dev build on esm.sh](https://esm.sh/module-tsx/dev)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with HTML, TypeScript, TSX, and import map code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CDN URLs and version-pinning guidance for browser execution.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
