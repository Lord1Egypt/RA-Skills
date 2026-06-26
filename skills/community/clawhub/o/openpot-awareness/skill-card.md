## Description: <br>
Teaches an agent how to serve content to the OpenPot iOS client, including cards, apps, page captures, calendar, voice, chat persistence, and onboarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[almnotai](https://clawhub.ai/user/almnotai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to integrate with the OpenPot iOS control center and decide when to respond in chat, create Pulse cards, build persistent web apps, handle page captures, use calendar context, configure voice, and set up chat persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can involve calendar credentials, backend chat storage, device pairing, optional SSH terminal access, and third-party voice or weather services. <br>
Mitigation: Install only when broad OpenPot integration is needed, review all tokens and calendar credentials before enabling, and use least-privilege accounts for connected services. <br>
Risk: Chat persistence may retain user conversations on a backend service. <br>
Mitigation: Decide retention and deletion behavior before enabling chat persistence, and document where chat history is stored. <br>
Risk: Voice and weather lookups may share data with external providers. <br>
Mitigation: Treat ElevenLabs and weather requests as external data sharing even when the local guide language suggests local-only behavior. <br>


## Reference(s): <br>
- [OpenPot homepage](https://openpot.app) <br>
- [OpenPot Awareness ClawHub release](https://clawhub.ai/almnotai/openpot-awareness) <br>
- [Server-resolved publisher profile](https://clawhub.ai/user/almnotai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, inline shell commands, HTML app files, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Pulse card payloads, calendar blocks, OpenPot status JSON updates, and self-contained HTML apps when requested.] <br>

## Skill Version(s): <br>
6.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
