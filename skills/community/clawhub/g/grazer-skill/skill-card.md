## Description: <br>
Grazer helps AI agents discover, filter, and engage with content across social, academic, decentralized, video, podcast, and agent-network platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottcjn](https://clawhub.ai/user/scottcjn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Grazer to give agents a unified discovery and engagement workflow across multiple content platforms, with CLI, Python, and Node.js interfaces. It is most relevant when an agent needs to browse content, score relevance, monitor notifications, or publish replies/posts through connected accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish posts, replies, and other engagement through connected accounts. <br>
Mitigation: Use test accounts first, prefer dry-run previews where available, and review outbound actions before enabling publishing workflows. <br>
Risk: Continuous discovery and auto-response automation can act repeatedly or without enough operator review. <br>
Mitigation: Keep auto_respond disabled unless explicitly needed, use idempotency controls for repeated jobs, and run automation under narrow operating limits. <br>
Risk: The skill reads local account tokens and configuration from the user's Grazer directory. <br>
Mitigation: Restrict permissions on ~/.grazer, rotate credentials as needed, and avoid shared or production credentials during initial evaluation. <br>
Risk: The default LLM URL or bundled ClawHub token may not match the operator's security requirements. <br>
Mitigation: Replace the default LLM URL with an HTTPS endpoint the operator controls and do not use the bundled ClawHub token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scottcjn/grazer-skill) <br>
- [NPM package](https://www.npmjs.com/package/grazer-skill) <br>
- [PyPI package](https://pypi.org/project/grazer-skill) <br>
- [BoTTube skill page](https://bottube.ai/skills/grazer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code examples, configuration snippets, and structured discovery results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce outbound action previews, platform search results, generated SVG content, and account-connected posting guidance depending on requested workflow.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
