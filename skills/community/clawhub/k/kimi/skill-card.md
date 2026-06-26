## Description: <br>
Build and debug Kimi API workflows for chat, coding, reasoning, and tool-calling with live model checks, retries, and safe routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, debug, and migrate Moonshot Kimi API workflows for chat, coding, long-context research, structured outputs, and agent integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt content may be sent to Moonshot's Kimi API during use. <br>
Mitigation: Send only approved content, redact secrets and identifiers before API calls, and keep sensitive preprocessing local when needed. <br>
Risk: Moonshot API credentials could be mishandled if copied into files or prompts. <br>
Mitigation: Keep MOONSHOT_API_KEY in environment variables and do not store bearer tokens in project files, markdown notes, or debug logs. <br>
Risk: Optional local routing or approval notes may become stale or overly permissive. <br>
Mitigation: Review saved ~/kimi/ approval and routing notes periodically and update redaction boundaries before recurring workflows. <br>
Risk: Structured output or tool-facing responses may be invalid or unsafe to execute directly. <br>
Mitigation: Use strict schemas or a deterministic normalization pass, validate outputs before downstream writes, and avoid destructive automation from unvalidated responses. <br>


## Reference(s): <br>
- [Kimi skill page](https://clawhub.ai/ivangdavila/kimi) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Kimi API patterns](artifact/api-patterns.md) <br>
- [Kimi routing matrix](artifact/routing-matrix.md) <br>
- [Kimi safety workflows](artifact/safety-workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local note templates and API request patterns; users should review commands and redaction boundaries before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
