## Description: <br>
Identity Guard blocks personal, sensitive, or security-critical requests unless the current sender_id matches a configured master or allowlist entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhongxuYang](https://clawhub.ai/user/ZhongxuYang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw multi-user agents use this skill to gate sensitive answers, protected file edits, system operations, and allowlist management on sender_id-based authorization instead of display names or conversational claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change who is trusted through identities.json and allowlist updates. <br>
Mitigation: Restrict who can run init.sh or add-user.sh, review identities.json changes, and initialize the master identity in a private, controlled session. <br>
Risk: Authorization may be too broad when channel context is missing, because guard.sh can check whether a sender is authorized in any channel. <br>
Mitigation: Always pass trusted channel metadata to guard.sh for channel-scoped checks and avoid global allowlists unless broad access is intentional. <br>
Risk: Sender IDs and session logs are sensitive identifiers. <br>
Mitigation: Use direct messages for sender ID discovery, keep identities.json private, and treat session logs containing sender_id values as private data. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/ZhongxuYang/identity-guard) <br>
- [Publisher profile](https://clawhub.ai/user/ZhongxuYang) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces allow, deny, setup, and refusal guidance based on sender_id authorization state.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
