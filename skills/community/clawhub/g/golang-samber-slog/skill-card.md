## Description: <br>
Structured logging extensions for Golang using samber/slog packages for multi-handler pipelines, log sampling, attribute formatting, HTTP middleware, and backend routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design Go slog pipelines with samber handlers, including sampling, PII-aware formatting, request logging middleware, routing, and backend sinks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated logging guidance may enable request body, response body, or broad header logging that exposes sensitive data. <br>
Mitigation: Require explicit scoping, redaction, size limits, sensitive-endpoint exclusions, retention controls, and user approval before enabling body or broad header logging. <br>
Risk: Generated configurations may route logs to external sinks and transmit operational or user data outside the application boundary. <br>
Mitigation: Require user approval for external log sinks and review destination, retention, and privacy settings before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-samber-slog) <br>
- [samber Go Skills Repository](https://github.com/samber/cc-skills-golang) <br>
- [slog-multi](https://github.com/samber/slog-multi) <br>
- [slog-sampling](https://github.com/samber/slog-sampling) <br>
- [slog-formatter](https://github.com/samber/slog-formatter) <br>
- [Pipeline Patterns](references/pipeline-patterns.md) <br>
- [Sampling Strategies](references/sampling-strategies.md) <br>
- [HTTP Middlewares](references/http-middlewares.md) <br>
- [Backend Handlers](references/backend-handlers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Go and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dependency versions, logging pipeline recommendations, and handler configuration examples.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
