## Description: <br>
Use when a user needs to read, search, create, update, delete, comment on, tag, or inspect Memos data through this repository's Go CLI, especially when the agent should prefer real project commands over guessing HTTP API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogeecn](https://clawhub.ai/user/rogeecn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Memos from the terminal with the published Go CLI, including listing, searching, creating, updating, deleting, commenting on, tagging, and inspecting Memos data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an external Go CLI with @latest can change behavior between runs. <br>
Mitigation: Install only from a trusted source and consider pinning a specific CLI version. <br>
Risk: Memos API keys and admin keys can expose or modify private data. <br>
Mitigation: Use least-privileged keys, keep secrets out of committed files, and never echo secret values. <br>
Risk: Delete, update, comment, tag, and visibility commands can change or expose Memos data. <br>
Mitigation: Run configuration checks first and require explicit user confirmation for destructive or public-visibility changes. <br>
Risk: The artifact contains an inconsistent admin workflow example using go run. <br>
Mitigation: Use the canonical memos-cli binary for operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogeecn/memos-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to request or use Memos URL and API key configuration without echoing secret values.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
