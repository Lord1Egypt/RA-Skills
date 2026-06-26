## Description: <br>
Kaiwu Search lets agents search Chinese (Traditional and Simplified) and English web content through the Kaiwu API, with bilingual query expansion and multi-engine aggregation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when an agent needs web search results for Chinese-language, Taiwan, China, East Asia, or bilingual research tasks where general search tools may return weak Chinese-language coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and usage metadata are sent to the external Kaiwu service. <br>
Mitigation: Do not send secrets, private documents, or sensitive research topics as search queries unless the user has approved that disclosure. <br>
Risk: The skill can use a wallet/SIWE signature to register with Kaiwu when an API key is missing. <br>
Mitigation: Require explicit user approval before wallet-based registration or account linking. <br>
Risk: The skill requires a sensitive API key. <br>
Mitigation: Store KAIWU_API_KEY only in the agent's secret store and avoid exposing it in logs, prompts, or generated command output. <br>


## Reference(s): <br>
- [ClawHub Kaiwu Search Release](https://clawhub.ai/daaab/kaiwu-search) <br>
- [Kaiwu API](https://kaiwu.dev) <br>
- [Kaiwu Search Endpoint](https://kaiwu.dev/v1/search) <br>
- [Kaiwu Credits Endpoint](https://kaiwu.dev/v1/credits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KAIWU_API_KEY and may use wallet/SIWE registration when a wallet is available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
