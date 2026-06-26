## Description: <br>
This skill helps agents convert markdown files or markdown text into JSON-safe strings for API calls, LLM prompts, and configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waldekmastykarz](https://clawhub.ai/user/waldekmastykarz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert markdown documentation, prompts, release notes, or help text into JSON-safe strings that can be embedded in API payloads, LLM prompts, configuration files, and CI/CD automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown converted for the OpenAI API example may include private prompts, credentials, internal documentation, or other sensitive content. <br>
Mitigation: Review and redact input files before sending converted content to external APIs; use the example only with content approved for that API account. <br>
Risk: Installing or running `mdstr` executes an npm package in the user's environment. <br>
Mitigation: Verify that the npm package `mdstr` is the intended package before installation or use. <br>


## Reference(s): <br>
- [ClawHub mdstr skill page](https://clawhub.ai/waldekmastykarz/mdstr) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration] <br>
**Output Format:** [Markdown with bash command examples and JSON string output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying CLI outputs one JSON-quoted string to stdout, strips trailing newlines by default, writes errors to stderr, and uses deterministic exit codes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
