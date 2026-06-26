## Description: <br>
Intelligent memory layer for Clawdbot using Mem0 that provides semantic search and automatic storage of user preferences, patterns, and context across conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agents use this skill to search, add, list, and delete persistent conversational memories so responses can adapt to user preferences, patterns, and prior context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores conversational memories persistently, which can retain personal context longer than a single session. <br>
Mitigation: Enable it deliberately, avoid storing secrets or sensitive personal data, and periodically review stored memories with the list command. <br>
Risk: Memory add and search workflows use OpenAI-backed processing through OPENAI_API_KEY. <br>
Mitigation: Confirm users understand that memory content may be processed by OpenAI and configure the API key only in deployments where that processing is acceptable. <br>
Risk: The delete script supports deleting all memories for a user without an interactive confirmation prompt. <br>
Mitigation: Use the --all deletion flag carefully and verify the target user ID before running deletion commands. <br>


## Reference(s): <br>
- [Mem0 Integration Patterns](references/integration-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/Sieyer/mem0-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/Sieyer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script output can include a ---JSON--- marker when JSON_OUTPUT is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
