## Description: <br>
Metaso Search helps agents query the Metaso Chinese AI search service and return structured Chinese search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuxinyuan321](https://clawhub.ai/user/qiuxinyuan321) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to run Chinese-language web searches through Metaso, retrieve structured results, and support Chinese knowledge lookup, concept explanation, question answering, and information organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Metaso API keys may be exposed if stored in plaintext files or committed to synced project directories. <br>
Mitigation: Store the key in an environment variable or secret manager, keep plaintext key files out of version control and sync tools, and rotate the key after suspected exposure. <br>
Risk: Search results can be incomplete, stale, or misleading for high-impact decisions. <br>
Mitigation: Review retrieved sources and use additional verification before relying on results for legal, medical, financial, or security-sensitive work. <br>


## Reference(s): <br>
- [Metaso Search ClawHub release](https://clawhub.ai/qiuxinyuan321/metaso-search) <br>
- [qiuxinyuan321 publisher profile](https://clawhub.ai/user/qiuxinyuan321) <br>
- [Metaso API playground](https://metaso.cn/search-api/playground) <br>
- [Metaso](https://metaso.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-oriented search result guidance with PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can request a result count and JSON output when the underlying PowerShell command is used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
