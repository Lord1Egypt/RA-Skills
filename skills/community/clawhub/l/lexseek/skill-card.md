## Description: <br>
法索 AI 法律助手，提供法律条文检索功能，当用户询问法律问题、查询法规条文、查找司法解释或了解法律条款内容时，帮助检索相关法律依据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daixin877889](https://clawhub.ai/user/daixin877889) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search legal statutes, regulations, and judicial interpretations through LexSeek after authentication. The agent analyzes legal fact patterns, extracts professional legal search terms, runs one or more searches, and summarizes retrieved provisions with source names and article numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Legal queries and authentication data are sent to an external LexSeek service. <br>
Mitigation: Install only when the publisher and LexSeek are trusted, and avoid submitting sensitive legal facts unless the deployment accepts that data flow. <br>
Risk: The skill asks for account passwords through chat or CLI. <br>
Mitigation: Use a dedicated LexSeek account or pre-provisioned API key instead of a reusable main-account password. <br>
Risk: The API key is stored locally in plaintext. <br>
Mitigation: Run the skill in an isolated environment and use logout or key rotation after use. <br>
Risk: Legal-search results may be incomplete, unavailable, or unsuitable as legal advice. <br>
Mitigation: Treat responses as reference material and consult a qualified lawyer for specific legal decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daixin877889/lexseek) <br>
- [LexSeek service](https://lexseek.cn) <br>
- [登录与认证](artifact/references/auth.md) <br>
- [法律 API 接口](artifact/references/legal-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with retrieved legal provisions and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include multi-query result consolidation, law names, article numbers, effectiveness metadata, and reminders to consult a qualified lawyer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
