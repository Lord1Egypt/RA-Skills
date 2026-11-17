## Description:

Build generative UI with OpenUI - any LLM provider, any backend language. Scaffold, integrate, validate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[othmanadi](https://clawhub.ai/user/othmanadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold, integrate, and validate OpenUI generative UI applications across React-oriented frontends, multiple LLM providers, and several backend languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated chat servers can allow unauthenticated use of a paid AI provider key.

Mitigation: Add authentication, authorization, rate limits, request and message limits, and provider spending caps before deployment.

Risk: Chat content and the generated system prompt are sent to the configured model provider.

Mitigation: Review provider data handling and disclose model-provider transmission to users.

Risk: Generated backend code or dependencies may be deployed before review.

Mitigation: Pin CLI and package versions, review generated routes, and scan the application before using it beyond local development.

## Reference(s):

- [OpenUI Lang Specification](references/openui-lang-spec.md)
- [OpenUI Component Patterns](references/component-patterns.md)
- [OpenUI Adapter Matrix](references/adapter-matrix.md)
- [OpenUI Backend Patterns](references/backend-patterns.md)
- [OpenUI LLM Full Corpus](https://www.openui.com/llms-full.txt)
- [OpenUI LLM Topic Index](https://www.openui.com/llms.txt)
- [Server-Resolved GitHub Source](https://github.com/OthmanAdi/openui-forge/tree/main/skills/openui-forge)
- [ClawHub Skill Page](https://clawhub.ai/othmanadi/skills/openui-forge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify project files when used to scaffold components, frontend pages, backend handlers, and validation scripts.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
