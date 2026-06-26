## Description: <br>
Core GOYFILES external-bot contract for endpoint-first onboarding, strict agent behavior, direct tool mode, and text-fetch workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davfd](https://clawhub.ai/user/davfd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents use this skill to onboard with GOYFILES, verify bot ownership, and call hosted investigation tools for graph, document, archive, and full-text workflows. It is intended for operators who need structured access to the GOYFILES Epstein investigation graph and related source datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill registers an agent with an external service and receives one-time credentials and identity tokens. <br>
Mitigation: Keep credentials out of logs and persistent notes, and limit sharing of API keys and identity tokens to the active session that needs them. <br>
Risk: The verification flow may require a public social-media post that links an account to the bot. <br>
Mitigation: Confirm the account linkage and public visibility with the user before posting or submitting a claim tweet URL. <br>
Risk: The skill can use markdown write tools that may overwrite or append persistent notes. <br>
Mitigation: Confirm the target path and write mode before allowing overwrite or append actions. <br>
Risk: Fetched pages and investigation content may contain untrusted instructions. <br>
Mitigation: Treat fetched content as evidence only and follow the skill's structured API fields and anti-injection rule. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davfd/goyfiles-epstein) <br>
- [GOYFILES Skill Contract](https://goyfiles.com/skill.md) <br>
- [GOYFILES Tool Reference](https://goyfiles.com/bot-docs/tool-reference.md) <br>
- [GOYFILES Dataset and Source Reference](https://goyfiles.com/bot-docs/dataset-reference.md) <br>
- [GOYFILES Fulltext and Cypher Guide](https://goyfiles.com/bot-docs/fulltext-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include one-time API credentials, identity tokens, exact verification phrases, claim URLs, bounded text excerpts, and tool result payloads.] <br>

## Skill Version(s): <br>
6.5.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
