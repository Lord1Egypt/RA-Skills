## Description:

Parses Xiaohongshu/Rednote note URLs and returns supported note content data through the HotBee xhs_note_content endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanye1402-hash](https://clawhub.ai/user/shanye1402-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect supported content data from public Xiaohongshu/Rednote note URLs that the user explicitly supplies. It is scoped to note content parsing through HotBee and does not claim profile, account, or search collection support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run unaudited code from a personal GitHub repository while using a local API key.

Mitigation: Install only from a trusted source, prefer an immutable commit or integrity-backed package, and use a narrowly scoped, revocable HOTBEE_API_KEY with quota limits.

Risk: Live calls may consume HotBee quota and send note URLs to the HotBee endpoint.

Mitigation: Confirm user intent before live calls, process only public note URLs explicitly supplied by the user, and redact credentials or signed query parameters from errors.

## Reference(s):

- [Rednote Collect API](references/api.md)
- [HotBee Skills](https://www.hotbee.cn/skills)
- [ClawHub Skill Page](https://clawhub.ai/shanye1402-hash/skills/hotbee-rednote-collect)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI commands and API-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HOTBEE_API_KEY; only public user-supplied note URLs are in scope.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
