## Description: <br>
MSW (Mock Service Worker) v2 best practices, patterns, and API guidance for API mocking in JavaScript/TypeScript tests and development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anivar](https://clawhub.ai/user/anivar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to write, review, and debug MSW v2 handlers, server setup, response construction, GraphQL mocks, and JavaScript/TypeScript test patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested changes to test setup, service-worker startup, or pass-through mocking could alter whether tests make real network requests. <br>
Mitigation: Review proposed changes before applying them, especially lifecycle hooks, worker startup, and passthrough or bypass behavior. <br>
Risk: Incorrect MSW guidance can cause tests to compile incorrectly or silently fail to intercept requests. <br>
Mitigation: Compare generated handlers and setup code against the skill's MSW v2 rules and the target project's installed MSW version. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anivar/msw-skill) <br>
- [Source Repository](https://github.com/anivar/msw-skill) <br>
- [Handler API Reference](references/handler-api.md) <br>
- [Response API Reference](references/response-api.md) <br>
- [Server API Reference](references/server-api.md) <br>
- [Test Patterns Reference](references/test-patterns.md) <br>
- [MSW v1 to v2 Migration Reference](references/migration-v1-to-v2.md) <br>
- [Anti-Patterns Reference](references/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript and JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; produces guidance and proposed code or configuration changes for agent review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
