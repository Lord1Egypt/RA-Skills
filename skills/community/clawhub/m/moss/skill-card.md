## Description: <br>
Documentation and capabilities reference for Moss semantic search, including Moss APIs, SDKs, and integration patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CoderOMaster](https://clawhub.ai/user/CoderOMaster) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to understand Moss semantic search APIs, SDK methods, credentials, and integration patterns for adding retrieval to applications and voice agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Moss project keys can grant access to project data if exposed or used in the wrong environment. <br>
Mitigation: Provide a Moss project key only when the agent should access that project, prefer scoped or revocable keys, and avoid pasting real keys into shared terminals or prompts. <br>
Risk: Create, upsert, delete, upload, or sync actions can change Moss indexes or sensitive project data. <br>
Mitigation: Require confirmation before data-changing Moss operations and review the target project, index, and document set before proceeding. <br>


## Reference(s): <br>
- [Moss documentation](https://docs.moss.dev) <br>
- [Moss LLM documentation index](https://docs.moss.dev/llms.txt) <br>
- [Moss API endpoint](https://service.usemoss.dev/v1/manage) <br>
- [ClawHub skill page](https://clawhub.ai/CoderOMaster/moss) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with tables, SDK examples, API examples, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Moss credential environment variable names and examples for JavaScript, Python, REST API, and voice-agent integrations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
