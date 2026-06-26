## Description: <br>
GroqCloud (groq.com) lets agents read, create, and update GroqCloud data through the OOMOL oo CLI connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to operate GroqCloud through an OOMOL-connected account, including model discovery, model metadata lookup, and non-streaming OpenAI-compatible chat completions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected GroqCloud account and may use sensitive account credentials managed by OOMOL. <br>
Mitigation: Install and use it only when the agent is intended to access that connected GroqCloud account. <br>
Risk: Chat-completion requests may send user-provided content to GroqCloud and consume account credits. <br>
Mitigation: Review prompts and payloads before running chat-completion actions, especially for sensitive data or cost-sensitive accounts. <br>
Risk: Optional oo CLI installation and login steps introduce trust and account-linking decisions. <br>
Mitigation: Run install, login, or connection setup only after an auth or connection failure and only when the OOMOL oo CLI is trusted for the environment. <br>


## Reference(s): <br>
- [ClawHub GroqCloud Skill](https://clawhub.ai/oomol/oo-groqcloud) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [GroqCloud Homepage](https://groq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger GroqCloud connector calls through the OOMOL oo CLI and return connector JSON responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
